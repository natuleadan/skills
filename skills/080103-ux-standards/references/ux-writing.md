# UX Writing Reference

Deep reference for UX copy: error messages, empty states, CTAs, confirmation dialogs, success states, tone, and conciseness.

---

## Core Principles

1. **Every word earns its place** — if removing a word doesn't change meaning, remove it
2. **No restated headings** — if heading says "Payment", don't start body with "On the payment page…"
3. **No intros that repeat the title** — the heading already tells users where they are
4. **No em dashes** — use commas, colons, or semicolons
5. **Positive phrasing** — "Enter at least 8 characters" not "Password too short"
6. **One idea per sentence** — users scan, they don't read
7. **Write for scanning** — use lists, bold key terms, short paragraphs
8. **Avoid jargon, acronyms, and technical terms** unless your audience expects them

---

## Error Messages

### Formula: [What happened] + [Why it happened] + [How to fix it]

| Component | Example |
|---|---|
| What happened | "Couldn't save changes" |
| Why | "because the server is temporarily unavailable" |
| Fix | "Check your connection and try again" |

### Patterns

```
✗ Bad: "Invalid input"
✓ Good: "Enter a valid email address (e.g., user@example.com)"

✗ Bad: "Error 500"
✓ Good: "Something went wrong on our end. Please try again. If the problem persists, contact support."

✗ Bad: "Required"
✓ Good: "Password is required to create your account"

✗ Bad: "Field must be between 3-50 characters"
✓ Good: "Choose a username between 3 and 50 characters"

✗ Bad: "Invalid password"
✓ Good: "Password must include at least 8 characters, one uppercase letter, and one number"

✗ Bad: "Network error"
✓ Good: "Unable to connect. Check your internet connection and try again."
```

### Error Recovery

Offer a clear next step:
```
"Your session expired. [Log in again]"
"Couldn't load search results. [Try again]"
"Payment failed. Card declined by issuer. Try a different payment method or [contact your bank]."
```

---

## Empty States

### Formula: [Why it's empty] + [What to do about it]

```
✗ Bad: "Nothing here"
✓ Good: "No products yet — add your first product to get started"

✗ Bad: "No results"
✓ Good: "No results for "xyz". Try a different search term or browse our [categories]."

✗ Bad: "No notifications"
✓ Good: "No new notifications. We'll let you know when something arrives."

✗ Bad: "No files"
✓ Good: "Upload files to share them with your team. [Upload files]"
```

