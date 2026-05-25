# Realtime Patterns Lesson

Realtime enables live subscriptions. Choose broadcast or postgres_changes based on needs.

## Broadcast vs Postgres_changes

| Feature | Broadcast | Postgres_changes |
|---------|-----------|------------------|
| **Best For** | High-frequency events (cursors, game state) | Real DB changes needing persistence |
| **WAL** | Bypasses WAL | Uses WAL |
| **Scalability** | Better (high-frequency) | Limited (scaling issues at high frequency) |
| **Payload** | JSON supported | DB change data |
| **Persistence** | Transient | Persisted |

**Rule:** Default to **broadcast** for UI updates. Use **postgres_changes** only when you need WAL/audit trail.

## Channel Naming

Use hierarchical naming: `scope:entity:id`

- `room:chat:123` — room 123 chat channel
- `user:profile:456` — user 456 profile updates
- `game:state:789` — game state

## Private Channels

Enforce authorization via channel RLS:

```typescript
const channel = supabase.channel('room:123', {
  config: { private: true }
})
.on('broadcast', { event: 'msg' }, (payload) => console.log(payload))
.subscribe()
```

## Database Triggers for Broadcast

Instead of client `postgres_changes`, use trigger to call `realtime.broadcast_changes`:

```sql
create trigger notify_room_changes
after update on rooms
for each row
execute function realtime.broadcast_changes()
```

## Rules

- [ ] **Favor broadcast** for high-frequency updates
- [ ] **Postgres_changes** only for audit/persistence needs
- [ ] **Private channels** for authorization
- [ ] **Hierarchical naming** for channels
- [ ] **Database triggers** for controlled broadcast
