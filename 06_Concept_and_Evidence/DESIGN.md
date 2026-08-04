---
name: SAAKSHI
description: The witness for every rupee — an evidence-dossier accountability layer over India's public spending data.
colors:
  cream: "#F4F0E6"
  cream-panel: "#FBF9F3"
  cream-warm: "#EDE6D6"
  hair: "#D8D0BE"
  hair-strong: "#C9BFA6"
  navy: "#202A3E"
  navy-deep: "#1A2233"
  ink-2: "#4A5162"
  ink-3: "#5E6472"
  ink-faint: "#6B6858"
  case-bg: "#101826"
  case-panel: "#1D2740"
  case-hair: "#2A3450"
  on-dark: "#E9E4D7"
  on-dark-2: "#C9CEDA"
  on-dark-3: "#8A94AC"
  saffron: "#D98A2B"
  saffron-deep: "#B9761F"
  saffron-label: "#925C12"
  saffron-lite: "#E0912F"
  green: "#2E8B6B"
  green-deep: "#24735A"
  green-bright: "#5BD6A0"
  blue: "#2C6488"
  red: "#C0392B"
typography:
  display:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "clamp(2.7rem, 2.1rem + 4.2vw, 5.4rem)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "clamp(1.9rem, 1.4rem + 2.4vw, 3.1rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Georgia, 'Times New Roman', serif"
    fontSize: "clamp(1.4rem, 1.2rem + 0.7vw, 1.85rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.012em"
  body:
    fontFamily: "'Segoe UI', system-ui, -apple-system, Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "clamp(1rem, 0.96rem + 0.2vw, 1.075rem)"
    fontWeight: 400
    lineHeight: 1.62
  label:
    fontFamily: "'Segoe UI', system-ui, -apple-system, Roboto, 'Helvetica Neue', Arial, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 700
    letterSpacing: "0.12em"
  mono:
    fontFamily: "'Cascadia Code', 'Consolas', 'SFMono-Regular', 'Liberation Mono', Menlo, monospace"
    fontSize: "0.84rem"
    fontWeight: 400
rounded:
  sm: "6px"
  md: "10px"
  pill: "40px"
spacing:
  band-py: "clamp(4.5rem, 9vw, 8.5rem)"
  gutter: "clamp(1.25rem, 5vw, 5rem)"
  measure: "68ch"
components:
  button-primary:
    backgroundColor: "{colors.saffron}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: "0.85rem 1.4rem"
  button-primary-hover:
    backgroundColor: "{colors.saffron-deep}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.navy}"
    rounded: "{rounded.sm}"
    padding: "0.85rem 1.4rem"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.navy}"
    rounded: "{rounded.sm}"
    padding: "0.55rem 1rem"
  card-cream:
    backgroundColor: "{colors.cream-panel}"
    textColor: "{colors.navy}"
    rounded: "{rounded.md}"
    padding: "1.6rem"
  card-casefile:
    backgroundColor: "{colors.case-bg}"
    textColor: "{colors.on-dark}"
    rounded: "{rounded.md}"
  chip-conf-high:
    backgroundColor: "{colors.green}"
    textColor: "#FFFFFF"
    rounded: "4px"
    padding: "0.18rem 0.6rem"
---

# Design System: SAAKSHI

## Overview

**Creative North Star: "The Forensic Dossier"**

SAAKSHI reads as a case that has been opened on a warm paper desk, not a product landing page. Everything sits on a cream ledger ground ruled with a faint 40px baseline grain, and the evidence — data-source graphs, audit ledgers, terminal runs, case files — arrives on it as physical documents: hairline-bordered cream panels for the reasoning, and near-black "case-file" cards for the raw machine output. The two surfaces alternate down the page so the argument feels like it moves between the desk (where a person reasons) and the machine (where the data lives). Georgia serif carries every heading and every pull-quote; the sans is reserved for reading and for machine labels; monospace is the voice of IDs, codes, and figures.

The personality is sober, evidentiary, and quietly confident. Saffron is the single accent that lights up a live edge, a primary action, or a validated finding; forensic green marks confirmation; the palette never reaches for a second decorative hue. Density is high but ordered — data is packed into grids of hairline-divided cells (ledgers, dossier meta, signal grids) rather than loose cards. The one recurring, load-bearing gesture is the ⚠ honest-limit mark, which appears as a first-class element wherever the system states what it cannot know. This world explicitly refuses the default problem→solution→team explainer chrome, the fused "score," and any decoration that would read as marketing rather than evidence.