### Empty State Components
1. Relevant illustration or icon (optional — don't force it)
2. Brief explanation (why is this empty?)
3. Clear action button or link (what to do next)

---

## Call-to-Actions (CTAs)

### Specific Verbs Only

```
✗ Bad: "Submit"
✓ Good: "Create account", "Save changes", "Send message"

✗ Bad: "OK"
✓ Good: "Confirm", "Delete workspace", "Add to cart"

✗ Bad: "Yes" / "No"
✓ Good: "Delete file" / "Keep file", "Leave workspace" / "Stay"

✗ Bad: "Continue"
✓ Good: "Continue to payment", "Continue to review"
```

### CTA Guidelines
- Start with a verb (action-oriented)
- Be specific about what happens when clicked
- Keep under 3-4 words
- Match the button label to the page heading/task
- Use sentence case: "Save changes" not "Save Changes"

---

## Confirmation Dialogs

### Formula: [What will happen] + [Scope] + [Reversibility or consequences]

```
✗ Bad: "Are you sure?"
✓ Good: 'Delete "Project Alpha"? This action cannot be undone. All files, comments, and settings will be permanently removed.'

✗ Bad: "Confirm"
✓ Good: 'Remove "Jane Doe" from the workspace? They will lose access to all projects and files.'

✗ Bad: "Discard changes?"
✓ Good: "You have unsaved changes. If you leave, your changes will be lost."
```

### Confirmation Button Labels
| Dialog Purpose | Confirm Button | Cancel Button |
|---|---|---|
| Delete single item | "Delete file" | "Cancel" |
| Delete multiple items | "Delete 3 files" | "Cancel" |
| Discard changes | "Discard" | "Keep editing" |
| Leave workspace | "Leave workspace" | "Stay" |
| Remove member | "Remove member" | "Cancel" |
| Cancel subscription | "Cancel subscription" | "Keep plan" |

---

## Success States

### Brief, Action-Specific

```
✓ "Workspace created"
✓ "Invitation sent to 3 people"
✓ "Changes saved"
✓ "Password updated"
✓ "Payment successful"
✓ "Upload complete (14 files)"
```

```
✗ Bad: "Success!"
✓ Good: "Profile updated"

✗ Bad: "Your changes have been saved successfully."
✓ Good: "Changes saved"

✗ Bad: "The file has been uploaded to your account. You can now share it with others."
✓ Good: "File uploaded"
```

### When to Add Next Steps
If the action leads to another action the user likely wants to take:
```
"Workspace created. [Invite your team]"
"Payment confirmed. [View receipt]"
"Upload complete. [Share files]"
```

---

## Tone

### Establish Your Voice

| Product Type | Tone |
|---|---|
| B2B / Enterprise | Professional, direct, respectful. Avoid jokes or casual phrasing |
| Consumer / Creative | Warm, helpful, human. Can have personality when appropriate |
| Utility / Tool | Minimal, functional, neutral. Get out of the way |
| Health / Finance | Empathetic, clear, trustworthy. No ambiguity |
| Kids / Education | Simple, encouraging, playful |

### Voice Principles (All Products)

1. **Be helpful, not clever** — users came to accomplish a task, not to be entertained
2. **Be respectful of user data** — don't joke about sensitive actions (deletion, payment, privacy)
3. **Be consistent** — same tone on error as on success
4. **Be concise** — half the words, twice the clarity
5. **Be human** — prefer contractions ("you'll" over "you will", "can't" over "cannot")

---

## Microcopy

### Placeholder Text
Use for format examples, not instructions:
```
✓ "user@example.com"
✗ "Enter your email address"
✗ "Email"
```

### Helper Text
Use for clarification, not repetition:
```
✓ "We'll never share your email"
✗ "Enter your email address in the field below"
```

### Loading States
```
✓ "Saving…" / "Uploading…" / "Processing…" / "Connecting…"
✗ "Please wait" / "Loading, please be patient"
```

### Tooltip Text
- Use only when the label or surrounding context isn't enough
- Explain the consequence or benefit, not the literal behavior
```
✓ "Public: visible to anyone with the link"
✗ "Toggle this to make it public"
```

---

## Formatting & Punctuation

### Sentence Case
- Buttons, headings, links, labels: sentence case ("Save changes" not "Save Changes")
- Proper nouns and brand names: capitalized as usual

### Punctuation
- Error messages: end with period (full sentences)
- Button labels: no period
- Snackbar/toast: no period
- Labels: no period
- Helper text: full sentences with period
- Lists: each item ends with period if items are full sentences

### Numbers
- Numbers 0–9: spell out ("three items")
- Numbers 10+: use numerals ("14 files")
- Percentages: use "%" symbol ("25% complete")
- Currency: use symbol + numeral ("$49.99")

---

## Accessibility in Copy

### Screen Reader Awareness
- Avoid directional language: "on the left", "below" — use "previous", "next", "following"
- Headings must be descriptive: "Payment settings" not "Settings"
- Links must be meaningful: "View order details" not "Click here"
- Alt text: describe the purpose, not the appearance

### Date & Time
```
✓ "May 25, 2026" — screen reader pronounces naturally
✓ "25 May 2026" — unambiguous across locales
✗ "05/25/26" — ambiguous (US vs EU interpretation)
```

---

## Common Violations

| Violation | Fix |
|---|---|
| "Please enter your email" | "Enter your email" |
| "Successfully deleted" | "Deleted" or "Workspace deleted" |
| "You have 3 notifications" | "3 notifications" |
| "Click here for more info" | "View documentation" |
| "Are you sure you want to continue?" | Specific confirmation |
| "Invalid credentials" | "Email or password is incorrect" |
| "Your session has expired" | "Session expired. Log in again." |
| "An error has occurred" | Specific error + fix |
