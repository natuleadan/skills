Vector Indexes
Build and optimize LanceDB vector indexes, including IVF, HNSW and binary quantized indexes.

You can create and manage multiple vector indexes on any Lance dataset. LanceDB offers two kinds of vector indexing algorithms: Inverted File (IVF) and Hierarchical Navigable Small World (HNSW).
IVF + HNSW
In LanceDB, HNSW is not exposed as a top-level vector index. Instead, it's available as a sub-index inside IVF partitions. What this means in practice is that vectors are first partitioned by IVF, then each selected partition is searched using an HNSW graph. LanceDB supports the unquantized variant IVF_HNSW_FLAT, along with quantized variants such as IVF_HNSW_PQ and IVF_HNSW_SQ. This combines IVF's scalability with HNSW's higher-recall ANN search within partitions.

Manual Indexing
If using LanceDB OSS, you will have to create the vector index manually, by calling table.create_index(), and updating the index as new data arrives and tuning its parameters is also a manual process.

Automatic Indexing
Enterprise-only Vector indexing is managed automatically in LanceDB Enterprise. As soon as data is updated, the system updates the index and optimizates it. This is done asynchronously as a background process.
When you create a table in LanceDB Enterprise, LanceDB automatically:
Infers the vector columns from the schema
Create an optimized IVF_PQ index without manual configuration
Automatically configure indexing parameters
The default distance is l2 (Euclidean).
You can call create_index() with different parameters to create a new index — this replaces any existing index. Although the create_index API returns immediately, the building of the vector index is asynchronous. To wait until all data is fully indexed, you can specify the wait_timeout parameter.

Choose the Right Index
Use this table as a quick starting point for choosing the right index type and quantization method for your use case:
If your top priority is…	Use this index	Why	Typical compressed size vs. raw vectors
Highest recall / no quantization	IVF_HNSW_FLAT	Uses raw vectors inside the IVF+HNSW structure, avoiding quantization loss.	Around raw vector size plus HNSW graph overhead
Best recall/latency trade-off	IVF_HNSW_SQ	Combines IVF partitioning with HNSW graph search for strong quality at low latency.	Typically a little larger than 1/4 of raw size
Maximum compression	IVF_RQ	RaBitQ-style quantization with very strong compression.	Around 1/32 of raw size
Higher accuracy at small dimensions (dimension <= 256)	IVF_PQ	On small-dimensional vectors, IVF_PQ often provides higher accuracy with similar performance compared to IVF_RQ.	Usually 1/64 to 1/16 of raw size (depends on num_sub_vectors)
If your vector search frequently includes metadata filters (where(...)), prefer IVF_RQ or IVF_PQ. In filtered workloads, HNSW-backed IVF indexes such as IVF_HNSW_FLAT and IVF_HNSW_SQ can show higher latency variance.
Compression ratios are practical rules of thumb and can vary with vector distribution, metric, and configuration. For small dimensions, choose IVF_PQ for accuracy, not for guaranteed higher compression than IVF_RQ.

Index Tuning
Start with these values, then tune for your workload:
HNSW-backed IVF indexes (IVF_HNSW_FLAT, IVF_HNSW_SQ, IVF_HNSW_PQ)
num_partitions: start at num_rows // 1,048,576 (rounded to an integer)
Lower num_partitions can reduce search latency, but index build may become slower because partitions are larger.
ef_construction: start at 150; increase for better recall, decrease for faster indexing.
IVF_RQ
num_partitions: start at num_rows // 4096 (rounded to an integer). This is a strong default for most datasets.
IVF_PQ
num_partitions: start at num_rows // 4096 (rounded to an integer).
num_sub_vectors: start at dimension // 8. Increase for better recall, decrease for faster search and smaller indexes.
For small dimensions (dimension <= 256), IVF_PQ is often preferred over IVF_RQ for better accuracy at similar query performance.

Example: Construct an IVF Index
In this example, we will create an index for a table containing 1536-dimensional vectors. The index will use IVF_PQ with L2 distance, which is well-suited for high-dimensional vector search.
Make sure you have enough data in your table (at least a few thousand rows) for effective index training.

