import json, os
BASE = os.path.dirname(__file__)
with open(os.path.join(BASE,"data","summary.json")) as f:
    DATA = json.load(f)
DJ = json.dumps(DATA)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>Quant Survey Pipeline | Facial Wash Consumer Test</title>
<style>
:root{{
  --ink:#16162a;--ink-mid:#4a4a6a;--ink-muted:#8888a8;
  --paper:#f8f7fc;--white:#fff;
  --accent:#5346c8;--accent-lt:#edebff;
  --a2:#c2488a;--a3:#1aaa78;--warn:#d95b2a;--warn-lt:#fef0ea;
  --border:#e2dff0;
  font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--paper);color:var(--ink);min-height:100vh;font-size:14px;line-height:1.6}}

.site-header{{background:var(--ink);padding:22px 28px 20px;position:sticky;top:0;z-index:50}}
.site-header h1{{font-size:17px;font-weight:700;color:#fff;letter-spacing:-.3px}}
.site-header p{{font-size:12px;color:var(--ink-muted);margin-top:2px}}
.hbadge{{display:inline-block;background:var(--accent);color:#fff;font-size:10px;font-weight:700;
  padding:2px 8px;border-radius:20px;letter-spacing:.5px;text-transform:uppercase;margin-left:8px;vertical-align:middle}}

.pipeline-nav{{display:flex;background:#fff;border-bottom:2px solid var(--border);overflow-x:auto;
  scrollbar-width:none;position:sticky;top:68px;z-index:40;padding:0 18px}}
.pipeline-nav::-webkit-scrollbar{{display:none}}
.ptab{{display:flex;align-items:center;gap:7px;padding:0 16px;height:48px;font-size:12.5px;
  font-weight:600;color:var(--ink-muted);cursor:pointer;white-space:nowrap;
  border-bottom:3px solid transparent;margin-bottom:-2px;transition:color .15s,border-color .15s;user-select:none}}
.ptab:hover{{color:var(--accent)}}
.ptab.active{{color:var(--accent);border-bottom-color:var(--accent)}}
.tnum{{width:20px;height:20px;border-radius:50%;background:var(--border);display:flex;
  align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0}}
.ptab.active .tnum{{background:var(--accent);color:#fff}}

.main{{max-width:1080px;margin:0 auto;padding:28px 20px 80px}}
.step-panel{{display:none}}.step-panel.active{{display:block}}
.section-title{{font-size:21px;font-weight:800;color:var(--ink);letter-spacing:-.4px;margin-bottom:3px}}
.section-sub{{font-size:13px;color:var(--ink-mid);margin-bottom:24px;max-width:660px}}

/* REGION TOGGLE */
.region-toggle{{display:flex;gap:6px;margin-bottom:20px;flex-wrap:wrap;align-items:center}}
.region-toggle span{{font-size:12px;color:var(--ink-muted);margin-right:4px;font-weight:600}}
.rtbtn{{padding:5px 14px;border-radius:20px;border:1.5px solid var(--border);background:#fff;
  font-size:12px;font-weight:600;color:var(--ink-mid);cursor:pointer;transition:all .15s}}
.rtbtn:hover{{border-color:var(--accent);color:var(--accent)}}
.rtbtn.active{{background:var(--accent);border-color:var(--accent);color:#fff}}

.card{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:18px 20px;margin-bottom:15px}}
.card-title{{font-size:11px;font-weight:700;color:var(--ink-mid);margin-bottom:3px;
  text-transform:uppercase;letter-spacing:.4px}}
.card-sub{{font-size:12px;color:var(--ink-muted);margin-bottom:12px}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:15px}}
@media(max-width:680px){{.grid-2{{grid-template-columns:1fr}}}}

.kpi-row{{display:flex;gap:11px;flex-wrap:wrap;margin-bottom:20px}}
.kpi-box{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:13px 16px;flex:1;min-width:110px}}
.kpi-val{{font-size:24px;font-weight:800;color:var(--accent);letter-spacing:-1px;line-height:1}}
.kpi-label{{font-size:11px;color:var(--ink-muted);margin-top:3px;text-transform:uppercase;letter-spacing:.3px}}

/* BAR — absolute scale, value shown, no normalisation */
.bar-wrap{{margin-bottom:8px}}
.bar-meta{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:3px}}
.bar-meta .blabel{{font-size:12px;color:var(--ink-mid);flex:1;padding-right:8px;line-height:1.3}}
.bar-meta .bval{{font-size:13px;font-weight:700;color:var(--ink);white-space:nowrap}}
.bar-track{{height:10px;background:var(--border);border-radius:5px;overflow:hidden}}
.bar-fill{{height:100%;border-radius:5px;transition:width .5s ease}}

.tbl{{width:100%;border-collapse:collapse;font-size:12.5px}}
.tbl th{{background:var(--paper);font-weight:700;text-align:left;padding:7px 10px;
  border-bottom:2px solid var(--border);color:var(--ink-mid);font-size:11px;
  text-transform:uppercase;letter-spacing:.3px}}
.tbl td{{padding:7px 10px;border-bottom:1px solid var(--border);color:var(--ink)}}
.tbl tr:last-child td{{border-bottom:none}}
.pc{{font-weight:700;color:var(--accent)}}.pc-w{{font-weight:700;color:var(--warn)}}.pc-g{{font-weight:700;color:var(--a3)}}
.hl td{{background:var(--accent-lt)}}

.insight{{border-left:3px solid var(--accent);background:var(--accent-lt);padding:10px 14px;
  border-radius:0 6px 6px 0;margin-top:12px;font-size:13px}}
.insight.warn{{border-color:var(--warn);background:var(--warn-lt)}}
.insight.green{{border-color:var(--a3);background:#edfaf5}}
.insight strong{{font-weight:700}}

.pill{{display:inline-block;padding:2px 9px;border-radius:20px;font-size:11px;font-weight:600;margin:2px}}
.pp{{background:var(--accent-lt);color:var(--accent)}}.pw{{background:var(--warn-lt);color:var(--warn)}}
.pg{{background:#edfaf5;color:var(--a3)}}.pgray{{background:#f0eff5;color:var(--ink-mid)}}

.funnel-wrap{{display:flex;flex-direction:column;align-items:center;padding:8px 0}}
.funnel-step{{position:relative;display:flex;flex-direction:column;align-items:center}}
.funnel-block{{border-radius:7px;display:flex;align-items:center;justify-content:center;
  flex-direction:column;padding:9px 12px;margin:0 auto}}
.funnel-conn{{width:2px;height:14px;background:var(--border)}}
.f-label{{font-size:10px;font-weight:700;letter-spacing:.3px;color:rgba(255,255,255,.8);text-transform:uppercase}}
.f-n{{font-size:19px;font-weight:800;color:#fff}}
.f-pct{{font-size:11px;color:rgba(255,255,255,.65)}}
.dropoff{{position:absolute;right:-85px;top:50%;transform:translateY(-50%);
  background:var(--warn-lt);color:var(--warn);border:1px solid #ffd4bf;border-radius:20px;
  padding:2px 8px;font-size:11px;font-weight:700;white-space:nowrap}}

.reco-card{{border:1.5px solid var(--border);border-radius:10px;padding:15px 17px;
  margin-bottom:11px;background:#fff;position:relative}}
.reco-num{{position:absolute;top:14px;right:16px;font-size:26px;font-weight:900;color:var(--border);line-height:1}}
.reco-tag{{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:var(--accent);margin-bottom:4px}}
.reco-title{{font-size:14px;font-weight:800;color:var(--ink);margin-bottom:4px;letter-spacing:-.2px}}
.reco-body{{font-size:13px;color:var(--ink-mid);line-height:1.6}}

.compare-row{{display:grid;grid-template-columns:165px 1fr;gap:8px;align-items:center;margin-bottom:8px}}
.cbar-item{{display:flex;align-items:center;gap:5px;font-size:11.5px;color:var(--ink-mid)}}
.minibar{{height:7px;border-radius:4px;flex-shrink:0;min-width:3px}}

.step-badge{{display:inline-flex;align-items:center;gap:6px;background:var(--accent-lt);color:var(--accent);
  border-radius:6px;padding:4px 10px;font-size:11px;font-weight:700;letter-spacing:.3px;margin-bottom:12px}}

.flow-nodes{{display:flex;align-items:flex-start;gap:0;flex-wrap:wrap;margin-top:10px}}
.flow-node{{display:flex;flex-direction:column;align-items:center;text-align:center;flex:1;min-width:76px}}
.flow-box{{width:68px;height:42px;border-radius:8px;display:flex;align-items:center;justify-content:center;
  font-size:10px;font-weight:700;text-align:center;line-height:1.2;padding:4px}}
.flow-lbl{{font-size:10px;color:var(--ink-muted);margin-top:4px;line-height:1.3;max-width:72px}}
.flow-arrow{{width:16px;height:42px;display:flex;align-items:center;justify-content:center;
  color:var(--ink-muted);font-size:12px;flex-shrink:0}}

.quote-grid{{display:flex;flex-wrap:wrap;gap:7px;margin-top:9px}}
.quote-chip{{background:var(--paper);border:1px solid var(--border);border-radius:6px;
  padding:6px 10px;font-size:12px;font-style:italic;color:var(--ink-mid)}}
</style>
</head>
<body>

<header class="site-header">
  <div style="max-width:1080px;margin:0 auto">
    <h1>Quant Survey Pipeline <span class="hbadge">Synthetic Data</span></h1>
    <p>End-to-end consumer test · Facial wash / skincare · n=306 · Awareness → Trial → Repeat</p>
  </div>
</header>

<nav class="pipeline-nav">
  <div class="ptab active" data-step="0"><span class="tnum">1</span>Study Design</div>
  <div class="ptab" data-step="1"><span class="tnum">2</span>Awareness & Funnel</div>
  <div class="ptab" data-step="2"><span class="tnum">3</span>Drivers & Barriers</div>
  <div class="ptab" data-step="3"><span class="tnum">4</span>Product Experience</div>
  <div class="ptab" data-step="4"><span class="tnum">5</span>Recommendations</div>
</nav>

<main class="main">

<!-- ═══ STEP 1 ═══ -->
<section class="step-panel active" id="step-0">
  <div class="step-badge">Stage 1 of 5 · Study Design</div>
  <h2 class="section-title">Survey Methodology</h2>
  <p class="section-sub">Quant consumer test — early trialist evaluation of a reformulated facial wash with a new brightening claim. Three-region recruitment with non-core-BUMO oversampling to isolate switching potential.</p>

  <div class="grid-2">
    <div class="card">
      <div class="card-title">Objectives</div>
      <div class="card-sub">Three diagnostic pillars driving questionnaire structure</div>
      <div style="display:flex;flex-direction:column;gap:10px;margin-top:4px">
        <div style="display:flex;gap:10px;align-items:flex-start">
          <div style="width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0">A</div>
          <div><div style="font-size:13px;font-weight:700">In-Market Effectiveness</div>
          <div style="font-size:12px;color:var(--ink-muted)">Assess GTM, promo, and media inputs driving awareness and consideration</div></div>
        </div>
        <div style="display:flex;gap:10px;align-items:flex-start">
          <div style="width:26px;height:26px;border-radius:50%;background:var(--a2);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0">B</div>
          <div><div style="font-size:13px;font-weight:700">Trial Drivers & Barriers</div>
          <div style="font-size:12px;color:var(--ink-muted)">What converts awareness to purchase — and what blocks it</div></div>
        </div>
        <div style="display:flex;gap:10px;align-items:flex-start">
          <div style="width:26px;height:26px;border-radius:50%;background:var(--a3);color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0">C</div>
          <div><div style="font-size:13px;font-weight:700">Usage Experience</div>
          <div style="font-size:12px;color:var(--ink-muted)">Satisfaction, attribute ratings, and repeat intent among trialists</div></div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Recruitment Design</div>
      <div class="card-sub">Structured to detect switching opportunity from competitor BUMOs</div>
      <table class="tbl">
        <thead><tr><th>Parameter</th><th>Spec</th></tr></thead>
        <tbody>
          <tr><td>Sample</td><td><strong>n = 306</strong></td></tr>
          <tr><td>Regions</td><td>Luzon · Visayas · Mindanao</td></tr>
          <tr><td>Quota per region</td><td>~100 respondents</td></tr>
          <tr><td>Non-core BUMO quota</td><td>≥ 80% per region</td></tr>
          <tr><td>Brightening BUMO quota</td><td>~30% target (key switching segment)</td></tr>
          <tr><td>Gender</td><td>~70% female</td></tr>
          <tr><td>Note</td><td class="pc-w">Not nationally representative</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Survey Flow</div>
    <div class="card-sub">Awareness-gated branching — three distinct respondent paths</div>
    <div class="flow-nodes">
      <div class="flow-node"><div class="flow-box" style="background:#f0eff5;color:var(--ink-mid)">Screener &amp; Demo</div><div class="flow-lbl">Skin type, category, BUMO</div></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node"><div class="flow-box" style="background:var(--accent-lt);color:var(--accent)">Awareness Gate</div><div class="flow-lbl">Heard/seen reformulated product?</div></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node"><div class="flow-box" style="background:var(--warn-lt);color:var(--warn)">Not Aware</div><div class="flow-lbl">End survey</div></div>
      <div class="flow-arrow" style="opacity:.3">·</div>
      <div class="flow-node"><div class="flow-box" style="background:#fef0ea;color:var(--warn)">Aware / Did Not Buy</div><div class="flow-lbl">Concept test + barriers</div></div>
      <div class="flow-arrow">→</div>
      <div class="flow-node"><div class="flow-box" style="background:#edfaf5;color:var(--a3)">Trialist</div><div class="flow-lbl">Full 16-attribute rating grid</div></div>
    </div>
    <div class="insight" style="margin-top:16px"><strong>Design note:</strong> Non-BUMO oversampling means aggregate rates are directional, not nationally projected. Diagnostic value is in BUMO-cut comparisons — especially the 2× trial gap between core users and the brightening segment.</div>
  </div>

  <div class="card">
    <div class="card-title">Questionnaire Structure</div>
    <div class="card-sub">5 sections · 16-attribute product grid for trialists · dual-track for non-trialists (pre-concept recall + post-concept stimulus)</div>
    <div style="display:flex;flex-wrap:wrap;gap:7px;margin-top:6px">
      <div class="pill pp">Section 1 · Demographics</div>
      <div class="pill pp">Section 2 · Skin & Category Behavior</div>
      <div class="pill pgray">Section 3 · Awareness</div>
      <div class="pill pw">Section 4 · Barriers + Concept Test (Non-Trialists)</div>
      <div class="pill pg">Section 5 · Usage Experience (Trialists)</div>
    </div>
    <div style="margin-top:11px;font-size:12px;color:var(--ink-muted)">
      Key scales: Purchase intent (5pt Likert), Product superiority vs BUMO, 16-item attribute grid (5pt), Open-ended liking/disliking drivers, Concept exposure (PI, relevance, value perception), Benefit perception pre/post stimulus.
    </div>
  </div>
</section>

<!-- ═══ STEP 2 ═══ -->
<section class="step-panel" id="step-1">
  <div class="step-badge">Stage 2 of 5 · Awareness & Funnel</div>
  <h2 class="section-title">Awareness & Conversion Funnel</h2>
  <p class="section-sub">Where the funnel collapses — and how it varies by region and BUMO group.</p>

  <div class="region-toggle">
    <span>View:</span>
    <button class="rtbtn active" data-region="National">National</button>
    <button class="rtbtn" data-region="Luzon">Luzon</button>
    <button class="rtbtn" data-region="Visayas">Visayas</button>
    <button class="rtbtn" data-region="Mindanao">Mindanao</button>
  </div>

  <div class="kpi-row" id="s2kpi"></div>

  <div class="grid-2">
    <div class="card" style="min-height:300px">
      <div class="card-title">Conversion Funnel</div>
      <div class="card-sub" id="s2funnelSub">Total n=306</div>
      <div class="funnel-wrap" id="funnelViz" style="padding-right:88px"></div>
    </div>
    <div class="card">
      <div class="card-title">Funnel by BUMO Group</div>
      <div class="card-sub" id="s2bumoSub">Awareness / Trial / Repeat (% of prior stage)</div>
      <table class="tbl" id="funnelTable"></table>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Awareness Source Mix</div>
    <div class="card-sub" id="s2chanSub">Where did aware respondents first encounter the product?</div>
    <div id="awarenessChannels" style="margin-top:4px"></div>
    <div id="s2chanInsight" class="insight"></div>
  </div>
</section>

<!-- ═══ STEP 3 ═══ -->
<section class="step-panel" id="step-2">
  <div class="step-badge">Stage 3 of 5 · Drivers & Barriers</div>
  <h2 class="section-title">Trial Drivers & Barriers</h2>
  <p class="section-sub">What converts awareness into purchase — and what blocks it.</p>

  <div class="region-toggle">
    <span>View:</span>
    <button class="rtbtn active" data-region="National">National</button>
    <button class="rtbtn" data-region="Luzon">Luzon</button>
    <button class="rtbtn" data-region="Visayas">Visayas</button>
    <button class="rtbtn" data-region="Mindanao">Mindanao</button>
  </div>

  <div class="grid-2">
    <div class="card">
      <div class="card-title">Top Trial Drivers</div>
      <div class="card-sub" id="s3driverSub">% of trialists who cited each factor</div>
      <div id="trialDriverBars"></div>
      <div class="insight green"><strong>Pattern:</strong> Sensorial first impression (texture, scent) is the dominant pull factor — ahead of advertising. In-store trial or sampling programmes may convert at higher rates than ATL-only activations.</div>
    </div>
    <div class="card">
      <div class="card-title">Top Trial Barriers</div>
      <div class="card-sub" id="s3barrierSub">% of aware non-trialists who cited each factor</div>
      <div id="trialBarrierBars"></div>
      <div class="insight warn"><strong>Pattern:</strong> Current brand loyalty dominates as a wall. But the #2 barrier — <em>claim disbelief</em> — is actionable: it signals a proof gap, not a relevance gap.</div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Benefits Sought by BUMO Segment</div>
    <div class="card-sub">Top 5 benefits each segment looks for in a facial wash</div>
    <div id="benefitsByBumo"></div>
    <div class="insight">
      <strong>Key:</strong> Brightening / Whitening users lead on brightening (82%) and dark spot reduction (83%) — the exact claim made by the reformulated product. The trial gap isn't about benefit relevance. It's about <em>whether they believe the claim</em>.
    </div>
  </div>

  <div class="card">
    <div class="card-title">Benefit Perception — Pre vs. Post Concept Exposure</div>
    <div class="card-sub">What non-trialists believe the product delivers, before and after seeing the concept stimulus</div>
    <div id="perceptionCompare"></div>
    <div class="insight warn">
      <strong>Critical finding:</strong> Before exposure, the product is read as a functional facial wash — oil control and deep cleansing dominate perception. Brightening is at 9%. Even after the concept, functional cues remain strong — the product equity is working against its beauty claim.
    </div>
  </div>
</section>

<!-- ═══ STEP 4 ═══ -->
<section class="step-panel" id="step-3">
  <div class="step-badge">Stage 4 of 5 · Product Experience</div>
  <h2 class="section-title">Product Experience <span style="font-size:14px;font-weight:400;color:var(--ink-muted)">(Trialists only · n=<span id="trialistN"></span>)</span></h2>
  <p class="section-sub">Satisfaction, attribute performance, and repeat drivers among respondents who purchased and used the product.</p>

  <div class="kpi-row" id="s4kpi"></div>

  <div class="grid-2">
    <div class="card">
      <div class="card-title">Overall Product Rating</div>
      <div class="card-sub">Considering everything about the product, how would you describe it?</div>
      <div id="oarChart"></div>
      <div class="quote-grid">
        <div class="quote-chip">"feels refreshing naman"</div>
        <div class="quote-chip">"mukha kang fresh after"</div>
        <div class="quote-chip">"malambot ang pakiramdam"</div>
        <div class="quote-chip">"mabango"</div>
        <div class="quote-chip">"nagbago yung skin ko over time"</div>
        <div class="quote-chip">"parang napaka-dry after"</div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Suggested Improvements</div>
      <div class="card-sub">What would make you more likely to repurchase? (% of trialists)</div>
      <div id="improvementBars"></div>
      <div class="insight warn"><strong>Formulation flag:</strong> Dryness leads improvement requests by a wide margin — and directly undermines the brightening/skin-health positioning. A product claiming skin radiance cannot leave skin feeling tight after washing.</div>
    </div>
  </div>

  <div class="card">
    <div class="card-title">Attribute Rating Grid — % rated Excellent (T1 Box)</div>
    <div class="card-sub">16 attributes rated 1–5. Functional/wash attributes lead; beauty-outcome attributes (brightening, dark spots, hydration) trail. This mirrors the claim credibility gap seen in non-trialists.</div>
    <div id="attrGrid" style="margin-top:6px"></div>
  </div>

  <div class="card">
    <div class="card-title">Repeat Purchase Intent</div>
    <div class="card-sub">How likely are you to buy this product again?</div>
    <div id="repeatChart"></div>
  </div>
</section>

<!-- ═══ STEP 5 ═══ -->
<section class="step-panel" id="step-4">
  <div class="step-badge">Stage 5 of 5 · Recommendations</div>
  <h2 class="section-title">Strategic Recommendations</h2>
  <p class="section-sub">Data-grounded actions from funnel diagnostics, benefit perception gaps, and trialist experience.</p>

  <div class="card" style="background:var(--ink);border-color:var(--ink);margin-bottom:20px">
    <div style="font-size:11px;font-weight:700;letter-spacing:.5px;color:var(--ink-muted);text-transform:uppercase;margin-bottom:6px">Key Finding</div>
    <div style="font-size:17px;font-weight:800;color:#fff;line-height:1.4;letter-spacing:-.3px">
      Despite 67% awareness, trial collapses at 20% among Brightening-segment users — not because the product fails, but because the brightening claim <em style="color:var(--accent-lt)">isn't believed</em> against a product still perceived as a functional/oil-control wash.
    </div>
    <div style="margin-top:9px;font-size:13px;color:var(--ink-muted)">Trialists rate the product well once used. This is a communication and credibility gap, not a product failure.</div>
  </div>

  <div class="reco-card">
    <div class="reco-num">01</div>
    <div class="reco-tag">Communication · Claim Proof</div>
    <div class="reco-title">Build visible proof architecture for the brightening claim</div>
    <div class="reco-body">"Not convinced the brightening claim is real" is the #2 trial barrier among aware non-trialists. For beauty-segment users who have seen brightening claims fail before, assertion is not enough. The creative needs to close the credibility gap — not just repeat the claim.
      <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:6px">
        <span class="pill pw">Claim believability gap</span>
        <span style="font-size:12px;color:var(--ink-muted)">→</span>
        <span class="pill pg">Before/after visual · ingredient RTB · dermatologist signal</span>
      </div>
    </div>
  </div>

  <div class="reco-card">
    <div class="reco-num">02</div>
    <div class="reco-tag">Communication · Benefit Framing</div>
    <div class="reco-title">Lead with "soft and hydrated skin" as the felt bridge to brightening</div>
    <div class="reco-body">Trialists who repeat cite skin softness as the sensorial confirmation that the product is working. Leading with post-wash feel ("hindi natutuyo, malambot") before the visual outcome ("mas maliwanag") may convert skeptics more effectively than a direct visual claim.
      <div class="insight green" style="margin-top:8px"><strong>Language note:</strong> "Maliwanag ang balat" can read as whitening. "Mas malusog at makinang na balat" or "healthy skin glow" may land the brightening equity without whitening connotations.</div>
    </div>
  </div>

  <div class="reco-card">
    <div class="reco-num">03</div>
    <div class="reco-tag">Product · Formulation</div>
    <div class="reco-title">Resolve post-wash dryness — it's undermining the skin-health claim</div>
    <div class="reco-body">Dryness leads improvement requests at 54% of trialists. "Skin feels hydrated (not tight)" is the lowest-rated product attribute at 39% T1 box — 56 points below the top functional attribute. A product claiming skin radiance that leaves skin feeling tight cannot hold the beauty positioning.
      <div class="insight warn" style="margin-top:8px"><strong>Priority:</strong> Brightening-segment trialists rate visual skin outcomes lower than core users — formulation feel is likely driving their skepticism more than the product's actual performance.</div>
    </div>
  </div>

  <div class="reco-card">
    <div class="reco-num">04</div>
    <div class="reco-tag">GTM · Visayas Distribution</div>
    <div class="reco-title">Fix Visayas distribution before adding ATL — awareness is a channel problem, not a media problem</div>
    <div class="reco-body">Visayas awareness sits ~11 points below national average (57% vs 68%). TV reach is already active there. The gap is in physical channel presence — drugstore shelf space and supermarket display — where the product is less visible than in Luzon.
      <div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:6px">
        <span class="pill pw">Visayas awareness: 57% vs 68% nat'l</span>
        <span class="pill pg">Action: Drugstore + supermarket display push</span>
      </div>
    </div>
  </div>

  <div class="card" style="margin-top:6px">
    <div class="card-title">Hypothesis Test Summary</div>
    <div class="card-sub">Three hypotheses tested for the trial drop-off among Brightening-segment users</div>
    <table class="tbl">
      <thead><tr><th>Hypothesis</th><th>Evidence</th><th>Verdict</th></tr></thead>
      <tbody>
        <tr>
          <td><strong>H1:</strong> Brightening benefit isn't what this segment wants</td>
          <td>Brightening BUMO: brightening (82%), dark spots (83%) — claim IS their #1 need</td>
          <td><span class="pill pg">Confirmed — relevant</span></td>
        </tr>
        <tr>
          <td><strong>H2:</strong> The brightening claim isn't believed</td>
          <td>#2 trial barrier; pre-concept perception: brightening at only 9%</td>
          <td><span class="pill pw">Confirmed — credibility gap</span></td>
        </tr>
        <tr>
          <td><strong>H3:</strong> Functional product equity blocks the beauty claim</td>
          <td>Non-trialists read product as oil-control/deep cleanse wash even after concept exposure</td>
          <td><span class="pill pw">Confirmed — equity mismatch</span></td>
        </tr>
        <tr class="hl">
          <td colspan="2"><strong>Product quality is not the problem</strong> — OAR Excellent: 53%, better than BUMO: 83%</td>
          <td><span class="pill pg">Strong delivery</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

</main>
<script>
const D = {DJ};

/* ── bar helper: absolute scale 0–100 ───────────────────────────────────── */
function bar(label, pct, color) {{
  const w = Math.min(Math.max(pct, 0), 100);
  return `<div class="bar-wrap">
    <div class="bar-meta">
      <div class="blabel">${{label}}</div>
      <div class="bval">${{pct}}%</div>
    </div>
    <div class="bar-track"><div class="bar-fill" style="width:${{w}}%;background:${{color}}"></div></div>
  </div>`;
}}

/* ── region state ────────────────────────────────────────────────────────── */
let s2Region = 'National';
let s3Region = 'National';

/* ── TAB NAVIGATION ──────────────────────────────────────────────────────── */
document.querySelectorAll('.ptab').forEach(tab => {{
  tab.addEventListener('click', () => {{
    document.querySelectorAll('.ptab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.step-panel').forEach(p=>p.classList.remove('active'));
    tab.classList.add('active');
    const step = parseInt(tab.dataset.step);
    document.getElementById('step-'+step).classList.add('active');
    window.scrollTo({{top:0,behavior:'smooth'}});
    if(step===1) renderS2(s2Region);
    if(step===2) renderS3(s3Region);
    if(step===3) renderS4();
  }});
}});

/* ── REGION TOGGLES ──────────────────────────────────────────────────────── */
document.querySelectorAll('#step-1 .rtbtn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('#step-1 .rtbtn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    s2Region = btn.dataset.region;
    renderS2(s2Region);
  }});
}});
document.querySelectorAll('#step-2 .rtbtn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('#step-2 .rtbtn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    s3Region = btn.dataset.region;
    renderS3(s3Region);
  }});
}});

