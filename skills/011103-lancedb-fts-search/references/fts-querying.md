# FTS Querying

Learn how to implement full-text search in LanceDB using BM25 for keyword-based retrieval.

LanceDB provides support for Full-Text Search via Lance, allowing you to incorporate keyword-based search (based on BM25) in your retrieval solutions.

## Basic Usage

Consider that we have a LanceDB table named my_table, whose string column text we want to index and query via keyword search, the FTS index must be created before you can search via keywords.

### Table Setup

First, open or create the table you want to search:

```typescript
import * as lancedb from "@lancedb/lancedb";
const uri = "data/sample-lancedb"
const db = await lancedb.connect(uri);

const data = [
    { vector: [3.1, 4.1], text: "Frodo was a happy puppy" },
    { vector: [5.9, 26.5], text: "There are several kittens playing" },
];
const tbl = await db.createTable("my_table", data, { mode: "overwrite" });
```

### Construct FTS Index

Create a full-text search index on your text column:

```typescript
await tbl.createIndex("text", {
    config: lancedb.Index.fts(),
});
```

### Full-text Search

Perform full-text search and retrieve results:

```typescript
const results = await tbl
    .search("puppy", "fts")
    .select(["text"])
    .limit(10)
    .toArray();
```

The search is conducted on all indexed columns by default, so it's useful when there are multiple indexed columns.
If you want to specify which columns to search use `fts_columns="text"`.
LanceDB automatically searches on the existing FTS index if the input to the search is of type `str`. If you provide a vector as input, LanceDB will search the ANN index instead.

## Advanced Usage

### Tokenize Table Data

By default, the text is tokenized by splitting on punctuation and whitespaces, and would filter out words that are longer than 40 characters. All words are converted to lowercase.
Stemming is useful for improving search results by reducing words to their root form, e.g. "running" to "run". LanceDB supports stemming for multiple languages.

For example, to enable stemming for English:

```python
table.create_fts_index("text", language="English", replace=True)
```

Default index parameters:

- `base_tokenizer`: "simple"
- `language`: English
- `with_position`: false
- `max_token_length`: 40
- `lower_case`: true
- `stem`: true
- `remove_stop_words`: true
- `ascii_folding`: true
- `custom_stop_words`: None — pass a `list[str]` to drop additional words beyond the language defaults. Requires `remove_stop_words=True`.

For example, for language with accents:

```python
table.create_fts_index(
    "text",
    language="French",
    stem=True,
    ascii_folding=True,
    replace=True,
)
```

### Filtering Options

LanceDB full text search supports filtering the search results by a condition, both pre-filtering and post-filtering are supported.

With pre-filtering:

```typescript
await tbl
.search("puppy")
.select(["id", "doc"])
.limit(10)
.where("meta='foo'")
.prefilter(true)
.toArray();
```

With post-filtering:

```typescript
await tbl
.search("apple")
.select(["id", "doc"])
.limit(10)
.where("meta='foo'")
.prefilter(false)
.toArray();
```

### Phrase vs. Terms Queries

Lance-based FTS doesn't support queries using boolean operators OR, AND in the search string.
For full-text search you can specify either a phrase query like "the old man and the sea", or a terms search query like `old man sea`.
To search for a phrase, the index must be created with `with_position=True` and `remove_stop_words=False`:

```python
table.create_fts_index("text", with_position=True, replace=True)
```

This will allow you to search for phrases, but it will also significantly increase the index size and indexing time.

### Fuzzy Search

Fuzzy search allows you to find matches even when the search terms contain typos or slight variations. LanceDB uses the classic Levenshtein distance to find similar terms within a specified edit distance.

| Parameter | Type | Default | Description |
|---|---|---|---|
| fuzziness | int | 0 | Maximum edit distance allowed for each term. If not specified, automatically set based on term length: 0 for length ≤ 2, 1 for length ≤ 5, 2 for length > 5 |
| max_expansions | int | 50 | Maximum number of terms to consider for fuzzy matching. Higher values may improve recall but increase search time |

### Search for Substring

LanceDB supports searching for substrings in the text column, you can set the `base_tokenizer` parameter to `"ngram"` to enable this feature:

| Parameter | Type | Default | Description |
|---|---|---|---|
| ngram_min_length | int | 3 | Minimum length of the n-grams to search for |
| ngram_max_length | int | 3 | Maximum length of the n-grams to search for |
| prefix_only | bool | false | Whether to only search for prefixes of the n-grams |

