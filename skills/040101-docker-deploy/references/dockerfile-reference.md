# Dockerfile Reference

## Multi-Stage Dockerfile

```dockerfile
# Stage 1: Dependencies
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Runner (production image)
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## .dockerignore

```
node_modules/
.git/
.env
.env.local
.next/
dist/
*.md
.gitignore
```

## CI/CD Integration

```yaml
# .github/workflows/deploy.yml
name: Docker Deploy
on:
  push:
    tags: ["v*"]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image
        run: docker build -t app:latest .
      - name: Push to registry
        run: |
          docker tag app:latest registry.example.com/app:${{ github.ref_name }}
          docker push registry.example.com/app:${{ github.ref_name }}
```

## Environment Variables

Secrets must never be baked into the image. Use `--env-file` or compose `.env`:

```bash
docker compose --env-file .env.production up -d
```

## Security Hardening

| Measure | Implementation |
|---|---|
| Drop capabilities | `cap_drop: ALL` + add only needed caps |
| No new privileges | `no-new-privileges: true` |
| Read-only root | `read_only: true` (with tmpfs for writable dirs) |
| Non-root user | Create `USER appuser` in Dockerfile |
| Read-only mounts | Mount scripts/configs with `:ro` |

## Quick Reference

```bash
# Build
docker build -t app:latest .

# Run
docker compose up -d

# With env file
docker compose --env-file .env.production up -d

# Stop
docker compose down

# View logs
docker compose logs -f

# Execute command in running container
docker compose exec app sh
```
