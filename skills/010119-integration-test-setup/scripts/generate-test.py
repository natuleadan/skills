#!/usr/bin/env python3
"""Generate an integration test boilerplate."""
import sys

TEMPLATE = '''import {{ beforeAll, describe, expect, test }} from "bun:test"
import {{ Pool }} from "pg"
import {{ getAuthHeaders }} from "../../helpers/auth"
import {{ describeIf, IS_PROD }} from "../../helpers/skip-in-prod"

const HOST = "http://localhost:3400"
let cookie = ""

async function req(method: string, path: string, body?: unknown, useCookie = true) {{
  const headers: Record<string, string> = {{ "content-type": "application/json" }}
  if (useCookie) {{
    headers["cookie"] = cookie
  }}
  const opts: RequestInit = {{ method, headers }}
  if (body) {{
    opts.body = JSON.stringify(body)
  }}
  const res = await fetch(`${{HOST}}${{path}}`, opts)
  const data = await (async () => {{ try {{ return await res.json() }} catch {{ return null }} }})()
  return {{ status: res.status, data }}
}}

describeIf(!IS_PROD, "{name} CRUD", () => {{
  beforeAll(async () => {{
    const pool = new Pool({{ connectionString: process.env.DATABASE_URL! }})
    await pool.query("DELETE FROM prd_products WHERE name LIKE 'test-%'")
    await pool.end()
    const auth = await getAuthHeaders("products:editor")
    cookie = auth.cookie
  }})

  test("POST creates item", async () => {{
    const {{ data }} = await req("POST", "/v1/{endpoint}", {{ name: "test-item", price: 10 }})
    expect(data?.code).toBe(1)
  }})
}})
'''

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Products"
    endpoint = sys.argv[2] if len(sys.argv) > 2 else "products"
    print(TEMPLATE.format(name=name, endpoint=endpoint))
