# Docker Deployment Patterns Reference

## Multi-Stage Build

Three stages is the standard pattern:

| Stage | Base | Purpose |
|-------|------|---------|
| `deps` | `node:22-alpine` | Install production dependencies |
| `builder` | `node:22-alpine` | Compile/build application |
| `runner` | `node:22-alpine` | Minimal runtime image |

## Environment Variable Management

| Method | Best for | Security |
|--------|----------|----------|
| `.env` file | Local dev | OK — never commit |
| `--env-file` flag | Staging/prod | Good — file on host |
| Orchestrator secrets | Production | Best — encrypted |
| Build args (`--build-arg`) | Build-time config | Poor — visible in image history |

## Docker Compose Production Recipe

```yaml
version: "3.9"
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env.production
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - DAC_OVERRIDE
      - SETUID
      - SETGID
    read_only: true
    tmpfs:
      - /tmp
```

## CI/CD Pipeline Patterns

| Trigger | Action |
|---------|--------|
| Push to `main` | Lint + test + build |
| Tag push (`v*`) | Lint + test + build + push to registry |
| Manual dispatch | Full deploy pipeline |
| PR | Lint + test only (no build) |

## Rollback Strategy

1. Keep previous image tag (`app:prev` or version tag)
2. On failure: `docker compose stop && docker compose up -d` with previous tag
3. For DB-dependent rollbacks, restore from backup first

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

## Logging

```yaml
# docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```
