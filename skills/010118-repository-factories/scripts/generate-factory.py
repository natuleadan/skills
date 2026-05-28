#!/usr/bin/env python3
"""Generate a domain repository factory boilerplate."""
import sys

FACTORY = '''import {{ eq, sql }} from "drizzle-orm"
import type {{ AnyPgTable }} from "drizzle-orm/pg-core"
import {{ db }} from "@/app/lib/infra/db"

type {name}Table = AnyPgTable & {{
  id: any
  name: any
  createdAt: any
}}

export function create{name}Repo(table: {name}Table) {{
  return {{
    async list() {{
      return db.select().from(table).orderBy(sql`${{table.createdAt}} desc`)
    }},
    async getById(id: string) {{
      const [row] = await db.select().from(table).where(eq(table.id, id)).limit(1)
      return row ?? null
    }},
    async create(data: Record<string, unknown>) {{
      const [row] = await db.insert(table).values(data as any).returning()
      return row
    }},
    async update(id: string, data: Record<string, unknown>) {{
      const [row] = await db.update(table).set(data as any).where(eq(table.id, id)).returning()
      return row ?? null
    }},
    async remove(id: string) {{
      const [row] = await db.delete(table).where(eq(table.id, id)).returning()
      return row ?? null
    }},
  }}
}}
'''

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Example"
    print(FACTORY.format(name=name))
