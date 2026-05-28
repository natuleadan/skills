#!/usr/bin/env python3
"""Generate a deterministic 384-dim vector from text (hash-based, no API needed)."""
import hashlib

def generate_embedding(text: str, dimensions: int = 384) -> list[float]:
    nums = []
    for i in range(dimensions):
        h = hashlib.sha256(f"{text}:{i}".encode()).hexdigest()
        nums.append((int(h[:8], 16) % 2000 - 1000) / 1000)
    return nums

if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) > 1 else "default text"
    vec = generate_embedding(text)
    print(f"[{','.join(f'{v:.4f}' for v in vec[:5])}, ...] ({len(vec)} dims)")
