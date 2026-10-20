# Accessibility review — public portfolio

2026-10-20. Target: WCAG 2.1 AA. This is a focused code and Chrome review, not a conformance certification.

## Findings and fixes

Two accessibility defects and one usability improvement were identified:

| Finding | Criterion | Impact | Resolution |
| --- | --- | --- | --- |
| Search/select borders had insufficient contrast | 1.4.11, non-text contrast | Major: input boundaries were harder to distinguish | Added `--control-border: #78909f`, providing 4.88:1 against the input background |
| Bootstrap's button focus styling could override the generic outline | 2.4.7, focus visible | Major: keyboard focus could be difficult to see | Added explicit component focus outlines; verified 2px teal outline with 4px offset in Chrome |
| Several standalone links had small hit areas | Optional target-size improvement | Minor: harder pointer/touch activation | Enlarged text links, clear-filter links, and footer links to at least 44px high |

44×44 target size is a WCAG 2.1 **AAA** criterion, not an AA requirement. This improvement does not claim every target meets AAA. [W3C target-size explanation](https://www.w3.org/WAI/WCAG21/Understanding/target-size.html).

Required visual control cues should contrast at least 3:1 against adjacent colors. Decorative divider lines do not identify input controls. [W3C non-text contrast](https://www.w3.org/WAI/WCAG21/Understanding/non-text-contrast.html).

## Contrast measurements

Computed from sRGB relative luminance, not sampled antialiased pixels.

| Element | Foreground | Background | Ratio | Threshold |
| --- | --- | --- | --- | --- |
| Body text | `#f0f1ed` | `#101923` | 15.62:1 | 4.5:1 |
| Muted card text | `#a6b2bd` | `#15212e` | 7.54:1 | 4.5:1 |
| Accent text/focus | `#83e1d3` | `#101923` | 11.54:1 | 4.5:1 text / 3:1 focus |
| Primary button text | `#10232b` | `#83e1d3` | 10.54:1 | 4.5:1 |
| Original input border | `#526370` | `#15212e` | 2.62:1 | 3:1 — failed |
| Revised input border | `#78909f` | `#15212e` | 4.88:1 | 3:1 |

## Keyboard and structure

- Skip link moves focus to `main`.
- Search → category → submit follows DOM order; category and submit have a visible focus outline.
- Enter submits the project filter successfully.
- Mobile menu exposes `aria-expanded` and `aria-controls`; Escape closes it and returns focus to its button.
- HTML parser/link tests check one h1 per page, language, unique IDs, input labels, landmarks, and anchor destinations.
- Decorative project artwork uses `aria-hidden`; the project title and description remain available in the link.
- Native select, button, input, and link semantics are retained. No custom ARIA widget or focus trap was introduced.
- All seven public pages have no horizontal document overflow at the tested 320px viewport (305px content area after scrollbar).

## Remaining manual review

NVDA/VoiceOver announcements, actual 200% text zoom, forced-colors mode, reduced-motion emulation, other browser engines, and physical devices were not tested. Source includes reduced-motion and no-JavaScript fallbacks, but source inspection does not replace assistive-technology testing.
