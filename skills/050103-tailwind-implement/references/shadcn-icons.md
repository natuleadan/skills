# shadcn/ui Icons Reference

## 1. Use the Project's iconLibrary

Detect the project's icon library before writing icon code:

```ts
/* Common icon libraries */
import { IconMail, IconX, IconUser } from "@tabler/icons-react"  /* Tabler — @tabler/icons-react */
import { Mail, X, User } from "lucide-react"                      /* Lucide — lucide-react */
import { FiMail, FiX, FiUser } from "react-icons/fi"             /* Feather — react-icons/fi */
import { IoMdMail, IoMdClose } from "react-icons/io"             /* Ionicons — react-icons/io */
```

**Check `package.json`** for which icon library is installed. Do not assume.

## 2. data-icon Attribute in Buttons

Icons inside buttons use `data-icon` attributes for proper spacing:

```tsx
/* ✅ Leading icon */
<Button>
  <IconMail className="size-4" data-icon="inline-start" />
  Send Email
</Button>

/* ✅ Trailing icon */
<Button>
  Edit
  <IconPencil className="size-4" data-icon="inline-end" />
</Button>

/* ✅ Icon-only button */
<Button size="icon" aria-label="Close">
  <IconX className="size-4" />
</Button>

/* ✅ Loading spinner */
<Button disabled>
  <IconLoader className="size-4 animate-spin" data-icon="inline-start" />
  Saving...
</Button>
```

## 3. No Sizing Classes on Icons Inside Components

Components handle icon sizing via CSS. Do not override:

```tsx
/* ❌ Incorrect */
<Button>
  <IconMail size={24} />        /* size prop overrides component styles */
  Send
</Button>

/* ❌ Incorrect */
<Alert>
  <AlertCircle size={20} />     /* size prop overrides Alert's icon sizing */
  Item not found
</Alert>

/* ✅ Correct */
<Button>
  <IconMail className="size-4" />
  Send
</Button>

/* ✅ Correct */
<Alert>
  <AlertCircle className="size-4" />
  Item not found
</Alert>
```

## 4. Pass Icons as Component Objects, Not String Keys

```tsx
/* ❌ Incorrect — string key */
const menuItems = [
  { icon: "home", label: "Home" },
  { icon: "settings", label: "Settings" },
]

/* ✅ Correct — component reference */
import { IconHome, IconSettings } from "@tabler/icons-react"

const menuItems = [
  { icon: IconHome, label: "Home" },
  { icon: IconSettings, label: "Settings" },
]

/* ✅ Rendering */
{menuItems.map((item) => {
  const Icon = item.icon
  return (
    <button key={item.label} className="flex items-center gap-2">
      <Icon className="size-4" />
      {item.label}
    </button>
  )
})}
```

## 5. No Emoji as Structural Icons

```tsx
/* ❌ Incorrect — emoji as structural icon */
<Button>
  📧 Send Email
</Button>
<div className="flex items-center gap-2">
  🚀 Deploying...
</div>

/* ✅ Correct */
<Button>
  <IconMail className="size-4" />
  Send Email
</Button>
<div className="flex items-center gap-2">
  <IconRocket className="size-4 animate-pulse" />
  Deploying...
</div>
```

Emoji is acceptable only in content areas (user-generated text, markdown content, or casual messaging UI), never in UI chrome, navigation, buttons, or structural component icons.

## 6. Icon Sizing Discipline

Design tokens for icon sizing:

```tsx
/* Size tokens */
<IconMail className="icon-sm" />      /* 16pt — inline with small text */
<IconMail className="size-4" />       /* 16pt — explicit */
<IconMail className="icon-md" />      /* 24pt — default size */
<IconMail className="size-6" />       /* 24pt — explicit */
<IconMail className="icon-lg" />      /* 32pt — large, standalone */

/* Common usage by component */
<Button size="sm"> <IconMail className="size-3.5" /> </Button>  /* 14pt */
<Button size="md"> <IconMail className="size-4" /> </Button>    /* 16pt */
<Button size="lg"> <IconMail className="size-5" /> </Button>    /* 20pt */
<Button size="xl"> <IconMail className="size-5" /> </Button>    /* 20pt */
<Button size="icon"> <IconX className="size-4" /> </Button>     /* 16pt */
<Button size="icon-sm"> <IconX className="size-3.5" /> </Button> /* 14pt */
<Button size="icon-lg"> <IconX className="size-5" /> </Button>  /* 20pt */
```

### Sizing by Context

| Context | Size Token | px |
|---|---|---|
| Small button, inline text | `icon-sm` / `size-3.5` | 14pt |
| Default button, menu items | `size-4` | 16pt |
| Large button, alert icons | `size-5` | 20pt |
| Dialog title icons, feature icons | `icon-md` / `size-6` | 24pt |
| Empty state, hero icons | `icon-lg` / `size-8` | 32pt |
| Page-level illustrations | `size-10` to `size-16` | 40-64pt |

## 7. Stroke Consistency

Icons within the same layer must use the same stroke width:

```tsx
/* ✅ Consistent — same icon library has uniform stroke */
<Button>
  <IconMail className="size-4" />
  <span>Send to</span>
  <IconUser className="size-4" />
  John
</Button>

/* ❌ Inconsistent — mixing feather (1.5px) with material (2px) */
<Button>
  <FiMail className="size-4" />    /* Feather: 1.5px stroke */
  Send
  <IoMdPerson className="size-4" /> /* Ionicons: 2px fill style */
</Button>
```

## 8. Alert Icons

```tsx
/* Match icon to variant */
<Alert variant="destructive">
  <AlertCircle className="size-4" />
  ...
</Alert>

<Alert variant="warning">
  <AlertTriangle className="size-4" />
  ...
</Alert>

<Alert variant="success">
  <IconCircleCheck className="size-4" />
  ...
</Alert>

<Alert variant="info">
  <InfoIcon className="size-4" />
  ...
</Alert>
```

## 9. Form Icon Patterns

```tsx
/* Input prefix icon */
<InputGroup>
  <InputGroupAddon>
    <IconSearch className="size-4" />
  </InputGroupAddon>
  <InputGroupInput placeholder="Search..." />
</InputGroup>

/* Input suffix icon (clear, password toggle) */
<InputGroup>
  <InputGroupInput value="search term" />
  <InputGroupAddon>
    <button onClick={clearSearch} aria-label="Clear search">
      <IconX className="size-4" />
    </button>
  </InputGroupAddon>
</InputGroup>
```
