# Vector Search Patterns

## Vector Search with Prefiltering

This is the default vector search setting. You can use prefiltering to boost query performance by reducing the search space before vector calculations begin. The system first applies your filter criteria to the dataset, then conducts vector search operations only on the remaining relevant subset.

```ts
import * as lancedb from "@lancedb/lancedb";

// Connect to LanceDB
const db = await lancedb.connect({
  uri: "db://your-project-slug",
  apiKey: "your-api-key",
  region: "us-east-1"
});

// Generate a sample 768-dimension embedding vector (typical for BERT-based models)
// In real applications, you would get this from an embedding model
const dimensions = 768;
const queryEmbed = Array.from({ length: dimensions }, () => Math.random() * 2 - 1);

// Open table and perform search
const tableName = "lancedb-enterprise-quickstart";
const table = await db.openTable(tableName);

// Vector search with filters (pre-filtering is the default)
const vectorResults = await table.search(queryEmbed)
  .where("label > 2")
  .select(["text", "keywords", "label"])
  .limit(5)
  .toArray();

console.log("Search results (with pre-filtering):");
console.log(vectorResults);
```

This filters out rows where label ≤ 2 before doing vector search, then picks specific columns from the top 5 matches.

The `.where("label > 2")` applies a filter before vector search, `.select(["text", "keywords", "label"])` chooses specific columns to return, and `.limit(5)` restricts results to the top 5 most similar vectors.

As a result, you'll see a pandas DataFrame with just the data you want from the most similar vectors.

## Vector Search with Postfiltering

Use postfiltering to prioritize vector similarity by searching the full dataset first, then applying metadata filters to the top results. This approach ensures you get the most similar vectors before filtering, which can be crucial when similarity is more important than metadata constraints.

```ts
const vectorResultsWithPostFilter = await (table.search(queryEmbed) as VectorQuery)
  .where("label > 2")
  .postfilter()
  .select(["text", "keywords", "label"])
  .limit(5)
  .toArray();

console.log("Vector search results with post-filter:");
console.log(vectorResultsWithPostFilter);
```

Here you can see how to do vector search first to get the most similar vectors, then filter by label > 1 on those results.

The `prefilter=False` parameter tells LanceDB to apply the filter after vector search instead of before, `.where("label > 1")` filters the top results by metadata, and `.select()` chooses which columns to include.

In the end, you receive a pandas DataFrame with the best matches that also meet your metadata requirements.

Post-filtering in LanceDB applies the filter condition after obtaining the nearest neighbors based on vector similarity.

## Multivector Search

Use multivector search when your documents contain multiple embeddings and you need sophisticated matching between query and document vector pairs. The late interaction approach finds the most relevant combinations across all available embeddings and provides nuanced similarity scoring.

Only cosine similarity is supported as the distance metric for multivector search operations.

```py
query_multi = np.random.random(size=(2, 256))
results_multi = tbl.search(query_multi).limit(5).to_pandas()
```

Here you can see how to take 2 query vectors and find the best matching pairs between them and document vectors using late interaction. The `np.random.random(size=(2, 256))` creates a 2×256 array with two random query vectors, `.limit(5)` returns the top 5 best document-query combinations, and `.to_pandas()` provides results in a DataFrame format.

Read more: Multivector search

## Advanced Search Scenarios

### Search With Distance Range

Use `distance_range` search when you need vectors within particular similarity bounds rather than just the closest neighbors. The system filters results to only include vectors that fall within your specified distance thresholds from the query.

```ts
import * as lancedb from "@lancedb/lancedb";

const results3 = await (
  tbl.search(Array(128).fill(1.2)) as lancedb.VectorQuery
)
  .distanceType("cosine")
  .distanceRange(0.1, 0.2)
  .limit(10)
  .toArray();
```

This shows three ways to search within distance ranges: bounded, upper bound only, and lower bound only.

The `distance_range()` method filters results by similarity thresholds — the first example finds vectors with distance between 0.1 and 0.5, the second finds vectors closer than 0.5, and the third finds vectors farther than 0.1.

Each approach returns Arrow tables with vectors that fall within your specified distance thresholds.

### Search With Binary Vectors

Use binary vector search for scenarios involving binary embeddings, such as those produced by hashing algorithms. The system stores these efficiently as packed uint8 arrays and uses Hamming distance calculations to determine vector similarity.

The number of dimensions of the binary vector must be a multiple of 8. A vector of dimensionality 128 will be stored as a uint8 array of size 16.

```ts
import * as lancedb from "@lancedb/lancedb";

import { Field, FixedSizeList, Int32, Schema, Uint8 } from "apache-arrow";

const schema = new Schema([
  new Field("id", new Int32(), true),
  new Field("vec", new FixedSizeList(32, new Field("item", new Uint8()))),
]);
const data = lancedb.makeArrowTable(
  Array(1_000)
    .fill(0)
    .map((_, i) => ({
      // the 256 bits would be store in 32 bytes,
      // if your data is already in this format, you can skip the packBits step
      id: i,
      vec: lancedb.packBits(Array(256).fill(i % 2)),
    })),
  { schema: schema },
);

const tbl = await db.createTable("binary_table", data);
await tbl.createIndex("vec", {
  config: lancedb.Index.ivfFlat({
    numPartitions: 10,
    distanceType: "hamming",
  }),
});

const query = Array(32)
  .fill(1)
  .map(() => Math.floor(Math.random() * 255));
const results = await tbl.query().nearestTo(query).limit(10).toArrow();
```

