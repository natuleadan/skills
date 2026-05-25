# Form UX Reference

Deep reference for form design patterns: labels, validation, error recovery, progressive disclosure, multi-step flows, autofill, and keyboard support.

---

## Labels & Structure

### Label Visibility Rules
| Label Style | Valid? | Notes |
|---|---|---|
| Always-visible top label | ✓ Best | Most scannable |
| Always-visible left label | ✓ | For desktop with wide forms |
| Floating label | ✓ Acceptable | Implement correctly (label animates up on focus/fill, never disappears) |
| Placeholder-only | ✗ Fails WCAG | Disappears on input, bad for memory |
| Icon-only | ✗ | Needs visible label for WCAG |

```html
<!-- Top label (preferred) -->
<div class="field">
  <label for="email">Email</label>
  <input id="email" type="email" autocomplete="email" />
</div>

<!-- Floating label (acceptable when implemented correctly) -->
<div class="floating-field">
  <input id="email" type="email" placeholder=" " autocomplete="email" />
  <label for="email">Email</label>
</div>
```

```css
/* Floating label CSS */
.floating-field {
  position: relative;
}
.floating-field label {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  transition: all 0.15s ease;
  pointer-events: none;
  color: var(--color-label);
}
.floating-field input:focus + label,
.floating-field input:not(:placeholder-shown) + label {
  top: 0;
  transform: translateY(0);
  font-size: 0.75em;
}
```

### Required vs Optional
- Mark required fields with `*` (asterisk)
- Include a legend at the top of the form: "Fields marked * are required"
- If most fields are required, mark optional fields with "(optional)" instead

### Helper Text
- Persistent below the field (not in a tooltip) for complex inputs
- Associates via `aria-describedby`
- Disappears on valid input? Only if it was instructional placeholder text

---

## Validation

### Timing

| Approach | Best For | Avoid |
|---|---|---|
| On blur | Most forms | Password fields (UX friction during typing) |
| On submit | Simple forms | Complex forms (too much error at once) |
| Live (on keypress) | Character counters, password strength | Email/URL validation |
| On focus | N/A — just preparation | Acting on empty field |

### Inline Validation Pattern

```tsx
function EmailField() {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');
  const [touched, setTouched] = useState(false);

  const validateEmail = (v: string) => {
    if (!v) return 'Email is required';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) {
      return 'Enter a valid email address (e.g., user@example.com)';
    }
    return '';
  };

  const handleBlur = () => {
    setTouched(true);
    setError(validateEmail(value));
  };

  return (
    <div className="field">
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onBlur={handleBlur}
        aria-invalid={!!error && touched}
        aria-describedby={error ? 'email-error' : undefined}
        autoComplete="email"
      />
      {error && touched && (
        <p id="email-error" className="field-error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
```

### Error Message Patterns

| Bad | Good |
|---|---|
| "Invalid input" | "Enter a valid email address (e.g., user@example.com)" |
| "Required" | "Password is required for this account" |
| "Error" | "Couldn't save changes. Check your connection and try again." |
| "Field must be between 3-50 characters" | "Username must be 3-50 characters" |
| "Invalid password" | "Password must include at least 8 characters, one uppercase letter, and one number" |

### Error Summary (Accessibility)
```html
<div role="alert" aria-live="assertive" class="error-summary" tabindex="-1">
  <h2>3 errors found</h2>
  <ul>
    <li><a href="#email">Enter a valid email address</a></li>
    <li><a href="#password">Password must be at least 8 characters</a></li>
    <li><a href="#terms">You must accept the terms</a></li>
  </ul>
</div>
```

### Focus Management on Error
- After form submission fails, focus the first error summary (if present) or the first invalid field
- Each error link in the summary scrolls to and focuses the associated field

---

## Input Types & Keyboard

### Semantic Input Types

```html
<!-- Text -->
<input type="text" inputmode="text" autocomplete="given-name" />

<!-- Email -->
<input type="email" inputmode="email" autocomplete="email" />

<!-- Phone -->
<input type="tel" inputmode="tel" autocomplete="tel" />

<!-- Number (with numeric keypad on mobile) -->
<input type="number" inputmode="numeric" pattern="[0-9]*" autocomplete="cc-number" />

<!-- URL -->
<input type="url" inputmode="url" autocomplete="url" />

<!-- Search -->
<input type="search" inputmode="search" autocomplete="search" />

<!-- Date -->
<input type="date" autocomplete="bday" />

<!-- Password -->
<input type="password" autocomplete="new-password" />
<input type="password" autocomplete="current-password" />
```

### Autocomplete Attributes
```html
<!-- Personal -->
autocomplete="name"         <!-- Full name -->
autocomplete="given-name"   <!-- First name -->
autocomplete="family-name"  <!-- Last name -->
autocomplete="email"
autocomplete="tel"
autocomplete="street-address"
autocomplete="postal-code"
autocomplete="country-name"

<!-- Account -->
autocomplete="username"
autocomplete="current-password"
autocomplete="new-password"
autocomplete="one-time-code"

<!-- Payment -->
autocomplete="cc-name"
autocomplete="cc-number"
autocomplete="cc-exp"
autocomplete="cc-csc"

<!-- Other -->
autocomplete="organization"
autocomplete="url"
autocomplete="language"
autocomplete="bday"
```

---

## Submit & Feedback States

### Button States
```tsx
function SubmitButton({ loading, success, error }: {
  loading: boolean;
  success: boolean;
  error: string | null;
}) {
  if (loading) {
    return (
      <button disabled aria-busy="true" type="submit">
        <span class="spinner" aria-hidden="true"></span>
        Saving…
      </button>
    );
  }

  if (success) {
    return (
      <button disabled type="submit" class="btn-success">
        ✓ Saved
      </button>
    );
  }

  return (
    <button type="submit">
      Save changes
    </button>
  );

  // Error is displayed as a persistent alert below the form or near the button
}
```