### Example: Fuzzy Search

#### Generate Data

First, let's create a table with sample text data for testing fuzzy search:

```typescript
import * as lancedb from "@lancedb/lancedb"

const db = await lancedb.connect({
    uri: "db://your-project-slug",
    apiKey: "your-api-key",
    region: "us-east-1"
});

const tableName = "fts-fuzzy-boosting-test-ts";
const n = 100;
const vectors = Array.from({ length: n }, () => 
    Array.from({ length: 128 }, () => Math.random() * 2 - 1)
);

const textNouns = ["puppy", "car"];
const text2Nouns = ["rabbit", "girl", "monkey"];
const verbs = ["runs", "hits", "jumps", "drives", "barfs"];
const adverbs = ["crazily", "dutifully", "foolishly", "merrily", "occasionally"];
const adjectives = ["adorable", "clueless", "dirty", "odd", "stupid"];

const generateText = (nouns: string[]) => {
    const noun = nouns[Math.floor(Math.random() * nouns.length)];
    const verb = verbs[Math.floor(Math.random() * verbs.length)];
    const adv = adverbs[Math.floor(Math.random() * adverbs.length)];
    const adj = adjectives[Math.floor(Math.random() * adjectives.length)];
    return `${noun} ${verb} ${adv} ${adj}`;
};

const text = Array.from({ length: n }, () => generateText(textNouns));
const text2 = Array.from({ length: n }, () => generateText(text2Nouns));
const count = Array.from({ length: n }, () => Math.floor(Math.random() * 10000) + 1);
```

#### Create Table

```typescript
const data = makeArrowTable(
    vectors.map((vector, i) => ({
        vector,
        id: i % 2,
        text: text[i],
        text2: text2[i],
        count: count[i],
    }))
);

const table = await db.createTable(tableName, data, { mode: "overwrite" });
```

#### Construct FTS Index

```typescript
await table.createIndex("text", { config: Index.fts() });
await waitForIndex(table, "text_idx");

await table.createIndex("text2", { config: Index.fts() });
await waitForIndex(table, "text2_idx");
```

#### Basic and Fuzzy Search

**Basic Exact Search**

```typescript
import { MatchQuery } from "@lancedb/lancedb";

const basicMatchResults = await table.query()
    .fullTextSearch(new MatchQuery("crazily", "text"))
    .select(["id", "text"])
    .limit(100)
    .toArray();
```

**Fuzzy Search with Typos**

```typescript
const fuzzyResults = await table.query()
    .fullTextSearch(new MatchQuery("craziou", "text", {
        fuzziness: 2,
    }))
    .select(["id", "text"])
    .limit(100)
    .toArray();
```

**Prefix based Match**

```typescript
const fuzzyResults = await table.query()
    .fullTextSearch(new MatchQuery("cra", "text", {
        prefixLength: 3,
    }))
    .select(["id", "text"])
    .limit(100)
    .toArray();
```

#### Phrase Match

Phrase matching enables you to search for exact sequences of words. Unlike regular text search which matches individual terms independently, phrase matching requires words to appear in the specified order with no intervening terms.
Phrase queries are supported but only for a single column; providing multiple columns with a quoted phrase raises an error.

Phrase matching is particularly useful for:
- Searching for specific multi-word expressions
- Matching exact titles or quotes
- Finding precise word combinations in a specific order

```typescript
import { PhraseQuery } from "@lancedb/lancedb";

const phraseResults = await table.query()
  .fullTextSearch(new PhraseQuery("puppy runs", "text"))
  .select(["id", "text"])
  .limit(100)
  .toArray();
```

#### Flexible Phrase Match

To provide more flexible phrase matching, LanceDB supports the `slop` parameter. This allows you to match phrases where the terms appear close to each other, even if they are not directly adjacent or in the exact order, as long as they are within the specified slop value.

For example, the phrase query "puppy merrily" would not return any results by default. However, if you set `slop=1`, it will match phrases like "puppy jumps merrily", "puppy runs merrily", and similar variations where one word appears between "puppy" and "merrily".

```typescript
import { PhraseQuery } from "@lancedb/lancedb";

const phraseResults = await table.query()
  .fullTextSearch(new PhraseQuery("puppy runs", "text", { slop: 1 }))
  .select(["id", "text"])
  .limit(100)
  .toArray();
```
