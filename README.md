# Quant Survey Pipeline

An end-to-end interactive tool that walks through a quantitative consumer test — from study design through raw data generation, funnel diagnostics, benefit perception analysis, and strategic recommendations.

Built to demonstrate the full quant analytics workflow: not just the output deck, but the methodology, data structure, and analytical decisions behind it.

> **All data is synthetic.** Respondent records are algorithmically generated to mirror the statistical structure of a real consumer test. No proprietary or identifying information is present.

---

## Live demo

[leilistiic.github.io/quant-survey-pipeline](https://leilistiic.github.io/quant-survey-pipeline)

---

## What this covers

The tool is structured as a five-stage pipeline — each tab is one step in the analysis workflow.

| Stage | What it shows |
|---|---|
| **1 · Study Design** | Objectives, recruitment quotas, survey branching logic, questionnaire structure |
| **2 · Awareness & Funnel** | Conversion funnel (Aware → Trial → Repeat), BUMO-cut breakdown, awareness channel mix, regional cuts |
| **3 · Drivers & Barriers** | Trial driver and barrier rankings on an absolute scale, benefits sought by segment, benefit perception pre/post concept exposure |
| **4 · Product Experience** | Overall product rating, 16-attribute performance grid, improvement priorities, repeat intent |
| **5 · Recommendations** | Hypothesis testing framework, data-grounded strategic actions |

Tabs 2 and 3 include a **Luzon / Visayas / Mindanao toggle** for regional cuts — the Visayas awareness gap and Mindanao distribution story each surface differently at the regional level.

---

## Study context (synthetic)

**Category:** Facial wash / skincare  
**Product:** Reformulated variant with a new brightening and niacinamide claim  
**Sample:** n=306 · Three regions (Luzon, Visayas, Mindanao) · ~100 per region  
**Recruitment:** ≥80% non-core-BUMO per region · ~30% brightening-segment quota  

**Four BUMO segments tracked:**
- Functional / Anti-acne
- Brightening / Whitening ← key switching target
- Anti-aging / Moisture
- Multi-benefit / Other

**Core finding:** 67% awareness but only 20% trial among the brightening segment — not a product failure (trialists rate it well at 53% Excellent) but a credibility gap: the brightening claim isn't believed against a product still perceived as a functional/oil-control wash.

---

## Files

```
quant-survey-pipeline/
├── index.html                  # Self-contained interactive tool — deploy this
├── 01_generate_data.py         # Generates respondents_raw.csv and summary.json
├── 02_build_html.py            # Injects summary.json into index.html
├── data/
│   ├── respondents_raw.csv     # 306 synthetic respondents, 40+ columns
│   └── summary.json            # Pre-aggregated summary for HTML injection
└── previews/
    ├── tab1_preview.png
    ├── tab2_preview.png
    ├── tab3_preview.png
    ├── tab4_preview.png
    └── tab5_preview.png
```

---

## Respondent data structure

`respondents_raw.csv` contains one row per synthetic respondent with the following field groups:

**Demographics** — region, gender, age band, income band, household size, skin type, wash frequency

**Category behavior** — primary BUMO, top 3 benefits sought in a facial wash

**Awareness** — is_aware flag, awareness channel, familiarity tier

**Trial path (trialists only)** — trial drivers, purchase channel, pack size bought, time since last purchase/use

**Product ratings (trialists only)** — 16 attribute ratings on a 1–5 scale, overall product rating, product superiority vs BUMO, repeat intent, recommend intent, suggested improvements

**Non-trialist path** — trial barriers, concept test scores (relevance, purchase intent, value perception, price index vs. others), benefit perception pre/post concept exposure

---

## Data generation logic

`01_generate_data.py` engineers statistical structure into the synthetic data rather than generating noise:

- **Funnel rates are BUMO-differentiated** — core users trial at 2× the rate of the brightening segment by design, mirroring the real diagnostic
- **Benefit weights by segment** — each BUMO group has calibrated probabilities for each benefit sought, so the cross-tab tells a coherent story (brightening segment leads on brightening at 82%, anti-acne segment leads on oil control at 80%)
- **Regional awareness modifiers** — Visayas awareness is suppressed by ~16% to reproduce the distribution-driven awareness gap
- **Attribute ratings are structured** — functional/wash attributes (suitable for daily use, rinses cleanly) score 85–95% T1 Box; beauty-outcome attributes (brightens skin, reduces dark spots, skin feels hydrated) score 39–58%, reflecting the credibility gap from inside the product experience
- **Barrier spread is realistic** — "already satisfied" at 74% dominates the barrier mix, with claim disbelief at 15% a distant but actionable second

---

## How to rebuild

Requires Python 3.x, no external dependencies beyond the standard library.

```bash
# Step 1: Generate synthetic respondent data
python 01_generate_data.py
# → writes data/respondents_raw.csv and data/summary.json

# Step 2: Build the self-contained HTML tool
python 02_build_html.py
# → writes index.html
```

The HTML is fully self-contained — no external CDN calls, no runtime dependencies. Open `index.html` directly in a browser or deploy to any static host.

---

## Analytical techniques demonstrated

- Awareness–trial–repeat funnel construction with BUMO and regional cuts
- Benefit importance ranking (top-3 pick from a closed list)
- Barrier and driver analysis with absolute-scale % visualization
- Pre/post concept exposure benefit perception comparison
- 16-attribute product rating grid (T1 Box and average)
- Hypothesis testing framework for funnel drop-off diagnosis
- Strategic implication mapping from data to recommendation

---

## What this doesn't include

A real version of this study would also include:

- **Key driver analysis (KDA)** — regression or MaxDiff to identify which attributes most predict repeat intent
- **Significance testing** — two-proportion z-tests on BUMO-cut differences
- **Open-ended coding** — NLP or manual coding of verbatim liking/disliking responses
- **Sample weighting** — post-stratification weights to correct for the non-BUMO oversampling

These were handled in the live study workflow using Power BI and manual analysis; the pipeline tool focuses on the structured survey data and derived metrics.

---

## Related portfolio tools

- [Shopper Mission Ranging Console](https://leilistiic.github.io/ranging-console) — Drug channel store segmentation
- [Distribution Correlation Console](https://leilistiic.github.io/distribution-correlation-console) — Numeric distribution vs. share relationship
- [Category Growth Console](https://leilistiic.github.io/category-growth-console) — 20-year growth era decomposition
