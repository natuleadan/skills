---
name: 040101-docker-deploy
description: Docker deployment patterns for web applications — multi-stage builds, environment management, CI/CD integration, and self-hosting strategies.
---

# Docker Deployment Patterns

Docker deployment patterns for web applications: multi-stage builds, environment management, CI/CD integration, and security hardening.

## References

| Topic | File |
|---|---|
| When to use Docker, architecture diagram | [references/use-cases.md](references/use-cases.md) |
| Multi-stage Dockerfile, .dockerignore, CI/CD YAML, security hardening, quick commands | [references/dockerfile-reference.md](references/dockerfile-reference.md) |
| Multi-stage build patterns, environment variable management, compose recipes, health checks | [references/docker-patterns.md](references/docker-patterns.md) |

## When to Use

- Self-hosting or on-premise deployment
- Staging that mirrors production
- Development without cloud services
- Fallback when primary hosting is unavailable
