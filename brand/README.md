# Order The Market — brand assets

**Name:** Order The Market
**Tagline:** Your success is our mission
**Mark:** a gold crescent wrapping rising gold bar-chart columns, cut by a red upward arrow, with small white sparkles.

## Colors

| Role | Hex | Notes |
|------|-----|-------|
| Background (maroon) | `#420000` | Deep maroon canvas of the full logo |
| Gold, light | `#EED875` | Main fill of crescent and bars |
| Gold, highlight | `#F4DC88` | Wordmark and lightest gold |
| Gold, mid | `#CEAC5C` | Gradient middle, tagline |
| Gold, dark | `#B78E4A` | Outlines and shaded edges |
| Red, bright | `#ED2024` | Arrow, start of gradient |
| Red, deep | `#721011` | Arrow tip, end of gradient |
| Sparkle | `#FFFFFF` | Small star accents |

Wordmark: wide, bold geometric sans in caps with very wide letter-spacing; tagline is the same style, smaller, in mid gold.

## Files (`logo/`)

| File | Use |
|------|-----|
| `fulllogo*.png/jpg` | Icon + wordmark + tagline. `_transparent` has no maroon background; `_nobuffer` is cropped tight. |
| `icononly*.png` | Mark alone (favicon, app icon, avatar). |
| `textonly*.png` | Wordmark alone. |
| `grayscale*.png` | One-color version for monochrome contexts. |
| `print*.svg/pdf/eps` | Vector versions for web scaling and print. Prefer `print_transparent.svg` on the web. |

On light backgrounds use a `_transparent` file; on dark/maroon use the standard one.