/* ═══════════════════════════════════════════════════════════════════════════
   STEP 2 — AWARENESS & FUNNEL
════════════════════════════════════════════════════════════════════════════ */
function renderS2(region) {{
  const isNat = region === 'National';
  const rd = isNat ? null : D.regional[region];

  // KPIs
  if (isNat) {{
    document.getElementById('s2kpi').innerHTML = [
      [D.total_n,       'Total respondents'],
      [D.aware_n+' ('+D.aware_pct+'%)', 'Aware'],
      [D.trial_n+' ('+D.trial_pct+'%)', 'Trial rate (of aware)'],
      [D.repeat_n+' ('+D.repeat_pct+'%)', 'Repeat rate (of trialists)'],
    ].map(([v,l])=>`<div class="kpi-box"><div class="kpi-val">${{v}}</div><div class="kpi-label">${{l}}</div></div>`).join('');
  }} else {{
    document.getElementById('s2kpi').innerHTML = [
      [rd.n,                  region+' respondents'],
      [rd.aware_pct+'%',      'Awareness rate'],
      [rd.trial_pct+'%',      'Trial rate (of aware)'],
      [region==='Visayas'?'⚠ Below national avg':'—', region==='Visayas'?'Awareness gap flagged':''],
    ].map(([v,l])=>`<div class="kpi-box"><div class="kpi-val">${{v}}</div><div class="kpi-label">${{l}}</div></div>`).join('');
  }}

  // Funnel viz (national only; regional shows bar chart instead)
  const funnelEl = document.getElementById('funnelViz');
  document.getElementById('s2funnelSub').textContent = isNat ? 'Total n=306' : region+' funnel (all BUMOs)';
  if (isNat) {{
    const stages = [
      {{lbl:'Total',  n:D.total_n,  sub:'100%',                   color:'#5346c8',w:260}},
      {{lbl:'Aware',  n:D.aware_n,  sub:D.aware_pct+'%',           color:'#7a6fd4',w:195, drop:Math.round(100-D.aware_pct)+'% not aware'}},
      {{lbl:'Trial',  n:D.trial_n,  sub:D.trial_pct+'% of aware',  color:'#d95b2a',w:134, drop:Math.round(100-D.trial_pct)+'% drop-off ↑ key gap'}},
      {{lbl:'Repeat', n:D.repeat_n, sub:D.repeat_pct+'% of tri.',  color:'#1aaa78',w:96,  drop:Math.round(100-D.repeat_pct)+'% one-time only'}},
    ];
    funnelEl.innerHTML = stages.map((s,i)=>`
      <div class="funnel-step">
        ${{i?'<div class="funnel-conn"></div>':''}}
        <div class="funnel-block" style="background:${{s.color}};width:${{s.w}}px">
          <div class="f-label">${{s.lbl}}</div><div class="f-n">${{s.n}}</div><div class="f-pct">${{s.sub}}</div>
        </div>
        ${{s.drop?`<div class="dropoff">▼ ${{s.drop}}</div>`:''}}
      </div>`).join('');
  }} else {{
    // Regional: show BUMO breakdown bars
    const rb = D.regional_bumo[region];
    funnelEl.innerHTML = '<div style="width:100%">' +
      Object.entries(rb).map(([bumo, bdata]) =>
        `<div style="margin-bottom:12px">
          <div style="font-size:11px;font-weight:700;color:var(--ink-mid);margin-bottom:4px">${{bumo}}<span style="font-size:10px;color:var(--ink-muted);margin-left:6px">n=${{bdata.n}}</span></div>
          ${{bar('Aware', bdata.aware_pct, 'var(--accent)')}}
          ${{bar('Trial (of aware)', bdata.trial_pct, 'var(--a3)')}}
        </div>`
      ).join('') + '</div>';
  }}

  // BUMO funnel table
  document.getElementById('s2bumoSub').textContent = isNat ? 'Awareness / Trial / Repeat (% of prior stage)' : region+' · BUMO awareness & trial rates';
  const bumos = Object.entries(D.funnel_by_bumo);
  document.getElementById('funnelTable').innerHTML =
    `<thead><tr><th>BUMO Segment</th><th>n</th><th>Aware %</th><th>Trial %</th><th>Repeat %</th></tr></thead><tbody>`+
    bumos.map(([nm,d])=>`<tr ${{nm.includes('Bright')?'class="hl"':''}}>
      <td><strong>${{nm}}</strong></td><td>${{d.total}}</td>
      <td class="${{d.aware_pct<60?'pc-w':'pc'}}">${{d.aware_pct}}%</td>
      <td class="${{d.trial_pct<20?'pc-w':'pc-g'}}">${{d.trial_pct}}%</td>
      <td class="${{d.repeat_pct===0?'pc-w':'pc'}}">${{d.repeat_pct}}%</td>
    </tr>`).join('')+'</tbody>';

  // Awareness channels
  const channels = isNat ? D.awareness_channels : D.regional_channels[region];
  const chanN = isNat ? D.aware_n : D.regional[region].n;
  document.getElementById('s2chanSub').textContent = `Where did aware respondents first encounter the product? (n=~${{chanN}})`;
  const chanColors = ['#5346c8','#5346c8','#7a6fd4','#c2488a','#c2488a','#8888a8','#8888a8','#aaa'];
  document.getElementById('awarenessChannels').innerHTML =
    channels.slice(0,7).map(([ch,n], i) => {{
      const p = Math.round(n / (isNat?D.aware_n:D.regional[region].n) * 100);
      return bar(ch, p, chanColors[i] || '#8888a8');
    }}).join('');

  const insights = {{
    'National': '<strong>Read:</strong> Supermarket display and TV are near-equal as top touchpoints — reflecting the drugstore/supermarket purchase journey for facial wash. Beauty influencer and TikTok are secondary but growing, particularly among the brightening segment.',
    'Luzon': '<strong>Luzon:</strong> TV and supermarket display both strong. Digital (TikTok, influencers) also over-indexed vs. national — suggesting Luzon consumers are more receptive to digital touchpoints for skincare discovery.',
    'Visayas': '<strong>Visayas flag:</strong> Supermarket display dominates but total aware base is smaller. TV reach is present — the gap is in physical availability, not media weight. More shelf presence needed before adding ATL spend.',
    'Mindanao': '<strong>Mindanao:</strong> TV remains the primary awareness driver. Digital channels under-index vs. national, suggesting ATL-first strategy remains appropriate for this region. Distribution in drugstores is the secondary lever.'
  }};
  document.getElementById('s2chanInsight').innerHTML = insights[region] || '';
}}

