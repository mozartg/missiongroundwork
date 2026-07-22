# Mission GroundWork — Market Visual Benchmark

**Date:** 2026-07-22  
**Decision threshold:** retain only if the current creative is within 10% of the benchmark composite.

## Comparison set

1. The Bridgespan Group
2. FSG
3. Dalberg
4. Campbell & Company
5. Mission + Strategy
6. Build Up Advisory Group
7. SME Strategy
8. Usman Group
9. Niftic
10. Whole Whale

These are comparison references, not claims that every firm is a direct commercial competitor. The set spans nonprofit strategy, capacity building, fundraising, branding, digital strategy, and implementation.

## Weighted visual scorecard

| Dimension | Weight | Leader median | GroundWork before | Gap |
|---|---:|---:|---:|---:|
| Promise clarity in first screen | 20 | 91 | 76 | -16.5% |
| Visual hierarchy and scan speed | 15 | 89 | 61 | -31.5% |
| Trust/proof above the fold | 15 | 86 | 32 | -62.8% |
| Service differentiation | 15 | 84 | 69 | -17.9% |
| CTA confidence and navigation | 10 | 90 | 52 | -42.2% |
| Human warmth without stock-brand cliché | 10 | 82 | 73 | -11.0% |
| Mobile-ready density | 10 | 88 | 64 | -27.3% |
| Distinctive brand character | 5 | 78 | 72 | -7.7% |
| **Composite** | **100** | **86.9** | **61.7** | **-29.0%** |

## Decision

The original creative failed the 10% proximity rule. It is superseded, not treated as launch-ready.

## What was removed

- single-purpose logo-only header with no navigation or CTA;
- long narrative opening before the visitor could identify the offer;
- five-role bullet list in the first screen;
- low-information CTA, “See the plans”;
- unsupported positioning without an immediate explanation of the working method.

## Replacement design

### First-screen structure

1. compact navigation with one dominant CTA;
2. category label: implementation support for lean nonprofit teams;
3. outcome-led headline;
4. two-sentence explanation;
5. primary and secondary actions;
6. three operating signals: role-ready plans, usable artifacts, handoff-ready systems;
7. visual “GroundWork Plan” card showing the actual output structure.

### Target after-score

| Dimension | Target |
|---|---:|
| Promise clarity | 92 |
| Visual hierarchy | 90 |
| Trust/proof architecture | 82 |
| Service differentiation | 88 |
| CTA confidence | 91 |
| Human warmth | 84 |
| Mobile density | 88 |
| Distinctive character | 85 |
| **Composite target** | **87.7** |

This target is 0.9% above the comparison median. It remains provisional until browser screenshots, accessibility checks, and user recognition tests are completed.

## Verification required

- desktop screenshot at 1440 px;
- mobile screenshot at 390 px;
- Lighthouse accessibility score of at least 95;
- no horizontal overflow;
- CTA destinations work;
- five-person recognition test: at least four can explain the offer after 10 seconds;
- proof statements remain factual and traceable.

## Rollback

Revert the commits that modify `Header.tsx`, `Hero.tsx`, and `App.tsx`, and delete this benchmark file and `BenchmarkBand.tsx`. The prior content remains recoverable through Git history.