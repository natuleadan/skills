# FTS Index

Create and tune BM25-based full-text search indexes in LanceDB.

LanceDB provides performant full-text search based on BM25, allowing you to incorporate keyword-based search in your retrieval solutions. This page shows examples on how to create and configure FTS indexes in LanceDB OSS and Enterprise, using the synchronous and asynchronous APIs.
In LanceDB Enterprise, create_fts_index API returns immediately, but index building happens asynchronously.

## Creating FTS Indexes

### Synchronous API

Use create_fts_index with synchronous LanceDB connections:

```python
table_name = "fts-index-create"
table = db.open_table(table_name)
table.create_fts_index("text")
```

Check FTS index status using the API:

```python
table_name = "fts-index-wait"

table = db.open_table(table_name)
table.create_fts_index("text")

index_name = "text_idx"
table.wait_for_index([index_name])
```

### Asynchronous API

When using async connections (connect_async), use create_index with the FTS configuration:

```python
import asyncio

import lancedb
import polars as pl
from lancedb.index import FTS

data = pl.DataFrame(
    {
        "id": [1, 2],
        "text": [
            "His first language is spanish",
            "Her first language is english",
        ],
    }
)

async def main(data: pl.DataFrame):
    uri = "ex_lancedb"
    db = await lancedb.connect_async(uri)
    tbl = await db.create_table("my_text", data=data, mode="overwrite")

    await tbl.create_index("text", config=FTS(language="English"))

    response = await tbl.search("spanish", query_type="fts")
    result = await response.limit(1).to_polars()
    print(result)
    return result

if __name__ == "__main__":
    asyncio.run(main(data))
```

The create_fts_index method is not available on AsyncTable. Use create_index with FTS config instead.

## Configuration Options

### FTS Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| with_position | bool | False | Store token positions (required for phrase queries) |
| base_tokenizer | str | "simple" | Text splitting method (simple, whitespace, or raw) |
| language | str | "English" | Language for stemming/stop words |
| max_token_length | int | 40 | Maximum token size; longer tokens are omitted |
| lower_case | bool | True | Lowercase tokens |
| stem | bool | True | Apply stemming (running → run) |
| remove_stop_words | bool | True | Drop common stop words |
| ascii_folding | bool | True | Normalize accented characters |
| custom_stop_words | list[str] | None | Extra stop words to drop in addition to the language defaults. Requires remove_stop_words=True. |
| min_ngram_length | int | 3 | Minimum n-gram length. Applies only when base_tokenizer="ngram". |
| max_ngram_length | int | 3 | Maximum n-gram length. Applies only when base_tokenizer="ngram". |
| prefix_only | bool | False | Index only prefix n-grams rather than all substrings. Applies only when base_tokenizer="ngram". |

max_token_length can filter out base64 blobs or long URLs.
Disabling with_position reduces index size but disables phrase queries.
ascii_folding helps with international text (e.g., "café" → "cafe").

### Phrase Query Configuration

Enable phrase queries by setting:

| Parameter | Required Value | Purpose |
|---|---|---|
| with_position | True | Track token positions for phrase matching |
| remove_stop_words | False | Preserve stop words for exact phrase matching |
