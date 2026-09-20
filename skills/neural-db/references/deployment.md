# Deployment

> Stub — expanded as the engine evolves.

## Distribution

- Per-version archives (Linux amd64, macOS arm64).
- Container image for server deployments.

## Notes

- Build it and run it as its own service.
- GPU acceleration is planned; CPU works today.

## Flow

```mermaid
sequenceDiagram
    participant Build
    participant Archive
    participant Runtime
    Build->>Archive: request
    Archive->>Runtime: process
    Runtime-->>Archive: result
    Archive-->>Build: response
```
