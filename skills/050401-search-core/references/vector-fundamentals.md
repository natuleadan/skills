# Vector Search Fundamentals

Vector search is a technique used to search for similar items based on their vector representations, called embeddings. It is also known as similarity search, nearest neighbor search, or approximate nearest neighbor search.

Raw data (e.g. text, images, audio, etc.) is converted into embeddings via an embedding model, which are then stored in a multimodal lakehouse like LanceDB. To perform similarity search at scale, an index is created on the stored embeddings, which can then used to perform fast lookups.

## Supported distance metrics

Distance metrics determine how LanceDB compares vectors to find similar matches. Euclidean or l2 is the default, and used for general-purpose similarity, cosine for unnormalized embeddings, dot for normalized embeddings (best performance), or hamming for binary vectors.

Ensure you always use the same distance metric that your embedding model was trained with. Most modern embedding models use cosine similarity, so cosine is often the best choice. However, if your vectors are normalized, you should use dot for best performance.

The right metric improves both search accuracy and query performance. Currently, LanceDB supports the following metrics:

| Distance metric | Mathematical form | Notes |
|---|---|---|
| `l2` | √(∑(xᵢ − yᵢ)²) | Measures the straight-line distance between two points in vector space. Calculated as the square root of the sum of squared differences between corresponding vector components. |
| `cosine` | 1 − (x·y / (‖x‖₂ ‖y‖₂)) | Measures directional difference between vectors. Computed as 1 minus cosine similarity (the dot product normalized by both vector magnitudes), so vector length does not affect the score. Use for unnormalized vectors. |
| `dot` | x·y = ∑ xᵢ yᵢ | Calculates the sum of products of corresponding vector components. Provides raw similarity scores without normalization, sensitive to vector magnitudes. Use for normalized vectors for best performance. |
| `hamming` | ∑ 1[xᵢ ≠ yᵢ] | Counts the number of positions where corresponding bits differ between binary vectors. Only applicable to binary vectors stored as packed uint8 arrays. |

For indexed search, supported distance metrics vary by index type:

| Index type | Supported distance metrics |
|---|---|
| IVF_FLAT | ["l2", "cosine", "dot", "hamming"] |
| IVF_PQ | ["l2", "cosine", "dot"] |
| IVF_SQ | ["l2", "cosine", "dot"] |
| IVF_RQ | ["l2", "cosine", "dot"] |
| IVF_HNSW_FLAT | ["l2", "cosine", "dot"] |
| IVF_HNSW_PQ | ["l2", "cosine", "dot"] |
| IVF_HNSW_SQ | ["l2", "cosine", "dot"] |

## Configure Distance Metric

By default, l2 will be used as metric type. You can specify the metric type as cosine or dot if required (hamming is supported for IVF_FLAT index only).

Note: You can configure the distance metric during search only if there's no vector index. If a vector index exists, the distance metric will always be the one you specified when creating the index.

```ts
const results2 = await (
  tbl.search(Array(128).fill(1.2)) as lancedb.VectorQuery
)
  .distanceType("cosine")
  .limit(10)
  .toArray();
```

Here you can see the same search but using cosine similarity instead of l2 distance. The result focuses on vector direction rather than absolute distance, which works better for normalized embeddings.

## Vector Search With ANN Index

Instead of performing an exhaustive search on the entire database for each and every query, approximate nearest neighbour (ANN) algorithms use an index to narrow down the search space, which significantly reduces query latency.

The trade-off is that the results are not guaranteed to be the true nearest neighbors of the query, but are usually "good enough" for most use cases.

Use ANN search for large-scale applications where speed matters more than perfect recall. LanceDB uses approximate nearest neighbor algorithms to deliver fast results without examining every vector in your dataset.

When a vector index is used, `_distance` is not always the true distance between full vectors. On quantized ANN indexes, LanceDB may compute `_distance` from the compressed representation for speed. Use `refine_factor` when you want reranking on full vectors.

## Exact vs Approximate Distances

When doing vector search, the meaning of "distance" depends on whether you are using an index and whether `refine_factor` is specified as part of your query. `nprobes` controls how many partitions are searched to find candidates, while `refine_factor` controls how many candidates are rescored on full vectors for better distance fidelity and reranking quality.

The table below summarizes the behavior of `_distance` in search results based on your query configuration:

| Query mode | Neighbor quality | `_distance` in results |
|---|---|---|
| No index or `.bypass_vector_index()` | Exact kNN (100% recall) | True distance on full vectors |
| Indexed ANN, no `refine_factor` | Approximate neighbors | Distance on the index representation: exact for flat indexes, approximate for quantized indexes |
| Indexed ANN + `refine_factor(1)` | Approximate neighbors (same candidate set) | Distances recomputed on full vectors for reranked candidates |
| Indexed ANN + `refine_factor(>1)` | Better recall than no refine (usually) | Distances recomputed on full vectors for reranked candidates |

```ts
// Indexed ANN search without refinement (fast, approximate `_distance`)
const fastResults = await (table.search(embedding) as lancedb.VectorQuery)
  .limit(10)
  .toArray();

// Recompute distances on full vectors for reranked candidates
const exactDistanceResults = await (table.search(embedding) as lancedb.VectorQuery)
  .limit(10)
  .refineFactor(1)
  .toArray();

// Rerank a larger candidate set for better recall (higher latency)
const higherRecallResults = await (table.search(embedding) as lancedb.VectorQuery)
  .limit(10)
  .refineFactor(20)
  .toArray();
```

For deeper tuning guidance on indexing and performance estimation, see the vector indexes page. For tuning nprobes, see below.

## Tuning nprobes

`nprobes` controls how many partitions are searched at query time.

`nprobes` improves candidate recall, but does not by itself make `_distance` exact.

By default, LanceDB automatically tunes `nprobes` to achieve the best performance without noticeably sacrificing accuracy.

In most cases, leave `nprobes` unset and use the auto-tuned value.

Only tune `nprobes` manually when recall is below your target, or when you need even higher performance for your workload.

- If recall is too low, increase `nprobes` gradually, but after a certain threshold, increasing `nprobes` yields only marginal accuracy gains.
- If you need higher performance and have recall headroom, decrease `nprobes` gradually.