**Key Characteristics:**
- Cream paper desk vs. near-black case-file, alternated band by band.
- Georgia serif for all display and pull-quotes; monospace for every ID, code, and figure.
- One saffron accent + one green confirmation hue; no decorative color.
- Hairline-divided data grids over loose cards; high, ordered density.
- The ⚠ honest-limit callout is a first-class element, never a footnote.
- Every motion effect degrades to a static, complete end-state.

## Colors

A warm two-ground palette — aged-paper cream and forensic navy/near-black — lit by a single saffron accent and a confirming green, with reserved blue and red for signal states only.

### Primary
- **Saffron (#D98A2B):** The one accent. Primary buttons, the lit graph edge, the corner case-marker chip, validated-finding tint, and the ⚠ mark base. On dark surfaces it shifts to **Saffron Lite (#E0912F)**; for large serif lockups on cream it deepens to **Saffron Deep (#B9761F)**; for small saffron text on cream it uses **Saffron Label (#925C12)** to hold contrast.

### Secondary
- **Forensic Green (#2E8B6B):** Confirmation and success — "verified" provenance pills, "FIRED"/PASS detector states, HIGH-confidence chips. On dark it brightens to **Green Bright (#5BD6A0)**; borders and the user-turn stroke use **Green Deep (#24735A)**.

### Tertiary
- **Signal Blue (#2C6488):** LOW-confidence chip and the persona's serif "sensor" line only. A quiet, non-actionable marker.
- **Alert Red (#C0392B):** Reserved strictly for failure/alert — the zero-recovery ledger figure, alert rows, the flag-detector state, the terminal's first traffic dot. Never used decoratively.

### Neutral
- **Cream (#F4F0E6):** The page ground; the desk everything sits on.
- **Cream Panel (#FBF9F3):** Raised reasoning surfaces — cards, node-line, persona, legend cells.
- **Cream Warm (#EDE6D6):** Inline code chips and the flywheel pill.
- **Hair (#D8D0BE) / Hair Strong (#C9BFA6):** Light-ground borders and dividers; the ruled-ledger hairline.
- **Navy (#202A3E) / Navy Deep (#1A2233):** Ink for all headings and text on cream; navy is also the full-bleed dark band ground, navy-deep the colophon.
- **Ink 2 / Ink 3 / Ink Faint (#4A5162 / #5E6472 / #6B6858):** The three-step muted-text ramp on cream — body-muted, secondary, and captions respectively, each held above its documented contrast floor.
- **Case BG (#101826) / Case Panel (#1D2740) / Case Hair (#2A3450):** The near-black case-file surface, its header/inset panel, and its hairlines.
- **On-Dark (#E9E4D7) / On-Dark 2 / On-Dark 3 (#C9CEDA / #8A94AC):** The text ramp on dark case-file surfaces — primary, secondary, muted.

### Named Rules
**The One Accent Rule.** Saffron is the only accent hue; green is confirmation, blue/red are signal states. A surface never introduces a fourth decorative color to add interest — density and hairlines carry the visual load instead.

**The Contrast-Tuned Saffron Rule.** Saffron is not one value: pick the variant for its ground (saffron-deep/label on cream, saffron-lite on dark). Never place base #D98A2B as small text on cream.

## Typography

**Display Font:** Georgia (with Times New Roman, serif)
**Body Font:** Segoe UI (with system-ui, Roboto, Helvetica Neue, Arial)
**Label/Mono Font:** Cascadia Code / Consolas monospace (ligatures off)

**Character:** A newspaper-of-record pairing: a classical serif that gives every heading and pull-quote gravity, against a plain civic-system sans for reading and machine labels. Monospace is a third, deliberate voice — it means "this is data": an ID, a code, a figure, a command.

### Hierarchy
- **Display** (Georgia 700, clamp 2.7–5.4rem, line-height 0.98, tracking -0.03em): the hero title only. Tightest tracking and leading of the ramp.
- **Headline** (Georgia 700, clamp 1.9–3.1rem, tracking -0.02em, max ~20ch): band titles.
- **Title** (Georgia 700, clamp 1.4–1.85rem): persona name, limit titles, section sub-heads.
- **Body** (Segoe UI 400, clamp 1–1.075rem, line-height 1.62, measure ~68ch): all running prose; ledes cap tighter (~40–54ch).
- **Label** (Segoe UI 600–700, 0.72–0.78rem, tracking 0.08–0.16em, uppercase): section kickers-in-context like "THE EVIDENCE GRAPH", column headers, provenance and status pills.
- **Serif Pull-Quote** (Georgia, clamp ~1.2–1.75rem, line-height ~1.4): the recurring device that closes a band — `.join__pull`, `.failure__pull`, `.run__foot`, `.colophon__line` — often italic on dark.
- **Mono** (monospace, ~0.7–0.88rem, tabular-nums for figures): every ID, LGD code, ₹ figure, command, and evidence hash.

### Named Rules
**The Data-Is-Mono Rule.** Any identifier, location code, currency figure, hash, or shell command is set in monospace. Prose is never set in mono, and data is never set in the serif or sans body face.

**The Serif-Closes-the-Band Rule.** Each narrative band ends on a Georgia pull-quote that states the takeaway. It is the one place body-scale prose gives way to serif.

## Layout

A single centered column, max-width **1320px**, with a fluid **gutter** of `clamp(1.25rem, 5vw, 5rem)`. The page is a vertical stack of full-bleed **bands**, each with vertical padding `--band-py` (`clamp(4.5rem, 9vw, 8.5rem)`); band grounds alternate cream and navy to pace the desk↔machine rhythm. Text measure is capped at `--measure` (68ch) for prose, tighter for ledes.

Two-column grids appear at the hero (`1.05fr / 1fr`), the citizen loop (`0.85fr / 1.15fr`, persona sticky at `top: 5.5rem`), and the close (`1.35fr / 0.65fr`); all collapse to a single column at 820–880px. Dense data is laid out as **hairline-gap grids**: ledger rows, dossier meta and signals, and the portal legend use `1px` gaps over a hair-colored background so the cell edges read as ruled lines rather than card gutters (`repeat(auto-fit/auto-fill, minmax(190–280px, 1fr))`).

Breakpoints in use: **940px** (masthead nav hides, CTA moves to the right), **880/820px** (grids collapse to one column, scroll-cue hidden), **620/430px** (terminal banner scales down), **480px** (masthead padding and wordmark tighten), **360px** (masthead CTA drops — the hero already carries both actions). Spacing rhythm is expressed almost entirely in `rem` with `clamp()` for fluidity; there is no fixed numeric step scale.

## Elevation & Depth

A hybrid: flat, hairline-bordered surfaces at rest, lifted by soft offset-plus-blur shadows that read as a document resting on a desk — never a flat halo. Cards and panels carry `--shadow-card`; dark case-file surfaces carry the deeper `--shadow-dark`; hover on a liftable card swaps to `--shadow-lift` with a `translateY(-2px/-3px)`. Depth on the dark bands is reinforced tonally (case-bg < case-panel) and by hairlines, not by heavier shadows.

### Shadow Vocabulary
- **Card** (`box-shadow: 0 1px 2px rgba(32,42,62,.05), 0 12px 30px -14px rgba(32,42,62,.28)`): resting elevation for cream panels, node-line, legend, buttons.
- **Lift** (`box-shadow: 0 2px 4px rgba(32,42,62,.06), 0 26px 60px -22px rgba(32,42,62,.40)`): hover state for cards and the primary button.
- **Dark** (`box-shadow: 0 2px 6px rgba(0,0,0,.30), 0 34px 70px -26px rgba(0,0,0,.55)`): every case-file / terminal / dossier / call surface.

### Named Rules
**The Offset-Not-Halo Rule.** Shadows always pair a tight near-shadow with a soft, downward, negatively-spread far-shadow so the surface reads as lifted paper. No symmetric ambient glow.

## Shapes

Gently rounded rectangles: **10px** (`--radius`) for cards, panels, ledgers, dossiers, and terminals; **6px** (`--radius-sm`) for buttons, chips, insets, and result banners; **4px** for the smallest pills (provenance, tags); **40px** for the two full-pill lozenges (flywheel claim, alignment tags) and the SVG portal labels. Borders are always hairlines — `--hair`/`--hair-strong` on cream, `--case-hair` on dark — and dividers are frequently a single dotted or solid hairline rather than a filled rule. Team placeholders use a **dashed** hairline to signal "intentionally blank." The signature non-rectangular form is the 45°-rotated saffron **case-marker chip** pinned to the corner of the hero node-line.

## Components

### Buttons
- **Shape:** gently rounded (6px, `--radius-sm`); pill-height inline-flex with a 0.6rem gap for the optional arrow glyph.
- **Primary:** saffron ground, white text, saffron-deep border, `--shadow-card`; padding `0.85rem 1.4rem`. Hover deepens to saffron-deep, lifts `translateY(-2px)`, swaps to `--shadow-lift`, and slides the arrow `+4px`.
- **Secondary:** transparent with a hair-strong border and navy text; hover darkens the border to navy over a cream-panel fill and lifts.
- **Ghost:** the compact variant (`0.55rem 1rem`, 0.9rem) — masthead CTA and "re-watch" actions.
- **Motion:** all transforms are suppressed under `prefers-reduced-motion`.

### Chips / Tags / Pills
- **Confidence chips** (`.conf`): solid-fill, white text, 4px radius — green (HIGH), saffron (MEDIUM), blue (LOW).
- **Provenance pills** (`.prov`): tinted translucent background + matching hairline border + inline SVG icon; green "verified live", saffron "reported".
- **Status/tag pills** (`.tag`, `.detector__status`): small uppercase mono, translucent tinted background, hairline border; state-driven (queued → running → FIRED).
- **Lozenges** (`.flywheel__novel`, `.align__list li`): 40px full pills, cream-warm or case-panel fill.

### Cards / Containers
- **Corner Style:** 10px.
- **Cream card** (`.limit`, `.loop__persona`, `.node-line`): cream-panel ground, hair border, `--shadow-card`; hover lifts to `--shadow-lift`.
- **Case-file card** (`.dossier`, `.terminal`, `.ledger`, `.call`, `.cmd`): case-bg ground, case-hair border, `--shadow-dark`, `overflow: hidden` so inner hairline grids clip cleanly.
- **Border:** always a hairline; dashed only for deliberately-blank placeholders.
- **Internal padding:** ~1.6rem on cream cards; dark surfaces use a fluid `clamp(1.1rem, 3vw, 2rem)`.

### Navigation (Masthead)
- Sticky, translucent cream (`color-mix` 86%) with `backdrop-filter: blur(10px) saturate(140%)` and a hair bottom border.
- Wordmark pairs a Georgia "SAAKSHI" with a saffron-label Devanagari साक्षी.
- Nav links are sans 600, ink-2, with a saffron underline that wipes in left→right on hover/focus (`right: 100% → 0`).
- Responsive: nav hides at 940px (CTA shifts right), the CTA itself drops at 360px.

### Signature: The Evidence Graph & Case-File Ledger
- **Evidence graph** (hero SVG): a central navy village node with a saffron ring, two dashed-hairline rings of eleven monospace-labelled portal pills, connected by faint saffron quadratic edges. On scroll the edges draw inward in sequence and briefly light (`--edge-lit`) as portals pop in; four concentric detector sweep arcs animate during the run. Fully present as static fallback.
- **Ledger / dossier / detector list:** hairline-gap grids on case-bg. Fired-signal state is carried by a head tint + status pill (green/saffron/red by confidence), never a colored side-border. Figures are right-aligned mono; the zero-recovery figure is the one red value.

### The Honest-Limit Mark (⚠)
A first-class element: `.warn-mark`, sans 700, saffron-deep on cream / saffron-lite on dark. It opens every limit card, caveat, synthetic-data notice, and the case-file verdict. It is content, not decoration.

## Do's and Don'ts

### Do:
- **Do** alternate cream reasoning surfaces with near-black case-file surfaces to pace the desk↔machine narrative.
- **Do** set every ID, code, currency figure, hash, and command in monospace (with `tabular-nums` for animated figures).
- **Do** close each narrative band with a Georgia serif pull-quote.
- **Do** carry fired/confidence state through head tints and status/confidence pills (green/saffron/blue/red), and provenance through the tinted pill-with-icon.
- **Do** lead any statement of uncertainty with the ⚠ honest-limit mark, inline with the claim it constrains.
- **Do** build data as hairline-gap grids (`1px` over a hair background), and give every graphic a complete static fallback plus a `prefers-reduced-motion` end-state.
- **Do** pick the saffron variant that matches the ground (deep/label on cream, lite on dark).

### Don't:
- **Don't** introduce a fourth decorative hue; blue and red are signal states only, never accents.
- **Don't** fuse the four signals into a single "score," visually or otherwise — four independent detectors, shown separately, is doctrine.
- **Don't** use a colored side-border or costume bar to mark a card's state; tint the head and set the pill instead.
- **Don't** set data in the serif/sans body face or prose in monospace.
- **Don't** use flat symmetric halo shadows; always the offset-plus-soft-blur pair.
- **Don't** rely on any animation to convey information — content lives in the HTML and must read with JS off.