Here you can see how to set up a table for binary vectors, pack them efficiently into bytes, and search using Hamming distance.

The schema defines a 32-byte vector field (256 bits ÷ 8), `np.random.randint(0, 2, size=256)` creates binary vectors, `np.packbits()` compresses them to bytes, and `.distance_type("hamming")` specifies hamming distance for similarity calculation.

The search produces an Arrow table with binary vectors ranked by how many bits differ from the query.

## Scaling Vector Search

### Batch Search

Use batch search to handle multiple query vectors simultaneously. This gives you significant efficiency gains over individual queries. LanceDB processes all vectors in parallel and organizes results with a `query_index` field that maps each result set back to its originating query.

```ts
// Batch query
console.log("Performing batch vector search...");
const batchSize = 5;
const queryVectors = Array.from(
  { length: batchSize },
  () => Array.from(
    { length: dimensions },
    () => Math.random() * 2 - 1,
  ),
);
let batchQuery = table.search(queryVectors[0]) as VectorQuery;
for (let i = 1; i < batchSize; i++) {
  batchQuery = batchQuery.addQueryVector(queryVectors[i]);
}
const batchResults = await batchQuery
  .select(["text", "keywords", "label"])
  .limit(5)
  .toArray();
console.log("Batch vector search results:");
console.log(batchResults);
```

This takes 5 query embeddings and finds the top 5 matches for each one in a single batch operation.

The `load_dataset()` loads embeddings from a Hugging Face dataset, `query_embeds` contains 5 query vectors, and `.search(query_embeds)` processes all queries simultaneously.

The final result is a pandas DataFrame with all results, including a `query_index` to tell you which query each result came from.

When processing batch queries, the results include a `query_index` field to explicitly associate each result set with its corresponding query in the input batch.

### Search With Asynchronous Indexing

To optimize for speed over completeness, enable the `fast_search` flag in your query to skip searching unindexed data.

While vector indexing occurs asynchronously, newly added vectors are immediately searchable through a fallback brute-force search mechanism. This ensures zero latency between data insertion and searchability, though it may temporarily increase query response times.

```ts
await table
  .query()
  .nearestTo(embedding)
  .fastSearch()
  .limit(5)
  .toArray();
```

Here you can see how to turn on fast search mode to skip unindexed vectors and only look through indexed data for speed.

The `fast_search=True` parameter tells LanceDB to only search indexed vectors, skipping any recently added data that hasn't been indexed yet.

You'll obtain a pandas DataFrame with the top 5 matches from indexed vectors, but might miss data that was just added.

### Brute Force Search

### Search With No Index

The simplest way to perform vector search is to perform a brute force search, without an index, where the distance between the query vector and all the vectors in the database are computed, with the top-k closest vectors returned.

This is equivalent to a k-nearest neighbours (kNN) search in vector space.

Choose brute force search when you need guaranteed 100% recall, typically with smaller datasets where query speed isn't the primary concern. The system scans every vector in the table and calculates precise distances to find the exact nearest neighbors.

```ts
import * as lancedb from "@lancedb/lancedb";

const db = await lancedb.connect(databaseDir);
const tbl = await db.openTable("my_vectors");

const results1 = await tbl.search(Array(128).fill(1.2)).limit(3).toArray();
```

This carries out a brute force search through every vector in the table to find the 3 closest matches to a random 1536-dimensional query. You'll get back a list of the most similar vectors with exact distances.

As you can imagine, the brute force approach is not scalable for datasets larger than a few hundred thousand vectors, as the latency of the search grows linearly with the size of the dataset. This is where approximate nearest neighbour (ANN) algorithms come in.

### Bypass the Vector Index

Use `bypass_vector_index` to get exact, ground-truth results by performing exhaustive searches across all vectors. Instead of relying on approximate methods, the system directly compares your query against every vector in the table, ensuring 100% recall at the cost of increased query time.

```ts
await table
  .query()
  .nearestTo(embedding)
  .bypassVectorIndex()
  .limit(5)
  .toArray();
```

This skips the approximate index and checks every single vector for exact, ground-truth results.

The `.bypass_vector_index()` method forces LanceDB to perform an exhaustive search through all vectors instead of using the approximate nearest neighbor index, ensuring exact results but at the cost of slower performance.

The outcome is a pandas DataFrame with the top 5 exact matches, guaranteeing 100% recall but taking longer to run.

This approach is particularly useful when:
- Evaluating ANN index quality
- Calculating recall metrics to tune index parameters
- Ensuring exact results for critical applications
