---
name: sdk-ops
description: "Use this skill when provisioning and operating infrastructure with the ops CLI - VPS provisioning, k3s clusters, datastores, backups, and firewall rules from YAML."
---

# Ops CLI

A CLI for provisioning and operating servers and clusters **from YAML**: bring up
hosts, install services, run backups and restores, and manage firewall rules.

## What you get

- Idempotent provisioning of a fleet of nodes.
- Cluster setup (k3s) and bare-metal/dockerized service variants.
- Datastores: PostgreSQL, Redis-compatible, NATS, etcd.
- Backup and restore to S3.
- Firewall allow-lists and peer routes.

## Conventions

- One YAML describes nodes and services.
- Services not declared are cleaned up on the next run.
- Credentials live per host, never in the repo.

## References

- `references/provisioning.md`
- `references/clusters.md`
- `references/datastores.md`
- `references/backups.md`
- `references/firewall.md`