/* ═══════════════════════════════════════════════════════════════════════════
   STEP 3 — DRIVERS & BARRIERS
════════════════════════════════════════════════════════════════════════════ */
function renderS3(region) {{
  const isNat = region === 'National';

  // Drivers
  const drivers = isNat ? D.trial_drivers : D.regional_drivers[region].map(([l,n]) => [l,n,0]);
  const triN = isNat ? D.trial_n : D.regional[region].n;
  document.getElementById('s3driverSub').textContent = `% of trialists who cited each factor${{''}}`+(isNat?` (n=${{D.trial_n}})`:`(${{region}})`);
  document.getElementById('trialDriverBars').innerHTML = drivers.map(([lbl,n,pct]) => {{
    const p = isNat ? pct : Math.round(n/Math.max(triN*0.25,1)*100);
    const displayP = isNat ? pct : Math.round(n/D.regional[region].n*100);
    return bar(lbl, isNat ? pct : displayP, 'var(--a3)');
  }}).join('');

  // Barriers — absolute scale, shows the dominance clearly
  const nonTriN = D.aware_n - D.trial_n;
  const barriers = isNat ? D.trial_barriers : D.regional_barriers[region].map(([l,n]) => [l,n,0]);
  document.getElementById('s3barrierSub').textContent = `% of aware non-trialists who cited each factor`+(isNat?` (n=${{nonTriN}})`:`(${{region}})`);
  document.getElementById('trialBarrierBars').innerHTML = barriers.map(([lbl,n,pct]) => {{
    const displayP = isNat ? pct : Math.round(n/Math.max(D.regional[region].n*0.65,1)*100);
    return bar(lbl, isNat ? pct : displayP, 'var(--warn)');
  }}).join('');

  // Benefits by BUMO — static (no regional cut)
  const colors = ['var(--accent)','var(--a2)','#e0891a','var(--a3)'];
  document.getElementById('benefitsByBumo').innerHTML =
    `<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-top:8px">`+
    Object.keys(D.benefits_by_bumo).map((nm,idx) => {{
      const bens = Object.entries(D.benefits_by_bumo[nm]);
      return `<div>
        <div style="font-size:11px;font-weight:700;color:${{colors[idx]}};margin-bottom:6px;text-transform:uppercase;letter-spacing:.3px">${{nm}}</div>
        ${{bens.map(([b,p]) => `
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;font-size:12px">
            <span style="color:var(--ink-mid)">${{b}}</span>
            <div style="display:flex;align-items:center;gap:5px">
              <div style="width:60px;height:6px;background:var(--border);border-radius:3px;overflow:hidden">
                <div style="height:100%;background:${{colors[idx]}};border-radius:3px;width:${{p}}%"></div>
              </div>
              <span style="font-weight:700;font-size:12px;min-width:32px;text-align:right">${{p}}%</span>
            </div>
          </div>`).join('')}}
      </div>`;
    }}).join('') + '</div>';

  // Benefit perception — static
  const bens = Object.keys(D.benefit_perception.pre);
  const maxAll = Math.max(...Object.values(D.benefit_perception.pre), ...Object.values(D.benefit_perception.post));
  document.getElementById('perceptionCompare').innerHTML =
    `<div style="margin-top:10px">
    <div style="display:flex;gap:14px;margin-bottom:10px;font-size:12px">
      <span style="display:flex;align-items:center;gap:5px"><span style="display:inline-block;width:11px;height:7px;border-radius:3px;background:#c0bcd8"></span>Before concept</span>
      <span style="display:flex;align-items:center;gap:5px"><span style="display:inline-block;width:11px;height:7px;border-radius:3px;background:var(--accent)"></span>After concept</span>
    </div>`+
    bens.map(b => {{
      const pre = D.benefit_perception.pre[b]||0, post = D.benefit_perception.post[b]||0;
      return `<div class="compare-row" style="margin-bottom:8px">
        <div style="font-size:12px;color:var(--ink-mid)">${{b}}</div>
        <div>
          <div class="cbar-item"><div class="minibar" style="width:${{Math.max(pre/maxAll*200,3)}}px;background:#c0bcd8"></div><span>${{pre}}%</span></div>
          <div class="cbar-item" style="margin-top:3px"><div class="minibar" style="width:${{Math.max(post/maxAll*200,3)}}px;background:var(--accent)"></div><span>${{post}}%</span></div>
        </div>
      </div>`;
    }}).join('') + '</div>';
}}