Index Configuration
Sometimes you need to configure the index beyond default parameters:
Index Types:
IVF_HNSW_FLAT: highest recall, with no vector quantization
IVF_HNSW_SQ: best recall/latency trade-off
IVF_RQ: best compression for large, high-dimensional datasets
IVF_PQ: often higher accuracy than IVF_RQ for small dimensions (<= 256) at similar query performance
metrics: default is l2, other available are cosine or dot
When using cosine similarity, distances range from 0 (identical vectors) to 2 (maximally dissimilar)
num_partitions: use index-specific starting points from the section above:
HNSW-backed IVF indexes (IVF_HNSW_FLAT, IVF_HNSW_SQ, IVF_HNSW_PQ): num_rows // 1,048,576
IVF_RQ and IVF_PQ: num_rows // 4096
num_sub_vectors: applies to IVF_PQ; start with dimension // 8. Larger values often improve recall but can slow search.
Let's take a look at a sample request for an IVF index:

```python
table.create_index(metric="l2", num_partitions=16, num_sub_vectors=4)
```

1. Setup
Connect to LanceDB and open the table you want to index.

```python
table_name = "vector-index-tbl"
table = db.open_table(table_name)
```

2. Construct an IVF Index
Create an IVF_PQ index with cosine similarity. Specify vector_column_name if you use multiple vector columns or non-default names. You can switch index_type to IVF_RQ, IVF_HNSW_SQ, or IVF_HNSW_FLAT depending on your recall/latency/compression target.

```python
table_name = "vector-index-build-ivf"
table = db.open_table(table_name)
table.create_index(
    metric="cosine",
    vector_column_name="keywords_embeddings",
)
```

3. Query the IVF Index
Search using a random 1,536-dimensional embedding.

```python
tbl = table
tbl.search(np.random.random((1536))).limit(2).nprobes(20).refine_factor(
    10
).to_pandas()
```

Search Configuration
Core knobs available on a vector search call:
Parameter	Description
limit	Number of results to return (k).
nprobes	Shorthand that sets both minimum_nprobes and maximum_nprobes to the same value. LanceDB auto-tunes this by default.
minimum_nprobes	Partitions that are always scanned. Higher values raise recall at the cost of latency.
maximum_nprobes	Upper bound on partitions scanned. The partitions above minimum_nprobes are only searched if the initial pass does not return enough results — useful for narrow filters. Set to 0 to remove the cap.
ef	HNSW search-time exploration factor. Relevant for IVF_HNSW_FLAT and IVF_HNSW_SQ; start around 1.5 * k and increase up to 10 * k for higher recall.
refine_factor	Reads additional candidates and reranks them in memory to recover recall lost to quantization.
Filtered queries and adaptive nprobes. When a where(...) filter is active, LanceDB starts by scanning minimum_nprobes partitions and only extends toward maximum_nprobes if fewer than limit rows survive the filter. Setting minimum_nprobes == maximum_nprobes (or calling nprobes(n)) disables this adaptive behavior and fixes the partition count.

```python
# Always scan 10 partitions; scan up to 50 only if the initial pass
# returns fewer than `limit` results (common with narrow filters).
(
    table.search(np.random.random(128))
    .minimum_nprobes(10)
    .maximum_nprobes(50)
    .where("id > 100")
    .limit(5)
    .to_pandas()
)
```
Recommended nprobes behavior by index type:
Index type	Guidance
IVF_HNSW_FLAT, IVF_HNSW_SQ	Keep the auto-tuned nprobes, then tune ef first. Expect higher latency variance under filtered search.
IVF_RQ	Keep auto-tuned nprobes; raise only when recall is insufficient.
IVF_PQ	Keep auto-tuned nprobes; raise when recall is insufficient. Often preferred over IVF_RQ when dimension <= 256.

Advanced Search Controls
These controls are useful for thresholded retrieval, recall measurement, and working around index-level metric constraints.
Method	Description
distance_range(lower_bound, upper_bound)	Return only rows whose distance falls within [lower_bound, upper_bound). Either bound is optional. Useful for near-duplicate detection or "close-enough" matching.
bypass_vector_index()	Skip the ANN index and perform an exhaustive (flat) scan. Primary uses: (1) compute ground-truth results to measure ANN recall@k, and (2) query with a metric the index was not built for (e.g., a non-cosine query on a multivector column).
Thresholding with distance_range:

```python
# Only return results whose distance falls within [0.0, 0.5).
# Useful for near-duplicate detection or thresholded similarity search.
(
    table.search(np.random.random(128))
    .distance_range(lower_bound=0.0, upper_bound=0.5)
    .limit(10)
    .to_pandas()
)
```
Measuring recall with bypass_vector_index:
Compare ANN results against a flat-scan ground truth to compute recall@k. This is the standard way to pick nprobes for your workload.

