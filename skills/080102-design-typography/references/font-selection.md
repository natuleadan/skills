# Font Selection Reference

## The Procedure (detailed)

### Step 1: Find 3 concrete brand-voice words

Most brand exercises produce abstractions: "elegant, modern, clean, sophisticated, premium." These words describe nothing. When you search a font catalog with "elegant," every font shows up.

Instead, describe the brand as a physical space:

| Abstract (bad) | Concrete (good) |
|---|---|
| Elegant, refined | Marble floor, brass fixtures, wool upholstery |
| Modern, clean | Glass window, steel frame, white wall |
| Friendly, approachable | Canvas bag, wooden toy, handwritten note |
| Trustworthy, professional | Wool suit, fountain pen, leather briefcase |

The words must be **physical objects** — things you can touch, smell, hear. A font catalog search filters better with "brass" + "wool" than "elegant" + "refined."

### Step 2: List the 3 reflex fonts

For a brand described as "marble floor, brass fixtures, wool upholstery," the reflex list might be:
1. Playfair Display (marble = classic serif, reflex)
2. Cormorant Garamond (brass = warm serif, reflex)
3. Fraunces (wool = soft serif, reflex)

**Write these down.** You will explicitly reject them in Step 3.

### Step 3: Reject them

The reflex fonts are the ones that come to mind immediately. They are the fonts every designer reaches for. By rejecting them, you force yourself to look deeper into the catalog. The goal is distinction, not correctness — many reflex fonts are perfectly decent typefaces.

### Step 4: Browse a real catalog

Use a real font catalog, not a "top 10" blog post:

| Source | URL | Best for |
|---|---|---|
| Google Fonts | fonts.google.com | Free, web-optimized, wide selection |
| Fontsource | fontsource.org | NPM-installable open-source fonts |
| Velvetyne | velvetyne.fr | Experimental, independent foundry |
| Future Fonts | futurefonts.xyz | Pre-release, cutting-edge type |
| Collletttivo | collletttivo.it | Collective open-source foundry |

Filter by the 3 concrete words. Look at **pages 2-5** of results. The first page is still reflex territory.

### Step 5: Cross-check

Final pick must not appear in the reflex list from Step 2. If it does, you didn't find a distinct choice — go back to Step 4.

---

## Reflex-reject font list (with rationale)

### Serif / Display Serif

| Font | Why rejected |
|---|---|
| **Fraunces** | The "soft serif" movement in one font. Every DTC brand from 2021-2023 used it. Variable-axis styling made it the "look, we're design-forward" choice. |
| **Newsreader** | Fraunces' more reserved sibling. The quiet default for "serious editorial." Still everywhere in 2024. |
| **Lora** | The default serif on every WordPress minimal-blog theme since 2016. Pairing it with literally anything signals "I picked the default." |
| **Crimson / Crimson Pro / Crimson Text** | The "academic poster" serif. Designed for TUG (TeX Users Group). Every design student's first serif choice. |
| **Playfair Display** | The "luxury brand" go-to. Its high contrast and crisp serifs make it the immediate pick for anything wine, fashion, or hotel. So oversaturated it's invisible. |
| **Cormorant / Cormorant Garamond** | Playfair's art-school cousin. Garamond revival with swash alternates. Every coffee shop, boutique, and indie magazine used it. |
| **DM Serif Display / DM Serif Text** | Google's own editorial serif, paired with DM Sans in every "startup blog" template. Safe, competent, forgettable. |
| **Instrument Serif** | The 2024 "new editorial" default. Saturated within a year of release. |

### Sans / Mono

| Font | Why rejected |
|---|---|
| **Inter** | The definitive "serious product" sans. Used by GitHub, Figma, Mozilla. Incredibly legible. Completely played out in every new SaaS dashboard. |
| **IBM Plex Sans / Serif / Mono** | The "we think about design" corporate stack. Adopted by every tech team that wanted to signal sophistication. Now signals "we copied IBM." |
| **Space Mono / Space Grotesk** | Developer-presentation default. Every tech conference slide deck since 2020. Grotesk is Inter's quirkier cousin — still everywhere. |
| **DM Sans** | Google's product sans. Paired with DM Serif in every template. Functional but worn out. |
| **Outfit** | The "rounded, friendly, modern" sans. Every wellness app, meditation brand, and children's product 2021-2024. |
| **Plus Jakarta Sans** | Outfit's more refined sibling. The "we're a serious wellness company" choice. Same saturation problem. |
| **Instrument Sans** | The 2024 product-sans default. Replaced Inter in the "new startup" stack. Already tired. |
| **Syne** | The "tech-forward variable font" displayed on every foundry demo. Overused as a "we do creative tech" signal. |

### What about these that are NOT reflex?

