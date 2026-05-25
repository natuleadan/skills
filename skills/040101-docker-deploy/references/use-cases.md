# Docker Use Cases & Architecture

## When to Use Docker

- Self-hosting or on-premise deployment
- Air-gapped environments without cloud access
- Staging that mirrors production infrastructure
- Development environments without cloud services
- Fallback when primary hosting platform is unavailable

## Architecture

```
Git push → CI Pipeline
  ├── Install dependencies
  ├── Lint + test
  ├── Build application
  └── Compile production artifacts

Docker build
  ├── Dockerfile (multi-stage: deps → builder → runner)
  └── docker compose up -d (production)
```
