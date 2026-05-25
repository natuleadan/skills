# Hybrid Search

Learn how to perform hybrid search in LanceDB by combining vector and full-text search techniques with reranking.

In certain cases, you may want to retrieve documents that are semantically similar to a given query, but also prioritize specific keywords. This is an example of hybrid search, a query method that combines multiple search techniques.
For detailed examples, look at this Python Notebook or the TypeScript Example

## Example: Hybrid Search

### 1. Setup

Import the necessary libraries and dependencies for working with LanceDB, OpenAI embeddings, and reranking.

```typescript
import * as lancedb from "@lancedb/lancedb";
import "@lancedb/lancedb/embedding/openai";
import { Utf8 } from "apache-arrow";
```

### 2. Connect to LanceDB

Establish a connection to your LanceDB instance, with different options for Enterprise setups or open source.

**OSS**

```typescript
import * as lancedb from "@lancedb/lancedb";
import * as arrow from "apache-arrow";

const databaseDir = "data/sample-lancedb";
const db = await lancedb.connect(databaseDir);
```

**Enterprise**

For LanceDB Enterprise, set the db:// URI, region and the host override to your private cloud endpoint:

```typescript
import * as lancedb from "@lancedb/lancedb";
import * as arrow from "apache-arrow";

const uri = "db://my-lancedb-instance/my-database";
const apiKey = "your-api-key";
const region = "your-region";
const hostOverride = "your-host-override";

const db = await lancedb.connect(uri, {
  apiKey,
  region,
  hostOverride,
});
```

### 3. Configure Embedding Model

Set up the any embedding model that will convert text into vector representations for semantic search.

```typescript
const embedFunc = lancedb.embedding.getRegistry().get("openai")?.create({
  model: "text-embedding-ada-002",
}) as lancedb.embedding.EmbeddingFunction;
```

### 4. Create Table & Schema

Define the data structure for your documents, including both the text content and its vector representation.

```typescript
const documentSchema = lancedb.embedding.LanceSchema({
  text: embedFunc.sourceField(new Utf8()),
  vector: embedFunc.vectorField(),
});

const tableName = "hybrid_search_example";
const table = await db.createEmptyTable(tableName, documentSchema, {
  mode: "overwrite",
});
```

### 5. Add Data

Insert sample documents into your table, which will be used for both semantic and keyword search.

```typescript
const data = [
  { text: "rebel spaceships striking from a hidden base" },
  { text: "have won their first victory against the evil Galactic Empire" },
  { text: "during the battle rebel spies managed to steal secret plans" },
  { text: "to the Empire's ultimate weapon the Death Star" },
];
await table.add(data);
console.log(`Created table: ${tableName} with ${data.length} rows`);
```

### 6. Build Full Text Index

Create a full-text search index on the text column to enable keyword-based search capabilities.

```typescript
console.log("Creating full-text search index...");
await table.createIndex("text", {
  config: lancedb.Index.fts(),
});
await waitForIndex(table as any, "text_idx");
```

### 7. Set Reranker [Optional]

Initialize the reranker that will combine and rank results from both semantic and keyword search. By default, lancedb uses RRF reranker, but you can choose other rerankers like Cohere, CrossEncoder, or others lister in integrations section.

```typescript
const reranker = await lancedb.rerankers.RRFReranker.create();
```

### 8. Hybrid Search

Perform a hybrid search query that combines semantic similarity with keyword matching, using the specified reranker to merge and rank the results.

```typescript
console.log("Performing hybrid search...");
const queryVector = await embedFunc.computeQueryEmbeddings("full moon in May");
const hybridResults = await table
  .query()
  .fullTextSearch("flower moon")
  .nearestTo(queryVector)
  .rerank(reranker)
  .select(["text"])
  .limit(10)
  .toArray();

console.log("Hybrid search results:");
console.log(hybridResults);
```

### 9. Hybrid Search - Explicit Vector and Text Query pattern

You can also pass the vector and text query explicitly. This is useful if you're not using the embedding API or if you're using a separate embedder service.

```python
vector_query = [0.1, 0.2, 0.3, 0.4, 0.5]
text_query = "flower moon"
(
    table.search(query_type="hybrid")
    .vector(vector_query)
    .text(text_query)
    .limit(5)
    .to_pandas()
)
```

## More on Reranking

You can perform hybrid search in LanceDB by combining the results of semantic and full-text search via a reranking algorithm of your choice. LanceDB comes with built-in rerankers and you can implement your own custom reranker as well.
By default, LanceDB uses RRFReranker(), which uses reciprocal rank fusion score, to combine and rerank the results of semantic and full-text search. You can customize the hyperparameters as needed or write your own custom reranker. Here's how you can use any of the available rerankers:

| Argument | Type | Default | Description |
|---|---|---|---|
| normalize | str | "score" | The method to normalize the scores. Can be rank or score. If rank, the scores are converted to ranks and then normalized. If score, the scores are normalized directly. |
| reranker | Reranker | RRF() | The reranker to use. If not specified, the default reranker is used. |
