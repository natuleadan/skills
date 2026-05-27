# Organization Plugin

Better Auth includes an organization plugin for multi-tenant setups. Users can belong to multiple organizations with different roles per org.

## Server Config

```typescript
import { betterAuth } from "better-auth"
import { organization } from "better-auth/plugins"
import { createAccessControl } from "better-auth/plugins/access"
import { adminAc } from "better-auth/plugins/admin/access"

const ac = createAccessControl({ ... })
const roles = {
  owner: ac.newRole({ ...adminAc.statements, organization: ["create", "read", "update", "delete"] }),
  admin: ac.newRole({ ...adminAc.statements, organization: ["read", "update"] }),
  member: ac.newRole({ products: ["read"] }),
}

export const auth = betterAuth({
  plugins: [
    organization({
      ac,
      roles,
      allowUserToCreateOrganization: true,
      organizationLimit: 3,
      invitationExpiresIn: 48 * 60 * 60,
      teams: { enabled: true, maximumTeams: 10 },
      dynamicAccessControl: { enabled: true },
      async sendInvitationEmail(data) {
        const link = `https://example.com/accept-invitation/${data.id}`
        // Send via email service
      },
    }),
  ],
})
```

## Client Config

```typescript
import { createAuthClient } from "better-auth/react"
import { organizationClient } from "better-auth/client/plugins"
import { ac, roles } from "./org-permissions"

export const authClient = createAuthClient({
  baseURL: "http://localhost:3000",
  plugins: [
    organizationClient({ ac, roles, dynamicAccessControl: { enabled: true } }),
  ],
})
```

## Key Concepts

- Three org roles: `owner` (full control), `admin` (almost full), `member` (read-only)
- Custom roles via Dynamic Access Control — any role name with granular permissions
- Teams are member groupings within orgs (no team-level roles)
- Invitations flow: invite by email -> user clicks link -> accepts/rejects -> becomes member

## CSRF Protection

Endpoints like `create`, `set-active`, `invite-member` require the `Origin` header. For server-to-server calls, inject it:

```typescript
function withOrigin(headers?: Headers): Headers {
  const h = headers ?? new Headers()
  if (!h.has("origin")) h.set("origin", "http://localhost:3000")
  return h
}

await auth.api.createOrganization({ body, headers: withOrigin(headers) })
```

## Lifecycle Hooks

~30 hooks for before/after operations: `beforeCreateOrganization`, `afterAddMember`, `beforeDeleteTeam`, `afterRemoveTeamMember`, etc. `before*` hooks return `{ data: modifiedData }` to transform input.

## Direct Add vs Invitation

- **Invitation** (`inviteMember`): sends email, user must accept
- **Direct add** (`addMember`, server-only): adds existing user immediately, no email
