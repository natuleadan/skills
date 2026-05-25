# FTS Advanced

## Search with Boosting

Boosting allows you to control the relative importance of different search terms or fields in your queries. This feature is particularly useful when you need to:
- Prioritize matches in certain columns
- Promote specific terms while demoting others
- Fine-tune relevance scoring for better search results

| Parameter | Type | Default | Description |
|---|---|---|---|
| positive | Query | required | The primary query terms to match and promote in results |
| negative | Query | required | Terms to demote in the search results |
| negative_boost | float | 0.5 | Multiplier for negative matches (lower values = stronger demotion) |

```typescript
import { MatchQuery, BoostQuery, MultiMatchQuery } from "@lancedb/lancedb";

const boostingResults = await table.query()
  .fullTextSearch(new BoostQuery(new MatchQuery("runs", "text"), new MatchQuery("puppy", "text"), {
    negativeBoost: 0.2,
  }))
  .select(["id", "text"])
  .limit(100)
  .toArray();
```

### Multi Match Query

Search across multiple fields simultaneously:

```typescript
const multiMatchResults = await table.query()
  .fullTextSearch(new MultiMatchQuery("crazily", ["text", "text2"]))
  .select(["id", "text", "text2"])
  .limit(100)
  .toArray();
```

### Search with Field Boosting

Apply different weightings per field:

```typescript
const multiMatchBoostingResults = await table.query()
  .fullTextSearch(new MultiMatchQuery("crazily", ["text", "text2"], {
    boosts: [1.0, 2.0],
  }))
  .select(["id", "text", "text2"])
  .limit(100)
  .toArray();
```

### Best Practices

- Use fuzzy search when handling user input that may contain typos or variations
- Apply field boosting to prioritize matches in more important columns
- Combine fuzzy search with boosting for robust and precise search results
- Create full-text search indices on text columns that will be frequently searched
- For hybrid search combining text and vectors, see hybrid search guide
- For complex queries, use SQL to combine FTS with other filter conditions

## Boolean Queries

LanceDB supports boolean logic in full-text search, allowing you to combine multiple queries using `and` and `or` operators. This is useful when you want to match documents that satisfy multiple conditions (intersection) or at least one of several conditions (union).

- In Python, combine two `MatchQuery` objects using either the `and` function or the `&` operator (e.g., `MatchQuery("puppy", "text") and MatchQuery("merrily", "text")`); both methods yield the same result. Similarly, use either the `or` function or the `|` operator for `or` queries.
- In TypeScript, boolean queries use `BooleanQuery` with a list of `[Occur, subquery]` pairs.

A boolean query must include at least one SHOULD or MUST clause. Queries that contain only a MUST_NOT clause are not allowed.

```typescript
import { MatchQuery, BooleanQuery, Occur } from "@lancedb/lancedb";

// Find documents containing both "puppy" and "merrily"
const mustResults = await table
    .search(
      new BooleanQuery([
        [Occur.Must, new MatchQuery("puppy", "text")],
        [Occur.Must, new MatchQuery("merrily", "text")],
      ]),
    )
    .select(["id", "text"])
    .limit(100)
    .toArray();

// Find documents containing either "puppy" or "merrily"
const shouldResults = await table
    .search(
      new BooleanQuery([
        [Occur.Should, new MatchQuery("puppy", "text")],
        [Occur.Should, new MatchQuery("merrily", "text")],
      ]),
    )
    .select(["id", "text"])
    .limit(100)
    .toArray();
```

### How to Use Booleans

| Operator | Python | TypeScript | Behavior |
|---|---|---|---|
| AND | `and` / `&` | `Occur.Must` | Intersection — documents must match all queries |
| OR | `or` / `\|` | `Occur.Should` | Union — documents must match at least one query |

## Substring Search (N-gram)

LanceDB supports searching for substrings in text columns using n-gram tokenization. This is useful for finding partial matches within text content.

### Setting Up the Table

First, create a table with sample text data and configure n-gram tokenization:

