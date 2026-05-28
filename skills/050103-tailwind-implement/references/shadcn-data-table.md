# shadcn Data Table with TanStack

Building complex data tables with sorting, filtering, pagination, row selection, column visibility, and row actions using TanStack Table and shadcn/ui Table components.

## Prerequisites

```bash
npm install @tanstack/react-table
```

## Column Definitions

See TanStack docs for `ColumnDef`. Key patterns:

- `accessorKey` — maps to a data property
- `header` — column header renderer (can be sortable)
- `cell` — cell renderer with formatting
- `id` — for action columns without data accessor
- `enableSorting: false` — disable sorting on specific columns
- `enableHiding: false` — prevent column from being hidden

## State Management

Manage 4 UI states with separate `useState` hooks:

- `SortingState` — column sort direction
- `ColumnFiltersState` — filter text per column
- `VisibilityState` — visible/hidden columns
- `RowSelectionState` — selected row IDs

Pass all states to `useReactTable` via the `state` object.

## Rendering

Use `flexRender()` for both header and cell content. The `<Table>` component from shadcn/ui maps directly to TanStack's row model:

- `<TableHeader>` iterates `table.getHeaderGroups()`
- `<TableBody>` iterates `table.getRowModel().rows`
- `<TableHead>` renders `flexRender(header.column.columnDef.header, header.getContext())`
- `<TableCell>` renders `flexRender(cell.column.columnDef.cell, cell.getContext())`

## Empty State

Show "No results." when `table.getRowModel().rows?.length` is falsy.

## Filtering Example

The `getFilteredRowModel()` plugin enables per-column filtering. Connect an `<Input>` to `table.getColumn("email")?.setFilterValue()`.

## Pagination Example

The `getPaginationRowModel()` plugin enables built-in pagination. Use `table.previousPage()`, `table.nextPage()`, `table.getCanPreviousPage()`, `table.getCanNextPage()` for controls.

## Row Selection Example

Add a `Checkbox` column with `id: "select"`. Use `row.getIsSelected()` and `row.toggleSelected()` for individual rows, `table.toggleAllPageRowsSelected()` for select-all.

## Column Visibility Example

Use a `DropdownMenu` with `DropdownMenuCheckboxItem` items that call `column.toggleVisibility()`.
