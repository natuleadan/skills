#!/usr/bin/env python3
"""Generate Drizzle schema boilerplate for a standard table."""
import sys

TEMPLATE = """import { pgTable, text, {extras} } from "drizzle-orm/pg-core"
import { id, slug } from "../_cuid"
import { timestamps } from "../_timestamps"

export const {table} = pgTable("{prefix}_{table}", {{
  id: id(),
  slug: slug(),
  name: text().notNull(),
  ...timestamps,
}})
"""

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "example"
    prefix = sys.argv[2] if len(sys.argv) > 2 else "prd"
    print(TEMPLATE.format(table=name, prefix=prefix, extras=""))
