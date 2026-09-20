---
name: platform
description: "Use this skill when working with the platform APIs — agents, robots and toolsets, how they are called, authenticated, scheduled, and when a human must confirm."
---

# Platform

How to work with the platform APIs: the service categories, how a call flows,
authentication, scheduling, and human-in-the-loop.

> Status: early. This skill describes what already exists; sections expand as the
> platform evolves.

## Service categories

| Category | What it is | How you call it |
|---|---|---|
| **Agent** | Consumes a toolset and performs tasks | by its slug |
| **Toolset** | A bundle of tools invoked together (code `XXX-P01`) | tool call per capability |
| **Robot** | Physical automation (code `XXX-R01`, area prefix) | by its slug |

## How a call flows

A request enters the API, the agent resolves the toolset, the tool runs, and the
result is returned. Long operations return a job handle to poll.

## Authentication

- API key or OAuth 2.1 for robots.
- The caller identity determines which agents and tools are reachable.

## Scheduling

A user books a slot on an agent; the booking becomes a reservation. Availability
is read before booking.

## Human-in-the-loop

Critical operations require a human to confirm before they run. HIL is triggered
by the operation type, not by the caller.

## References

- `references/agent-types.md` — categories and how each is addressed
- `references/api-usage.md` — request flow, jobs, and errors
- `references/scheduling.md` — bookings and availability
- `references/hil.md` — human-in-the-loop rules
