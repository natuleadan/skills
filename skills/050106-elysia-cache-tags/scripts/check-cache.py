#!/usr/bin/env python3
"""Simulate cache tag state (no external deps)."""
from typing import Dict, List, Optional, Set

class CacheTags:
    def __init__(self):
        self._store: Dict[str, str] = {}
        self._tags: Dict[str, Set[str]] = {}

    def set(self, key: str, value: str, tags: List[str], ttl: int = 30):
        self._store[key] = value
        for tag in tags:
            self._tags.setdefault(tag, set()).add(key)

    def get(self, key: str) -> Optional[str]:
        return self._store.get(key)

    def invalidate(self, tag: str) -> List[str]:
        members = list(self._tags.pop(tag, set()))
        for k in members:
            self._store.pop(k, None)
        return members

    def flush(self):
        self._store.clear()
        self._tags.clear()

if __name__ == "__main__":
    c = CacheTags()
    c.set("products:all", "[product data]", ["cache:tags:products", "cache:tags:cross:catalog"])
    c.set("product:123", "{product detail}", ["cache:tags:products:123"])
    print("Before:", len(c._store), "keys")
    removed = c.invalidate("cache:tags:products")
    print("After invalidate 'products':", len(c._store), "keys, removed:", removed)
