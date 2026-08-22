# Validation & Warnings

GhostMEAN checks your geometry continuously and shows warnings below the
panel table — but **a warning never blocks a calculation**. This is
deliberate: GhostMEAN never refuses to compute something, and never
silently "fixes" your numbers either (see
[Panel Geometry](Panel-Geometry) for why that matters). A warning is
purely informational — it tells you something looks unusual, in case it
wasn't intentional.

## Every warning GhostMEAN can show

| Warning | Fires when | Why it matters |
|---|---|---|
| `Major ≤ 0` | A panel's Major chord is zero or negative. | Almost certainly a typo — a wing panel needs a positive chord. |
| `Minor ≤ 0` | A panel's Minor chord is zero or negative. | Same as above, for the tip chord. |
| `Length ≤ 0` | A panel's span is zero or negative. | A zero-length panel contributes nothing to the wing; usually unintentional. |
| `Minor > Major` | The tip chord is larger than the root chord. | An unusual (reversed) taper — not invalid, but worth double-checking. |
| Large sweep (`> 60°`) | A panel's LE sweep exceeds 60°. | Very large sweep angles are rare for typical RC wings; likely a units/decimal mistake (e.g. `60` instead of `6.0`). |
| `Major ≠ previous panel's Minor` | Two consecutive enabled panels don't line up — see [Panel Geometry](Panel-Geometry). | A real, visible step is drawn in the geometry (not smoothed away) — this warning tells you it's there so it's not a surprise. |

Only **enabled** panels are checked — a disabled panel's values don't
affect the wing, so they're not flagged even if they'd otherwise trigger
a warning.

## What a warning looks like

Warnings appear as a single orange line below the panel table, prefixed
with `⚠`, listing every active issue at once (separated by `•`). The
line disappears entirely the moment nothing is wrong anymore — including
after `Plik / File → New Project`, which resets all warnings along with
the geometry.

## Try it yourself

`tests/fixtures/test_err.csv` (see [CSV Format](CSV-Format)) is a
deliberately broken file that triggers several of these warnings at
once — load it if you want to see the validation behavior firsthand
without typing bad numbers yourself.
