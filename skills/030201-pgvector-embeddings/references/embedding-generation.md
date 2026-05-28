# Embedding Generation

## OpenAI embedding

```typescript
import { OPENAI_API_KEY } from "@/app/lib/env"

export async function generateEmbedding(text: string): Promise<number[]> {
  if (!OPENAI_API_KEY) {
    // Deterministic fallback for dev
    return generateHashEmbedding(text)
  }
  const res = await fetch("https://api.openai.com/v1/embeddings", {
    method: "POST",
    headers: { Authorization: `Bearer ${OPENAI_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ model: "text-embedding-3-small", input: text.slice(0, 8000) }),
  })
  const data = await res.json() as { data: Array<{ embedding: number[] }> }
  return data.data[0].embedding
}
```

## Deterministic hash fallback

```typescript
export function generateHashEmbedding(text: string, dim = 384): number[] {
  const nums: number[] = []
  for (let i = 0; i < dim; i++) {
    let h = i * 31
    for (let j = 0; j < text.length; j++) {
      h = (h << 5) - h + text.charCodeAt(j)
      h |= 0
    }
    nums.push(((h % 2000) - 1000) / 1000)
  }
  return nums
}
```
