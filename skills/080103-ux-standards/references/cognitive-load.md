# Cognitive Load Reference

Deep reference for cognitive load principles: information density, chunking, progressive disclosure, visual noise reduction, and decision fatigue avoidance.

---

## What is Cognitive Load?

Cognitive load is the amount of mental effort being used in working memory. In UX, the goal is to minimize **extraneous cognitive load** — mental effort spent on understanding the interface rather than accomplishing the task.

### Three Types

| Type | Definition | UX Example |
|---|---|---|
| **Intrinsic** | Inherent complexity of the task | Filling out a tax form — there's no way to make this cognitively "easy" |
| **Extraneous** | Unnecessary mental effort imposed by bad design | A confusing layout, inconsistent labels, hidden features |
| **Germane** | Mental effort spent on learning and schema formation | First-time setup flow that teaches the product |

### Goal
- Minimize extraneous load
- Manage intrinsic load with chunking and progressive disclosure
- Support germane load with clear onboarding and patterns

---

## Information Density

### Optimal Density
- White space is not wasted space — it defines visual boundaries
- 40–60 characters per line for comfortable reading (web)
- 12–20 words per sentence maximum
- 3–5 bullet points per list before it needs sub-grouping

### Scannability Hierarchy
```
1. Heading (catch attention, summarize section)
2. Subheading (clarify what follows)
3. Bold key terms (for scanners)
4. Body text (read when needed)
```

### Text Density Guidelines
| Context | Words per Screen | Notes |
|---|---|---|
| Onboarding / first run | < 30 | No one reads walls of text when they want to start |
| Settings / configuration | < 100 | Group into sections |
| Data-heavy dashboards | < 50 text + metrics | Numbers are scannable, prose is not |
| Error / empty states | < 20 | Short + actionable |
| Confirmation dialogs | < 30 | Just enough to confirm the decision |

