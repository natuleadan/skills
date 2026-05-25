# Color Strategies — Deep Reference

## The Four-Level Commitment Framework

The commitment axis measures how much surface area the brand color occupies. It is not about saturation, contrast, or number of colors—it is about how much of the viewport is painted in the brand hue.

---

## Restrained

### Pattern
Neutrals tinted toward brand hue + one accent at ≤10% surface coverage. The accent is a tool, not a statement.

### Before/After

**Before (amateur restrained)**
```css
--bg: #ffffff;
--text: #333333;
--accent: #0066ff;
```
Flat neutrals with no hue relationship. The accent is generic blue with no connection to the brand.

**After (intentional restrained)**
```css
--bg: oklch(97% 0.004 260);
--text: oklch(25% 0.012 260);
--accent: oklch(50% 0.18 260);
```
The neutral has a subtle cool tint from the brand hue. The accent shares the same hue. The system is cohesive without shouting.

### When to Escalate to Committed

Escalate when the brand needs to be felt without effort: the user should know they are in your product within one second of landing, even if they are not looking at a logo. Escalate when competitive analysis shows your category defaults to Restrained and you need distinction. Escalate when the product uses color as a primary wayfinding tool (e.g., multi-workspace apps).

### Anti-patterns

- Accent on large areas: hero sections, full-width banners, card backgrounds
- Two accents diluting the single voice
- Gray neutrals with a distinct-hue accent (no relationship between neutral and accent)
- Accent on non-interactive elements (decorative use without purpose)

---

## Committed

### Pattern
One saturated color covering 30–60% of surfaces. The brand color paints navigation, primary sections, and key interactive elements.

### Before/After

**Before (fearful committed)**
```css
--primary: oklch(40% 0.16 260);
--primary-usage: only on buttons
```
Color appears on exactly one element type. The rest of the UI reads as generic.

**After (full committed)**
```css
--color-surface-primary: oklch(45% 0.17 260);
--color-surface-primary-soft: oklch(85% 0.08 260);
--color-text-on-primary: oklch(90% 0.04 260);
--color-border-primary: oklch(50% 0.15 260);
```
The primary hue is present in navigation background, section headers, primary buttons, active tab indicators, and selected states. The product has a clear dominant color identity.

### When to Use Full Palette

Use Full Palette when the product needs multiple distinct color roles for wayfinding: a multi-product suite, a platform with consumer and creator surfaces, an editorial system with sections. Use it when the experience has distinct functional zones that benefit from color coding (red for danger, green for success, blue for information) plus a brand color.

### Anti-patterns

- Visual fatigue from insufficient neutral breathing room
- Primary color on body text or long-form reading surfaces
- Same commitment level applied equally across all surfaces (primary needs to be present but not everywhere)
- Forgetting dark mode: a committed brand color in light mode can become overwhelming in dark mode if not adjusted

---

## Full Palette

### Pattern
Three to four named color roles (primary, secondary, accent, tertiary), each with distinct job definitions.

### Before/After

**Before (accidental palette)**
```css
--blue: #2563eb;
--green: #16a34a;
--orange: #ea580c;
--purple: #9333ea;
```
These are named by color name, not by role. They have no hierarchy. The designer will use whichever feels right in the moment.

**After (intentional palette)**
```css
--color-role-primary:   oklch(45% 0.17 260);
--color-role-secondary: oklch(55% 0.14 180);
--color-role-accent:    oklch(60% 0.19 30);
--color-role-neutral:   oklch(25% 0.012 260);

/* Usage rules documented in code: */
/* primary   → navigation, headings, hero         */
/* secondary → tags, supporting sections, stats    */
/* accent    → CTAs, highlights, badges, pricing   */
/* neutral   → body text, secondary text, borders  */
```
Roles are named by function. Each color earns its place through clear job descriptions.

### When to Use Drenched

Use Drenched for immersive single-purpose surfaces: brand film landing pages, campaign microsites, seasonal showcases, "coming soon" pages. The goal is to wrap the visitor in the brand atmosphere. Use it when the content is minimal and the feeling is maximal.

### Anti-patterns

- Full Palette used when the product only needs two colors (inflated complexity)
- Colors that only appear once (unused palette entries)
- The accent color has no relationship to the primary (chromatic chaos)
- Dark mode in Full Palette where all four hues shift unpredictably

---

## Drenched

### Pattern
Background and primary are the same hue at different lightness levels. The color field is the experience.

### Before/After

**Before (applied drenched)**
```css
--bg: oklch(35% 0.15 260);
--surface: oklch(40% 0.16 260);
--text: oklch(85% 0.06 260);
```
The entire viewport is one hue family. Content floats in a color field.

**After (contextual drenched)**
```css
/* Interactive elements break the monochrome with tiny high-chroma relief */
--accent: oklch(72% 0.22 40);
--accent-hover: oklch(75% 0.24 40);

/* Text remains readable with deliberate contrast */
--text-primary: oklch(90% 0.04 260);
--text-secondary: oklch(70% 0.06 260);
```
The drenched background is 2–3 lightness steps below the text. The accent is the only element that introduces a different hue, and it is tiny.

### Anti-patterns

- Drenched on a settings page (function requires Restrained)
- Drenched in dark mode without adjusting chroma (colors that looked rich in light mode become muddy)
- No accent relief (the page becomes a sensory slab)
- Equal chroma at all lightness levels (darker surfaces need less chroma to feel saturated)
- Using Drenched as a shortcut for "we need to look like a brand" without considering readability

---

## Strategy Selection Flow

```
Is the primary goal communication or immersion?
  → Communication → Is visual hierarchy critical?
    → Yes → Restrained (data, tools, dashboards)
    → No  → Committed (SaaS, portfolio, brand site)
  → Immersion → Are there 3+ distinct content zones?
    → Yes → Full Palette (editorial, multi-product, platforms)
    → No  → Drenched (campaign, launch, showcase)
```

This is a starting point, not a rule. The actual choice depends on the scene sentence, the register, and the specific brand expression goals.

---

## Chroma Calibration Table

Guidance for selecting chroma values at different lightness levels:

| Lightness | Max Usable Chroma | Notes |
|-----------|-------------------|-------|
| L > 90%   | 0.02–0.06         | Pastels only. Chroma above 0.06 looks washed out, not saturated. |
| L 70–90%  | 0.06–0.14         | Tinted surfaces. Good for soft backgrounds, hover states. |
| L 40–70%  | 0.12–0.22         | Full saturation range. Primary and accent colors live here. |
| L 20–40%  | 0.08–0.16         | Dark colors. Chroma compresses—needs higher values to read as saturated. |
| L < 20%   | 0.02–0.08         | Near-black. Chroma almost invisible. Use for tinted darks only. |

These are starting ranges. Test in your actual rendering environment—calibration differs between screens, color profiles, and ambient light.
