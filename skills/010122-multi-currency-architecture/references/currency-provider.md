# CurrencyProvider

## React Context

```typescript
const CurrencyContext = createContext<{
  currentCurrency: string
  currentCountry: string
  setCurrency: (code: string | null) => void
} | undefined>(undefined)

export function CurrencyProvider({ children, initialCurrency, initialCountry }) {
  const router = useRouter()
  const [currentCurrency, setCurrentCurrency] = useState(initialCurrency)
  const [currentCountry] = useState(initialCountry)

  const setCurrency = (code: string | null) => {
    if (!code) return
    CookieUtils.setCurrencyCookie(code)
    setCurrentCurrency(code)
    router.refresh() // triggers server re-render with new cookie
  }

  return (
    <CurrencyContext.Provider value={{ currentCurrency, currentCountry, setCurrency }}>
      {children}
    </CurrencyContext.Provider>
  )
}
```

## Cookie persistence

```typescript
function setCurrencyCookie(code: string) {
  document.cookie = `nxt_currency=${code}; path=/; maxAge=${30 * 24 * 60 * 60}; SameSite=Lax`
}
```

## Admin CRUD

Generic admin CRUD via factory:

```typescript
const resources = [
  { name: "currencies", table: currencies, fk: [{ table: "prices", column: "currencyId" }] },
  { name: "countries", table: countries, fk: [{ table: "products", column: "countryId" }] },
  { name: "taxes", table: taxes },
]
```