```python
query = np.random.random(128)
k = 10

# Ground truth: flat (exhaustive) scan, ignoring the ANN index.
truth = set(table.search(query).bypass_vector_index().limit(k).to_pandas()["id"])

# ANN results with the current nprobes setting.
ann = set(table.search(query).nprobes(20).limit(k).to_pandas()["id"])

recall_at_k = len(truth & ann) / k
```
Flat search is O(n) — reserve bypass_vector_index() for sampled recall measurements or small tables, not production queries.
Multivector indexing currently requires distance_type="cosine" — l2 is rejected at index-creation time. That restriction is why bypass_vector_index() is the escape hatch for non-cosine queries on a multivector column: the metric you want at query time cannot be served by the index, so you fall back to a flat scan. See Multivector Search for the full rules.

Example: Construct an HNSW Index

Index Configuration
There are four key parameters to set when constructing an HNSW index:
index_type: choose IVF_HNSW_SQ for a strong recall/latency/size trade-off, or IVF_HNSW_FLAT when you want the IVF+HNSW structure without vector quantization.
metric: The default is l2 euclidean distance metric. Other available are dot and cosine.
m: The number of neighbors to select for each vector in the HNSW graph.
ef_construction: The number of candidates to evaluate during the construction of the HNSW graph.

1. Construct an HNSW Index
The snippet below uses IVF_HNSW_SQ. If you want the unquantized variant, change index_type to IVF_HNSW_FLAT.

```python
table.create_index(index_type="IVF_HNSW_SQ")
```

2. Query the HNSW Index

```python
tbl = table
tbl.search(np.random.random((16))).limit(2).to_pandas()
```

Example: Construct a Binary Vector Index
Binary vectors are useful for hash-based retrieval, fingerprinting, or any scenario where data can be represented as bits.

Index Configuration
Store binary vectors as fixed-size binary data (uint8 arrays, with 8 bits per byte). For storage, pack binary vectors into bytes to save space.
Index Type: IVF_FLAT is used for indexing binary vectors
metric: the hamming distance is used for similarity search
The dimension of binary vectors must be a multiple of 8. For example, a 128-dimensional vector is stored as a uint8 array of size 16.
IVF_FLAT + hamming is the only supported path for binary vectors.
hamming distance is only valid on packed binary (uint8) data; it is rejected on float vector columns.
Quantized index types (IVF_PQ, IVF_RQ, IVF_SQ, IVF_HNSW_PQ, IVF_HNSW_SQ) do not accept binary inputs — their distance_type is restricted to l2, cosine, or dot.

1. Create Table and Schema

```python
table = tmp_db.create_table(table_name, schema=schema, mode="overwrite")
```

2. Generate and Add Data

```python
table.add(data)
```

3. Construct the Binary Index

```python
table.create_index(
    metric="hamming",
    vector_column_name="vector",
    index_type="IVF_FLAT",
)
```

4. Vector Search

```python
query = np.random.randint(0, 2, size=ndim)
query = np.packbits(query)
df = table.search(query).metric("hamming").limit(10).to_pandas()
df.vector = df.vector.apply(np.unpackbits)
```

Check Index Status
Vector index creation is fast - typically a few minutes for 1 million vectors with 1536 dimensions. You can check index status in two ways:

Option 1: Check the UI
Navigate to your table page - the "Index" column shows index status. It remains blank if no index exists or if creation is in progress.

Option 2: Use the API
Use list_indices() and index_stats() to check index status. By default, the index name is formed by appending _idx to the column name (e.g., a keywords_embeddings column produces keywords_embeddings_idx). Note that list_indices() only returns information after the index is fully built. To wait until all data is fully indexed, you can specify the wait_timeout parameter on create_index() or call wait_for_index() on the table.

```python
index_name = "keywords_embeddings_idx"
table.wait_for_index([index_name])
print(table.index_stats(index_name))
```

Custom Index Names
The {column}_idx suffix is a default convention, not the only supported naming path. Pass name=... to create_index() to override it — useful when you want to manage multiple indexes on the same column (for example, side-by-side IVF_PQ and IVF_HNSW_SQ builds) or when you script index replacement by name. Once set, list_indices(), index_stats(name), and wait_for_index([name]) all reference the custom name.

```python
# Override the default `{column}_idx` convention by passing `name=...`.
table.create_index(
    metric="cosine",
    vector_column_name="keywords_embeddings",
    name="my_custom_index",
)
table.wait_for_index(["my_custom_index"])
print(table.index_stats("my_custom_index"))
```
