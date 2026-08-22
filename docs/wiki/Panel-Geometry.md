# Panel Geometry

A wing is up to 5 sequential panels, from root to tip. GhostMEAN draws
**one half** and mirrors it automatically — the wing is always assumed
symmetric (left = right).

## The four fields

| Field | Meaning |
|---|---|
| `Major` | The root chord (larger) of this panel — the width where the panel starts, closer to the centerline. |
| `Minor` | The tip chord (smaller) of this panel — the width where the panel ends, further from the centerline. |
| `Length` | This panel's own span, measured along the spanwise axis — one side only, not the whole wing. |
| `Sweep (LE)` | The leading-edge sweep of this panel. See below — this one has a precise, locked definition. |

## Sweep — the exact definition

This is the one term worth being precise about, because getting it wrong
produces a wing that *looks* fine but has the wrong geometry underneath.

- Measured from the **global spanwise axis** (perpendicular to the
  symmetry axis), **absolutely and independently for each panel**.
  Angles are **never accumulated** across panels — Panel 3 at 10° sweep
  is always at 10° from the spanwise axis, no matter what sweep Panels 1
  and 2 have.
- `0°` = leading edge parallel to the spanwise axis.
- A positive/negative value offsets the leading edge sideways.
- **The chord never rotates.** It always stays parallel to the root
  chord. Sweep only offsets the leading edge; the trailing edge follows
  automatically (LE + the local chord at that point), so a tapered
  panel's *effective* trailing-edge sweep differs from its LE sweep —
  that's expected, not a bug.

## Continuity: Minor(N) = Major(N+1)

For a normal, physically continuous wing, **Panel N's `Minor` should
equal Panel N+1's `Major`** — the tip of one panel is the root of the
next. GhostMEAN doesn't enforce this for you (see below), but the **⧉**
button next to each panel does it automatically: click it and the next
panel's `Major` is set to the current panel's `Minor`, plus `Length` and
`Sweep` are copied over as a starting point, and the next panel is
enabled.

## What happens if it's NOT continuous

**GhostMEAN's core principle: your data is the truth. The program never
"fixes" your geometry for you.**

If Panel N's `Major` doesn't match Panel N-1's `Minor`, this is **not**
silently smoothed over. A real, visible step appears in the trailing
edge of the drawing — exactly what the numbers say, identical on screen,
in [Station View](Station-View), and in the exported PDF. The M.A.C. /
Area calculation and the drawing always read from the same single source
of geometry, so they can never disagree with each other.

GhostMEAN does show a warning when this happens (`Major ≠ previous
panel's Minor`) — see [Validation & Warnings](Validation) — but the
warning never blocks or hides anything. If you *meant* to have a step
(e.g. a strake, or a deliberately mismatched panel), that's fully
supported; the warning is just there so an accidental typo doesn't go
unnoticed.