```python
import pyarrow as pa
import lancedb

db = lancedb.connect(":memory:")

data = pa.table({"text": ["hello world", "lance database", "lance is cool"]})
table = db.create_table("test", data=data)
table.create_fts_index("text", base_tokenizer="ngram")
```

### Basic Substring Search

With the default n-gram settings (minimum length of 3), you can search for substrings of length 3 or more:

```python
results = table.search("lan", query_type="fts").limit(10).to_list()
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}

results = (
    table.search("nce", query_type="fts").limit(10).to_list()
)
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}
```

### Handling Short Substrings

By default, the minimum n-gram length is 3, so shorter substrings like "la" won't match:

```python
results = table.search("la", query_type="fts").limit(10).to_list()
assert len(results) == 0
```

### Customizing N-gram Parameters

You can customize the n-gram behavior by adjusting the minimum length and using prefix-only matching:

```python
table.create_fts_index(
    "text",
    base_tokenizer="ngram",
    replace=True,
    ngram_min_length=2,
    prefix_only=True,
)
```

### Testing Custom N-gram Settings

With the new settings, you can now search for shorter substrings and use prefix-only matching:

```python
results = table.search("lan", query_type="fts").limit(10).to_list()
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}

results = (
    table.search("nce", query_type="fts").limit(10).to_list()
)
assert len(results) == 0

results = table.search("la", query_type="fts").limit(10).to_list()
assert len(results) == 2
assert set(r["text"] for r in results) == {"lance database", "lance is cool"}
```

## Full-Text Search on Array Fields

LanceDB supports full-text search on string array columns, enabling efficient keyword-based search across multiple values within a single field (e.g., tags, keywords).

### Setting Up the Connection

```typescript
import * as lancedb from "@lancedb/lancedb"

const db = await lancedb.connect({
  uri: "db://your-project-slug",
  apiKey: "your-api-key",
  region: "us-east-1"
});
```

### Defining the Schema

Create a schema that includes an array field for tags:

```typescript
const tableName = "fts-array-field-test-ts";

const schema = new Schema([
  new Field("id", new Utf8(), false),
  new Field("tags", new List(new Field("item", new Utf8()))),
  new Field("description", new Utf8(), false)
]);
```

### Creating Sample Data

```typescript
const data = makeArrowTable(
  Array(10).fill(0).map((_, i) => ({
    id: `doc_${i}`,
    tags: [
      ["python", "machine learning", "data science"],
      ["deep learning", "neural networks", "AI"],
      ["database", "indexing", "search"],
      ["vector search", "embeddings", "AI"],
      ["full text search", "indexing", "database"],
      ["python", "web development", "flask"],
      ["machine learning", "deep learning", "pytorch"],
      ["database", "SQL", "postgresql"],
      ["search engine", "elasticsearch", "indexing"],
      ["AI", "transformers", "NLP"]
    ][i],
    description: [
      "Python for data science projects",
      "Deep learning fundamentals",
      "Database indexing techniques",
      "Vector search implementations",
      "Full-text search guide",
      "Web development with Python",
      "Machine learning with PyTorch",
      "Database management systems",
      "Search engine optimization",
      "AI and NLP applications"
    ][i]
  })),
  { schema }
);
```

### Creating the Table and Adding Data

```typescript
const table = await db.createTable(tableName, data, { mode: "overwrite" });
```

### Building the Full-Text Search Index

```typescript
await table.createIndex("tags", {
  config: Index.fts()
});

const ftsIndexName = "tags_idx";
await waitForIndex(table, ftsIndexName);
```

### Performing Fuzzy Search

Search for terms with typos using fuzzy matching:

```typescript
const fuzzyResults = await table.query()
  .fullTextSearch(new MatchQuery("learnin", "tags", {
    fuzziness: 2,
  }))
  .select(["id", "tags", "description"])
  .toArray();
```

### Performing Phrase Search

Search for exact phrases within the array fields:

```typescript
const phraseResults = await table.query()
  .fullTextSearch(new PhraseQuery("machine learning", "tags"))
  .select(["id", "tags", "description"])
  .toArray();
```