/* ═══════════════════════════════════════════════════════════════════════════
   STEP 4 — PRODUCT EXPERIENCE
════════════════════════════════════════════════════════════════════════════ */
function renderS4() {{
  document.getElementById('trialistN').textContent = D.trial_n;
  document.getElementById('s4kpi').innerHTML = [
    ['53%',    'OAR Excellent (T1 Box)'],
    [(D.superiority['Better than BUMO']||0)+'%', 'Better than own BUMO'],
    [(D.repeat_intent['Definitely would buy again']||0)+'%', 'Definite repeat intent'],
    ['54%',    'Cite post-wash dryness as issue'],
  ].map(([v,l])=>`<div class="kpi-box"><div class="kpi-val">${{v}}</div><div class="kpi-label">${{l}}</div></div>`).join('');

  const oarLbl = {{5:'Excellent',4:'Very Good',3:'Good',2:'Fair',1:'Poor'}};
  const oarClr = {{5:'var(--a3)',4:'var(--accent)',3:'var(--ink-mid)',2:'var(--warn)',1:'#c00'}};
  document.getElementById('oarChart').innerHTML =
    Object.entries(D.oar_distribution).sort((a,b)=>b[0]-a[0])
    .map(([k,v])=>bar(oarLbl[k], v, oarClr[k])).join('');

  document.getElementById('improvementBars').innerHTML =
    D.improvements.map(([lbl,n,pct])=>bar(lbl, pct, 'var(--warn)')).join('');

  const attrs = Object.entries(D.attr_ratings).sort((a,b)=>b[1].t1_pct-a[1].t1_pct);
  document.getElementById('attrGrid').innerHTML = attrs.map(([attr,d]) => {{
    const clr = d.t1_pct < 55 ? 'var(--warn)' : d.t1_pct >= 80 ? 'var(--a3)' : 'var(--accent)';
    return bar(attr, d.t1_pct, clr);
  }}).join('');

  const riOrder = ['Definitely would buy again','Probably would buy again','Might or might not','Probably would not','Definitely would not'];
  const riClr   = ['var(--a3)','var(--accent)','var(--ink-mid)','var(--warn)','#c00'];
  document.getElementById('repeatChart').innerHTML =
    riOrder.map((k,i)=>bar(k, D.repeat_intent[k]||0, riClr[i])).join('');
}}

/* ── INIT ──────────────────────────────────────────────────────────────────── */
renderS2('National');
</script>
</body>
</html>"""

out = os.path.join(BASE,"index.html")
with open(out,"w",encoding="utf-8") as f: f.write(HTML)
print(f"✓ Built index.html ({len(HTML):,} chars)")