### Transition Flow
```
Idle → Click → Loading (button disabled + spinner) → Success (checkmark + toast)
                                                → Error (alert near button, button re-enabled)
```

---

## Confirmation & Destructive Actions

### Confirmation Dialogs
```html
<div role="alertdialog" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Delete workspace "Acme"</h2>
  <p id="dialog-desc">
    This action cannot be undone. All projects, files, and settings will be permanently deleted.
  </p>
  <div class="dialog-actions">
    <button type="button" autofocus>Cancel</button>
    <button type="button" class="btn-danger">Delete workspace</button>
  </div>
</div>
```

### Principles
1. Specify exactly WHAT will be deleted/changed
2. Specify the scope (workspace, file, 3 items, etc.)
3. State if the action is reversible or permanent
4. Use explicit verb in the confirm button (not "OK" or "Confirm")
5. Include a non-destructive escape: Cancel or X

### Undo Actions
- Show undos as toasts with an action button:
```
Item deleted                [Undo]
```
- Time window: 5–10 seconds
- Clear on dismiss or manual undo

---

## Multi-Step Forms

### Progress Indicator
```html
<nav aria-label="Form progress" role="progressbar" aria-valuenow="2" aria-valuemin="1" aria-valuemax="4">
  <ol class="steps">
    <li class="step completed">
      <span class="step-number" aria-hidden="true">✓</span>
      <span class="step-label">Account</span>
    </li>
    <li class="step current" aria-current="step">
      <span class="step-number" aria-hidden="true">2</span>
      <span class="step-label">Profile</span>
    </li>
    <li class="step">
      <span class="step-number" aria-hidden="true">3</span>
      <span class="step-label">Payment</span>
    </li>
    <li class="step">
      <span class="step-number" aria-hidden="true">4</span>
      <span class="step-label">Confirm</span>
    </li>
  </ol>
</nav>
```

### Back Navigation
- Back button returns to previous step preserving all entered data
- Do not clear form state on back
- Forward navigation validates current step before proceeding

### Autosave
```ts
function useAutosave(data: unknown, delay = 3000) {
  const timerRef = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      saveDraft(data); // POST /api/drafts
    }, delay);
    return () => clearTimeout(timerRef.current);
  }, [data, delay]);
}
```

### Sheet Dismiss Confirm
```ts
const hasUnsavedChanges = useMemo(() => {
  return JSON.stringify(formData) !== JSON.stringify(initialData);
}, [formData, initialData]);

function handleSheetClose() {
  if (hasUnsavedChanges) {
    // Show confirmation dialog: "Discard changes?" with Cancel/Discard
  } else {
    closeSheet();
  }
}
```

---

## Progressive Disclosure

### When to Reveal
| Condition | Strategy |
|---|---|
| Optional advanced options | Collapsible section or "Show advanced" toggle |
| Conditional fields (e.g., "Other" with text input) | Show on selecting "Other" |
| Multi-page forms | Step-by-step with progress |
| Complex setting with defaults | Show simple controls, link to "Customize" |

```html
<details>
  <summary>Advanced options</summary>
  <div class="advanced-fields">
    <label for="timezone">Timezone</label>
    <select id="timezone">…</select>
  </div>
</details>
```

---

## Disabled States

```css
input:disabled,
button:disabled,
select:disabled,
textarea:disabled {
  opacity: 0.38; /* Material: 0.38, web typical: 0.4–0.5 */
  cursor: not-allowed;
  pointer-events: none; /* prevents hover/touch interference */
}

/* Ensure disabled elements are still visible enough */
.disabled-field-group {
  opacity: 0.5;
  /* Do not reduce below 0.38 */
}
```

---

## Mobile Form Design

### Touch-Friendly Inputs
```css
input, select, textarea {
  min-height: 44px; /* 48px preferred */
  font-size: 16px; /* Prevents iOS zoom on focus */
  padding: 12px 16px;
}
```

### iOS Zoom Prevention
- Set `font-size: 16px` (or larger) on inputs and selects — iOS auto-zooms if font-size < 16px
- Alternatively use `maximum-scale=1` (with WCAG caveat that this may block pinch zoom)

### Field Grouping
```html
<fieldset>
  <legend>Shipping Address</legend>
  <div class="field-row">
    <div class="field">
      <label for="first-name">First name</label>
      <input id="first-name" autocomplete="given-name" />
    </div>
    <div class="field">
      <label for="last-name">Last name</label>
      <input id="last-name" autocomplete="family-name" />
    </div>
  </div>
  <div class="field">
    <label for="address">Street address</label>
    <input id="address" autocomplete="street-address" />
  </div>
</fieldset>
```

### Input Width & Layout
- Full-width inputs on mobile (match container width)
- Two-column layout only on screens ≥ 600px
- Labels above inputs on mobile, left-aligned labels on desktop when space permits

---

## Form Accessibility Checklist

- [ ] Every input has a visible `<label>` (or `aria-label` for icon-only contexts)
- [ ] Labels use `for` attribute matching input `id`
- [ ] Error messages `role="alert"` or `aria-live="assertive"`
- [ ] Invalid inputs have `aria-invalid="true"`
- [ ] Helper text uses `aria-describedby`
- [ ] Required fields: `required` + `aria-required="true"` + visual `*`
- [ ] Submit button disables on submit + shows loading indicator
- [ ] Error summary at top with anchor links
- [ ] Focus moves to first error on failed submission
- [ ] Input types are semantically correct (`type="email"`, etc.)
- [ ] Autocomplete attributes set for common fields
- [ ] Touch targets ≥ 44px
- [ ] Font size ≥ 16px on mobile inputs
