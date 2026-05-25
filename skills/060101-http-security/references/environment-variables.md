# Environment Variables

## Required Variables

### Database

- `DATABASE_URL` — Database connection string
  - Format: `postgresql://user:password@host:port/database`
  - Never commit connection strings containing credentials

### Authentication

- `AUTH_SECRET` — Secret for signing auth tokens
  - Generate with: `openssl rand -base64 32`
  - Must be 32+ characters
  - Rotate periodically

- `AUTH_URL` — Application URL for auth redirects
  - Development: `http://localhost:3000`
  - Production: `https://your-domain.com`

## Optional Variables

- `PUBLIC_APP_URL` — Public app URL for client-side access
- `NODE_ENV` — Environment (`development`, `production`, `test`)
- `COOKIE_SECRET` — Cookie signing secret (generate with `openssl rand -base64 32`)
- `CSP_SCRIPT_SRC_DOMAINS`, `CSP_STYLE_SRC_DOMAINS`, etc. — Content Security Policy domains

## Variable Access Rules

- Server-side: `process.env.VARIABLE_NAME`
- Client-side: Only variables prefixed with `NEXT_PUBLIC_` or equivalent public prefix
- Build-time: Environment variables needed at build time must be available during compilation
- Runtime: Variables not marked as build-time are only needed at runtime

## Security Rules

- Never commit `.env` to version control
- Add `.env`, `.env.local`, `.env.*.local` to `.gitignore`
- Use different values for development vs production
- Generate secrets with `openssl rand -base64 32` (never reuse)
- Rotate secrets periodically (especially auth and encryption keys)
- Verify `.env` is in `.gitignore` before first commit

## Environment-Specific Files

- `.env` — Local development (gitignored)
- `.env.local` — Overrides `.env` (gitignored, never commit)
- `.env.production` — Production overrides (gitignored)
- `.env.example` — Template file without real values (committed to repo)

## Setup Checklist

- Create `.env` file in project root
- Add `DATABASE_URL` with valid connection string
- Generate and add `AUTH_SECRET`
- Set `AUTH_URL` to correct environment URL
- Verify `.env` is in `.gitignore`
- Create `.env.example` as a template for other developers
