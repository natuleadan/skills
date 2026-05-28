# Service Dual-Mode: index.ts + test.ts

## Purpose

Pair a production service (`index.ts` using `sys_*` or `prd_*` tables) with a test variant (`test.ts` using `tst_*` tables). Both instantiate the same domain factory.

## Structure

```
service/{module}/
├── index.ts    ← Production: instantiates factory with sys_* tables
└── test.ts     ← Test: instantiates factory with tst_* tables
```

## Example

```typescript
// service/push/index.ts (production)
import { sysPushSubscriptions } from "@/app/db/schema/sys/push"
import { createPushRepo } from "@/app/lib/domain/push/repo"
const pushRepo = createPushRepo({ subscriptions: sysPushSubscriptions })

// service/push/test.ts (test helpers)
import { testPushSubscriptions } from "@/app/db/schema/test/push"
import { createPushRepo } from "@/app/lib/domain/push/repo"
const pushRepo = createPushRepo({ subscriptions: testPushSubscriptions })
```

## When to use

Any module that needs to run the same logic against both test (`tst_*`) and system (`sys_*`) tables. Common domains: cron jobs, push notifications, webhooks, storage.