### Visual Density Guidelines
- Card/panel contents: max 10–12 items before needing categorization
- Tables: 5–7 columns max (beyond that, scroll or summarize)
- Navigation: 5–7 items per level max (Miller's Law)
- Dropdown menus: 8–10 items max (beyond that, add search or categories)

---

## Chunking

### The Magic Number 7±2
- Working memory can hold about 5–9 items at once
- Chunking groups items into meaningful units
- Phone numbers are chunked: "415-555-0192" not "4155550192"

### Chunking Strategies

| Technique | Before | After |
|---|---|---|
| Group by category | 20 settings in one list | General / Notifications / Privacy / Security |
| Group by step | One big form | Step 1: Account / Step 2: Profile / Step 3: Payment |
| Group by frequency | All features visible | Most used / Advanced / Hidden in Settings |
| Progressive disclosure | Full form visible on load | Show basic fields, "Show advanced options" link |

### Visual Chunking with CSS
```css
/* Group related fields with background + border */
.fieldset-group {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.fieldset-group legend {
  font-weight: 600;
  margin-bottom: 12px;
}
```

---

## Progressive Disclosure

### Principles
1. Show the most common/important options by default
2. Reveal advanced options on demand
3. Never hide critical or frequently used features

### Implementation Patterns

**Show/Hide Section:**
```html
<details class="advanced-section">
  <summary class="advanced-toggle">Advanced display settings</summary>
  <div class="advanced-content">
    <label for="dpi">DPI override</label>
    <input id="dpi" type="number" />
    <label for="refresh">Refresh rate</label>
    <select id="refresh">
      <option>60Hz (default)</option>
      <option>120Hz</option>
    </select>
  </div>
</details>
```

**Progressive Steps:**
```ts
// Only show shipping fields after user selects a shipping method
function StepCheckout() {
  const [step, setStep] = useState<'method' | 'address' | 'payment'>('method');

  return (
    <div>
      {step === 'method' && <ShippingMethod onSelect={() => setStep('address')} />}
      {step === 'address' && <ShippingAddress onNext={() => setStep('payment')} />}
      {step === 'payment' && <PaymentDetails />}
    </div>
  );
}
```

**"Show more" pattern:**
```html
<button aria-expanded="false" aria-controls="additional-filters">
  More filters (3)
</button>
<div id="additional-filters" hidden>
  <!-- Hidden until expanded -->
</div>
```

---

## Visual Noise Reduction

### Remove What Isn't Needed
Ask of every UI element:
- Does this help the user accomplish their current goal?
- Does this inform a decision the user needs to make?
- Does this reduce confusion?

If the answer to all three is "no", remove it or relegate it to a secondary space.

### Common Noise Sources

| Source | Fix |
|---|---|
| Decorative illustrations on functional pages | Remove or move to empty states |
| Multiple divider lines | Use white space instead of lines |
| Excessive color (more than 3-4 UI colors) | Use a single accent + neutral palette |
| Redundant labels (heading + paragraph saying the same thing) | Remove the paragraph |
| Icons next to every item (stock table, settings) | Only add icons that aid recognition |
| Animations that run after initial load | Disable or limit to hover/interaction |
| Border-heavy cards | Use flat cards with background, not borders |

### The Squint Test
Half-close your eyes and look at the screen:
1. Can you identify the primary action?
2. Can you distinguish different sections?
3. Are irrelevant elements invisible (good!) or competing for attention (bad)?

---

## Decision Fatigue

### Reduce Choice Count
- Hick's Law: time to make a decision increases logarithmically with the number of choices
- Limit choices per screen: 3–5 significant decisions maximum
- Exceptions: product catalogs, content feeds — provide filters/CTAs instead of reducing inventory

### Pre-select Smart Defaults
```ts
// Default settings that match 80%+ of users
const defaults = {
  language: navigator.language,
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
  notifications: {
    email: true,        // most users want email confirmation
    push: false,         // many users disable push initially
    sms: false,          // high friction, opt-in only
  },
};
```

### Defaults Guidelines
- Smart defaults based on context (not just "first option")
- Never pre-select dangerous options (agree to marketing emails, share data)
- Show a "Restore defaults" option for complex settings
- If the default is privacy-invasive, make it opt-in (not opt-out)

### Decision Sequencing
- Present related decisions together (address fields in one section)
- Present unrelated decisions on separate screens/steps
- Complex decision first (most important), simple ones after

---

## Hick's Law in Practice

### Navigation
```
✗ Bad: 12 items in main navigation (overwhelming)
✓ Good: 5 primary items + "More" menu with the rest
```

### Settings
```
✗ Bad: 40 settings in one flat list
✓ Good: 5 sections of 8 settings each
```

### Onboarding
```
✗ Bad: "Choose your preferences" with 15 checkboxes
✓ Good: 3-step onboarding: "What do you want to do?" → 4 options → context-relevant setup
```

---

## Memory & Recognition

### Recognition over Recall
- Users should **recognize** what to do, not **recall** how to do it
- Show options rather than asking users to remember and type

```
✗ Recall: "Enter your timezone" (user must know the timezone name)
✓ Recognition: Select "Pacific Time (UTC-8)" from a dropdown
```

### Reducing Short-Term Memory Load
- Keep important information visible during the task:
  - Cart total visible while entering payment
  - Selected filters visible when browsing results
  - Current step visible in multi-step forms
- Avoid forcing users to remember information from one step to the next
- Use autocomplete and suggestion lists instead of free-form text

---

## Cognitive Load Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Password confirmation field | Forces user to re-type (memory load + frustration) | Show password toggle + "Forgot password?" link |
| Reset filters instead of preserving | User must rebuild their view | Preserve filters across session | 
| Infinite scroll with no way to bookmark position | User loses context on refresh | Add pagination or "Save position" |
| Modal in modal | User loses track of navigation context | Use push navigation or stacked modals carefully |
| Tooltip for critical information | User must remember tooltip content | Show information inline |
| Multiple CTAs of equal visual weight | User doesn't know what to do first | One primary CTA, clearly stronger visual |

---

## Information Architecture & Cognitive Load

### Flat vs Deep IA
- Flat (all items at top level): wider but more choices per screen — Hick's Law penalty
- Deep (nested categories): fewer choices per screen — but users must navigate more levels

**Balance:**
- 3–5 top-level categories
- 2–3 levels deep maximum
- Each level: 5–7 items ideal

### Contextual Navigation
- Show contextual actions near the relevant content, not in a global toolbar
- Example: "Edit" button on the product itself, not in a universal toolbar

---

## Measuring Cognitive Load

### Self-Report Methods
- NASA-TLX (Task Load Index): standardized questionnaire after task completion
- Single Ease Question (SEQ): "Overall, how difficult was this task?" (1-7)

### Behavioral Metrics
- Task completion time (longer = higher load)
- Error rate (more errors = higher load)
- Click/scroll count before action (more navigation = confusion)
- Number of times user reverses an action (redo, undo, back-button clicks)

---

## Accessibility & Cognitive Load

### For Users with Cognitive Disabilities
- Avoid time limits (allow extending or disabling)
- Clear, simple language (no idioms, metaphors, or unnecessary wordplay)
- Consistent navigation and layout across all pages
- Predictable behavior (same interaction = same result everywhere)
- Error messages: simple, specific, suggest a fix
- Provide summaries of long content
- Use icons consistently and with labels (not icon-only or symbolic-only)

### Reduce Cognitive Load for All Users
- Consistent placement of common elements (search, nav, back)
- Familiar patterns (shopping cart icon → cart, gear icon → settings)
- Avoid surprising users with auto-advancing or auto-submitting forms
- Clear visual hierarchy reduces scanning effort