Some fonts are popular but earned their popularity through distinction, not saturation:

| Font | Why not reflex |
|---|---|
| **Satoshi** | Widely used but varied enough in applications. Its "grotesque with warmth" character still feels distinct. Use with caution — approaching reflex territory. |
| **Cabinet Grotesk** | Similar to Satoshi. Still slightly less saturated. |
| **Söhne** | Expensive (Klim license). Limited usage by budget alone. |
| **Untitled Sans** | Klim, expensive, reserved. Not in every free catalog. |
| **GT America / Pressura / Walsheim** | Grilli Type. Expensive, distinctive. Used by teams that invested in type. |

---

## Reflex-reject aesthetic lanes

Even with unique fonts, a saturated aesthetic pattern still reads as derivative.

### Editorial-typographic lane

**Identifiers**: Display serif heading + mono body + ruled `<hr>` separators + generous leading + minimalist layout + off-white background.

**Why rejected**: This is the default "design publication" look since 2019. It signals "we are designers" without differentiating which designers. Every portfolio, case study, and creative agency used it.

**Examples**: Fraunces + Space Mono + lots of `::before` decorative elements + ruled separators.

### Brutalist-utility lane

**Identifiers**: System-ui font stack + no border-radius + black-and-white + oversized type with no hierarchy + exposed grid lines.

**Why rejected**: Brutalism became the "I'm a serious UX person" backlash to decorative design. Now it's its own cliché — every tech landing page that wanted to look "raw" and "direct" used it.

**Examples**: Inter at 4rem + square black buttons + zero padding on card edges.

### Acid-maximalism lane

**Identifiers**: Variable-axis distortion (warp, slant, stretch) + vibrant gradients + retro grids + WIPE / SLIDE transitions.

**Why rejected**: The 2023-2024 creative-agency default. The reaction to minimalism became a trend itself. 90s rave aesthetics crossed with modern web tech.

**Examples**: Syne with full axis range + Warp filter on hero + chaotic color palette.

---

## Pairing strategies by genre

### Editorial / long-form / luxury

**Goal**: Create a clear voice contrast between display and body.

| Role | Characteristics | Examples (non-reflex) |
|---|---|---|
| Heading | Distinct serif, high contrast, strong personality | Garibaldi, Signifier, Tiempos Display |
| Body | Quiet sans, unobtrusive, excellent readability | Söhne, Untitled Sans, Graphik |

**Avoid**: Two serifs (competes for attention) or two quiet faces (says nothing).

**Pattern**: Headings interrupt with personality, body gets out of the way.

### Tech / dev / fintech

**Goal**: Authority, clarity, precision. One family does more than a pair.

| Approach | Examples (non-reflex) |
|---|---|
| Single variable family with extreme weight range | Uncut Sans (200-900), Obviously (variable) |
| Mono for code + sans for UI | Departure Mono + Bespoke Sans |
| Geometric sans with strong character | ABC Diatype, Avenir Next, Galapagos |

**Avoid**: Decorative serifs, multiple families, romantic flourishes. Tech branding is about earning trust through precision.

### Consumer / food / travel

**Goal**: Warmth, approachability, sensory connection.

| Role | Characteristics | Examples (non-reflex) |
|---|---|---|
| Brand voice | Warm sans with humanist details | Satoshi, General Sans, GT Alpina |
| Accent | Quirky serif for highlights | Tiempos, Tenez, Roslindale |

**Avoid**: Corporate clean (feels cold for food/travel) or overly decorative (feels insincere).

### Creative studios / agencies

**Goal**: Differentiation, attitude, rule-breaking.

**Strategies**:
- Mono body + display serif heading (old guard, but still works with unusual choices)
- One variable font pushed across all axes
- Extreme weight contrast within one family (hairline headings + black body)
- Pair an unusual genre (e.g., stencil + humanist) intentionally
- Use a "flawed" or hand-drawn face for personality

**Avoid**: Playing it safe. If the pair feels "comfortable," it's wrong for a creative studio.

---

## One family > timid pair

When in doubt, **commit to one family** rather than a safe pair that communicates nothing.

**Signs of a timid pair**:
- Both faces are neutral (Lora + Inter — neither says anything)
- Both faces have similar character (two geometric sans — why two?)
- The pair is the first Google Fonts recommended combo

**How one family wins**:
```
One committed family:          Timid pair:
Uncut Sans (200-900)          Lora + Inter
- hairline headings            - serif heading (default)
- semibold subheads            - sans body (default)
- regular body                 - zero character
- condensed for quotes         - no tension
- optical size range           - both blend in
```

If you can express the brand with one strong family, do that. Add a second only when there is a clear reason (e.g., technical text vs narrative text, brand voice vs body).
