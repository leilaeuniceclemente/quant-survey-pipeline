"""
Script 01 — Synthetic Respondent Data Generator
Quant Survey Pipeline | Portfolio Tool
Category: Facial Wash / Skincare
BUMO groups: Core (anti-acne/functional), Brightening (beauty-whitening target),
             Anti-aging, Other
"""

import csv, random, json, os

random.seed(42)
N = 306

BUMO_GROUPS = {
    "Functional / Anti-acne": {"n": 64,  "aware_rate": 0.78, "trial_rate": 0.44, "repeat_rate": 0.45},
    "Brightening / Whitening": {"n": 95,  "aware_rate": 0.72, "trial_rate": 0.22, "repeat_rate": 0.40},
    "Anti-aging / Moisture":   {"n": 62,  "aware_rate": 0.55, "trial_rate": 0.04, "repeat_rate": 0.00},
    "Multi-benefit / Other":   {"n": 85,  "aware_rate": 0.60, "trial_rate": 0.15, "repeat_rate": 0.30},
}

REGIONS   = ["Luzon", "Visayas", "Mindanao"]
GENDERS   = ["Female", "Male"]
AGE_BANDS = ["18–24", "25–35", "36–45", "46–59"]
INCOME_BANDS = [
    "PHP 10,001–18,000","PHP 18,001–25,000","PHP 25,001–40,000",
    "PHP 40,001–60,000","PHP 60,001–100,000","PHP 100,001+"
]

AWARENESS_CHANNELS = [
    "TV ad", "Supermarket display", "Drugstore display",
    "TikTok", "Facebook", "Beauty influencer", "YouTube",
    "Family / Friends", "Online shopping site", "Radio", "In-store demo"
]
AWARENESS_WEIGHTS         = [0.35, 0.26, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01, 0.00]
AWARENESS_WEIGHTS_VISAYAS = [0.22, 0.33, 0.16, 0.05, 0.09, 0.04, 0.03, 0.04, 0.02, 0.01, 0.01]

BENEFITS_SOUGHT = [
    "Brightens / evens skin tone", "Reduces dark spots & hyperpigmentation",
    "Keeps skin hydrated", "Controls excess oil", "Prevents breakouts",
    "Gentle / non-irritating", "Deep cleansing", "Anti-aging / firming", "Smells pleasant"
]

BENEFIT_PERCEPTION_LABELS = [
    "Brightens skin tone", "Keeps skin hydrated",
    "Controls oil / prevents breakouts", "Deep cleansing",
    "Reduces dark spots", "Gentle on skin"
]

TRIAL_DRIVERS = [
    "Liked / related to TV ad",
    "Liked price for perceived benefit",
    "Liked the product texture or scent",
    "Product addresses my skin needs",
    "Attractive packaging",
    "Easy to find in store",
    "Recommended by friends / family",
    "Recommended by beauty influencer"
]

TRIAL_BARRIERS = [
    "Already satisfied with current facial wash",
    "Not convinced the brightening claim is real",
    "Did not like / relate to TV ad",
    "Not recommended by friends / family",
    "Difficult to find in store",
    "Price too high for perceived benefit",
    "Did not like / relate to TikTok content",
    "Packaging not appealing"
]

# Weights tuned so barriers show strong spread: #1 dominant, rest much smaller
BARRIER_WEIGHTS = {
    "Functional / Anti-acne":   [0.19, 0.10, 0.20, 0.13, 0.08, 0.09, 0.05, 0.04],
    "Brightening / Whitening":  [0.42, 0.22, 0.10, 0.11, 0.10, 0.07, 0.08, 0.05],
    "Anti-aging / Moisture":    [0.55, 0.18, 0.09, 0.08, 0.12, 0.10, 0.06, 0.04],
    "Multi-benefit / Other":    [0.48, 0.15, 0.12, 0.09, 0.10, 0.08, 0.05, 0.04],
}

# Trial driver weights: bigger spread so top driver clearly dominates
DRIVER_WEIGHTS = {
    "Functional / Anti-acne":   [0.55, 0.35, 0.22, 0.38, 0.18, 0.28, 0.14, 0.10],
    "Brightening / Whitening":  [0.30, 0.40, 0.45, 0.42, 0.22, 0.20, 0.18, 0.28],
    "Anti-aging / Moisture":    [0.32, 0.28, 0.30, 0.38, 0.16, 0.22, 0.14, 0.16],
    "Multi-benefit / Other":    [0.38, 0.28, 0.28, 0.32, 0.18, 0.22, 0.16, 0.14],
}

PRODUCT_ATTRIBUTES = [
    "Suitable for daily use",
    "Rinses off cleanly",
    "Controls oil throughout the day",
    "Deep cleansing feel",
    "Refreshing feel during wash",
    "Gentle / non-irritating on skin",
    "Easy to lather",
    "Attractive packaging",
    "Pleasant scent",
    "Leaves skin feeling soft",
    "Skin looks brighter after wash",
    "Reduces appearance of dark spots",
    "Skin feels hydrated (not tight)",
    "Long-lasting matte finish",
    "Suitable for sensitive skin",
    "Visibly improved skin texture over time",
]

ATTR_T1_BASE = {
    "Suitable for daily use":                  0.91,
    "Rinses off cleanly":                      0.89,
    "Controls oil throughout the day":         0.85,
    "Deep cleansing feel":                     0.83,
    "Refreshing feel during wash":             0.87,
    "Gentle / non-irritating on skin":         0.80,
    "Easy to lather":                          0.82,
    "Attractive packaging":                    0.74,
    "Pleasant scent":                          0.72,
    "Leaves skin feeling soft":                0.66,
    "Skin looks brighter after wash":          0.58,
    "Reduces appearance of dark spots":        0.52,
    "Skin feels hydrated (not tight)":         0.55,
    "Long-lasting matte finish":               0.60,
    "Suitable for sensitive skin":             0.70,
    "Visibly improved skin texture over time": 0.50,
}

IMPROVEMENT_AREAS = [
    "Improve moisturising effect — skin feels dry after use",
    "Strengthen brightening result — visible change takes too long",
    "Add more active skin ingredients",
    "Offer more promotions / discounts",
    "Improve the scent",
    "Make product easier to find in stores",
]
IMPROVEMENT_WEIGHTS = [0.54, 0.32, 0.20, 0.16, 0.12, 0.10]

PURCHASE_CHANNELS = ["Supermarket","Drugstore","E-commerce","Convenience store","Beauty specialty store"]
PACK_SIZES        = ["50ml travel","100ml","100ml twin-pack","150ml","200ml"]
TIME_SINCE        = ["Less than 1 week","1–2 weeks ago","1 month ago","2 months ago","3 months ago","More than 3 months"]

# Benefits sought by BUMO — Brightening segment now strongly leads on brightening/dark spots
BUMO_BENEFIT_WEIGHTS = {
    "Functional / Anti-acne": {
        "Brightens / evens skin tone": 0.22, "Reduces dark spots & hyperpigmentation": 0.18,
        "Keeps skin hydrated": 0.48, "Controls excess oil": 0.80,
        "Prevents breakouts": 0.78, "Gentle / non-irritating": 0.65,
        "Deep cleansing": 0.85, "Anti-aging / firming": 0.10, "Smells pleasant": 0.28
    },
    "Brightening / Whitening": {
        "Brightens / evens skin tone": 0.82, "Reduces dark spots & hyperpigmentation": 0.75,
        "Keeps skin hydrated": 0.52, "Controls excess oil": 0.30,
        "Prevents breakouts": 0.22, "Gentle / non-irritating": 0.44,
        "Deep cleansing": 0.32, "Anti-aging / firming": 0.18, "Smells pleasant": 0.45
    },
    "Anti-aging / Moisture": {
        "Brightens / evens skin tone": 0.40, "Reduces dark spots & hyperpigmentation": 0.35,
        "Keeps skin hydrated": 0.88, "Controls excess oil": 0.20,
        "Prevents breakouts": 0.15, "Gentle / non-irritating": 0.75,
        "Deep cleansing": 0.30, "Anti-aging / firming": 0.90, "Smells pleasant": 0.35
    },
    "Multi-benefit / Other": {
        "Brightens / evens skin tone": 0.45, "Reduces dark spots & hyperpigmentation": 0.38,
        "Keeps skin hydrated": 0.50, "Controls excess oil": 0.48,
        "Prevents breakouts": 0.40, "Gentle / non-irritating": 0.45,
        "Deep cleansing": 0.52, "Anti-aging / firming": 0.25, "Smells pleasant": 0.38
    }
}

# Pre-concept: product perceived as functional wash (oil/breakout), NOT brightening
BENEFIT_PERCEPTION_W_PRE = {
    "Brightens skin tone": 0.09, "Keeps skin hydrated": 0.08,
    "Controls oil / prevents breakouts": 0.68, "Deep cleansing": 0.52,
    "Reduces dark spots": 0.06, "Gentle on skin": 0.10,
}
# Post-concept: brightening jumps but functional cues still strong
BENEFIT_PERCEPTION_W_POST = {
    "Brightens skin tone": 0.55, "Keeps skin hydrated": 0.38,
    "Controls oil / prevents breakouts": 0.72, "Deep cleansing": 0.48,
    "Reduces dark spots": 0.35, "Gentle on skin": 0.28,
}

# Regional config
REGION_WEIGHTS = {"Luzon": 0.40, "Visayas": 0.30, "Mindanao": 0.30}
REGION_AWARE_MODIFIER = {"Luzon": 1.0, "Visayas": 0.84, "Mindanao": 0.95}
REGION_TRIAL_MODIFIER = {"Luzon": 1.05, "Visayas": 1.10, "Mindanao": 0.90}

# ── helpers ──────────────────────────────────────────────────────────────────
def weighted_choice(choices, weights):
    total = sum(weights); r = random.uniform(0, total); upto = 0
    for c, w in zip(choices, weights):
        upto += w
        if r <= upto: return c
    return choices[-1]

def attribute_rating(base, var=0.10):
    adj = base * random.uniform(1-var, 1+var); r = random.random()
    if r < adj: return 5
    elif r < adj+0.15: return 4
    elif r < adj+0.30: return 3
    elif r < adj+0.40: return 2
    return 1

def attr_key(attr):
    return "rating_" + attr[:28].replace(" ","_").replace("/","").replace("(","").replace(")","").lower()

# ── build rows ────────────────────────────────────────────────────────────────
rows = []
resp_id = 1000

for bumo, cfg in BUMO_GROUPS.items():
    for _ in range(cfg["n"]):
        r = {}
        r["respondent_id"] = f"R{resp_id}"; resp_id += 1
        r["bumo"] = bumo
        r["region"] = random.choices(REGIONS, weights=[REGION_WEIGHTS[rg] for rg in REGIONS])[0]
        r["gender"] = random.choices(GENDERS, weights=[0.70, 0.30])[0]
        r["age_band"] = random.choices(AGE_BANDS, weights=[0.25, 0.38, 0.25, 0.12])[0]
        r["income_band"] = random.choices(INCOME_BANDS, weights=[0.18,0.27,0.23,0.16,0.11,0.05])[0]
        r["household_size"] = random.randint(2, 6)
        r["wash_freq_per_day"] = random.choices([1,2,3], weights=[0.20,0.62,0.18])[0]
        r["skin_type"] = random.choices(
            ["Oily","Dry","Combination","Normal","Sensitive"],
            weights=[0.32,0.18,0.30,0.12,0.08])[0]

        bw = BUMO_BENEFIT_WEIGHTS[bumo]
        bens = [b for b in BENEFITS_SOUGHT if random.random() < bw[b]]
        if not bens: bens = [max(bw, key=bw.get)]
        r["benefits_sought"] = "|".join(bens[:3])

        # Awareness with regional modifier
        aware_base = cfg["aware_rate"] * REGION_AWARE_MODIFIER[r["region"]]
        r["is_aware"] = random.random() < aware_base

        if not r["is_aware"]:
            r["awareness_channel"] = ""; r["familiarity"] = "Not aware"
            r["is_trialist"] = False; r["is_repeater"] = False
        else:
            aw_w = AWARENESS_WEIGHTS_VISAYAS if r["region"] == "Visayas" else AWARENESS_WEIGHTS
            r["awareness_channel"] = weighted_choice(AWARENESS_CHANNELS, aw_w)
            trial_base = cfg["trial_rate"] * REGION_TRIAL_MODIFIER[r["region"]]
            r["is_trialist"] = random.random() < trial_base
            if r["is_trialist"]:
                r["familiarity"] = random.choices(
                    ["Bought within past 3 months","Regular buyer"], weights=[0.65,0.35])[0]
                r["is_repeater"] = random.random() < cfg["repeat_rate"]
            else:
                r["familiarity"] = random.choices(
                    ["Seen/heard, don't want to buy","Seen/heard, considering but haven't bought"],
                    weights=[0.45,0.55])[0]
                r["is_repeater"] = False

        if r["is_trialist"]:
            tdw = DRIVER_WEIGHTS[bumo]
            drivers = [d for d,w in zip(TRIAL_DRIVERS, tdw) if random.random() < w]
            if not drivers: drivers = [TRIAL_DRIVERS[2]]
            r["trial_drivers"] = "|".join(drivers[:3])
            r["trial_barriers"] = ""

            r["purchase_channel"] = random.choices(
                PURCHASE_CHANNELS, weights=[0.38,0.32,0.14,0.08,0.08])[0]
            r["pack_size_bought"] = random.choices(
                PACK_SIZES, weights=[0.10,0.44,0.16,0.20,0.10])[0]
            r["time_since_last_purchase"] = random.choices(
                TIME_SINCE, weights=[0.22,0.13,0.33,0.07,0.02,0.09])[0]
            r["time_since_last_use"] = random.choices(
                TIME_SINCE, weights=[0.30,0.09,0.41,0.04,0.02,0.13])[0]

            for attr in PRODUCT_ATTRIBUTES:
                base = ATTR_T1_BASE[attr]
                if bumo == "Brightening / Whitening" and attr in [
                    "Skin looks brighter after wash","Reduces appearance of dark spots",
                    "Skin feels hydrated (not tight)","Visibly improved skin texture over time"]:
                    base *= 0.80
                r[attr_key(attr)] = attribute_rating(base)

            r["overall_product_rating"] = random.choices(
                [5,4,3,2,1], weights=[0.53,0.25,0.14,0.06,0.02])[0]
            sup_w = {
                "Functional / Anti-acne":   [0.91,0.09,0],
                "Brightening / Whitening":  [0.78,0.20,0.02],
                "Anti-aging / Moisture":    [0.80,0.20,0],
                "Multi-benefit / Other":    [0.82,0.18,0]
            }
            r["product_superiority"] = random.choices(
                ["Better than BUMO","Same as BUMO","Worse than BUMO"],
                weights=sup_w[bumo])[0]
            r["repeat_intent"] = random.choices(
                ["Definitely would buy again","Probably would buy again",
                 "Might or might not","Probably would not","Definitely would not"],
                weights=[0.44,0.30,0.14,0.08,0.04])[0]
            r["recommend_intent"] = random.choices(
                ["Definitely would recommend","Probably would recommend",
                 "Might or might not","Probably would not","Definitely would not"],
                weights=[0.42,0.33,0.16,0.06,0.03])[0]

            bp_w = BENEFIT_PERCEPTION_W_POST
            bp_post = [b for b,w in bp_w.items() if random.random() < w]
            r["benefit_perception_post"] = "|".join(bp_post[:2]) if bp_post else "Deep cleansing"

            imp = [a for a,w in zip(IMPROVEMENT_AREAS, IMPROVEMENT_WEIGHTS) if random.random() < w]
            r["suggested_improvements"] = "|".join(imp[:2]) if imp else IMPROVEMENT_AREAS[0]
            for f in ["concept_relevance","concept_purchase_intent","value_perception",
                      "price_index_vs_others","benefit_perception_pre"]:
                r[f] = ""

        elif r["is_aware"]:
            tbw = BARRIER_WEIGHTS[bumo]
            barriers = [b for b,w in zip(TRIAL_BARRIERS, tbw) if random.random() < w]
            if not barriers: barriers = [TRIAL_BARRIERS[0]]
            r["trial_barriers"] = "|".join(barriers[:3])
            r["trial_drivers"] = ""

            r["concept_relevance"] = random.choices(
                ["Very relevant","Somewhat relevant","Not sure","Somewhat irrelevant","Very irrelevant"],
                weights=[0.22,0.35,0.25,0.12,0.06])[0]
            r["concept_purchase_intent"] = random.choices(
                ["Definitely would buy","Probably would buy","Might or might not","Probably would not","Definitely would not"],
                weights=[0.12,0.28,0.30,0.20,0.10])[0]
            r["value_perception"] = random.choices(
                ["Very good value","Fairly good value","Average value","Somewhat poor value","Very poor value"],
                weights=[0.18,0.32,0.30,0.14,0.06])[0]
            r["price_index_vs_others"] = random.choices(
                ["A lot higher","A little higher","About the same","A little lower","A lot lower"],
                weights=[0.08,0.22,0.42,0.20,0.08])[0]
            bp_pre = [b for b,w in BENEFIT_PERCEPTION_W_PRE.items() if random.random() < w]
            r["benefit_perception_pre"] = "|".join(bp_pre[:2]) if bp_pre else "Controls oil / prevents breakouts"

            for attr in PRODUCT_ATTRIBUTES: r[attr_key(attr)] = ""
            for f in ["overall_product_rating","product_superiority","repeat_intent",
                      "recommend_intent","benefit_perception_post","suggested_improvements",
                      "purchase_channel","pack_size_bought","time_since_last_purchase","time_since_last_use"]:
                r[f] = ""
        else:
            for f in ["trial_drivers","trial_barriers","concept_relevance","concept_purchase_intent",
                      "value_perception","price_index_vs_others","benefit_perception_pre",
                      "benefit_perception_post","suggested_improvements","purchase_channel",
                      "pack_size_bought","time_since_last_purchase","time_since_last_use",
                      "overall_product_rating","product_superiority","repeat_intent","recommend_intent"]:
                r[f] = ""
            for attr in PRODUCT_ATTRIBUTES: r[attr_key(attr)] = ""

        rows.append(r)

# ── write CSV ─────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir,"respondents_raw.csv"),"w",newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader(); writer.writerows(rows)
print(f"✓ {len(rows)} respondents written")

# ── aggregate ─────────────────────────────────────────────────────────────────
def pct(n,d): return round(n/d*100,1) if d else 0.0

aware     = [r for r in rows if r["is_aware"]]
trialists = [r for r in rows if r["is_trialist"]]
repeaters = [r for r in rows if r["is_repeater"]]
non_tri   = [r for r in aware if not r["is_trialist"]]

# ── funnel by BUMO ──
funnel_by_bumo = {}
for bumo in BUMO_GROUPS:
    g  = [r for r in rows if r["bumo"]==bumo]
    aw = [r for r in g if r["is_aware"]]
    tr = [r for r in g if r["is_trialist"]]
    rp = [r for r in g if r["is_repeater"]]
    funnel_by_bumo[bumo] = {
        "total":len(g),"aware":len(aw),"aware_pct":pct(len(aw),len(g)),
        "trial":len(tr),"trial_pct":pct(len(tr),len(aw)),
        "repeat":len(rp),"repeat_pct":pct(len(rp),len(tr))
    }

# ── awareness channels ──
ch_counts = {}
for r in aware:
    c=r["awareness_channel"]; ch_counts[c]=ch_counts.get(c,0)+1
awareness_channels = sorted(ch_counts.items(),key=lambda x:-x[1])

# ── benefits by BUMO ──
benefits_by_bumo = {}
for bumo in BUMO_GROUPS:
    g = [r for r in rows if r["bumo"]==bumo]; bc={}
    for r in g:
        for b in r["benefits_sought"].split("|"):
            bc[b]=bc.get(b,0)+1
    benefits_by_bumo[bumo]={b:pct(c,len(g)) for b,c in sorted(bc.items(),key=lambda x:-x[1])[:5]}

def top_counts(field, pool):
    counts={}
    for r in pool:
        for v in r.get(field,"").split("|"):
            if v: counts[v]=counts.get(v,0)+1
    return sorted(counts.items(),key=lambda x:-x[1])

# ── attr ratings ──
attr_ratings={}
for attr in PRODUCT_ATTRIBUTES:
    key=attr_key(attr)
    vals=[int(r[key]) for r in trialists if r.get(key,"")!=""]
    if vals:
        attr_ratings[attr]={
            "t1_pct":round(sum(1 for v in vals if v==5)/len(vals)*100,1),
            "avg":round(sum(vals)/len(vals),2)
        }

# ── benefit perception ──
bp_pre_counts={}
for r in non_tri:
    for b in r.get("benefit_perception_pre","").split("|"):
        if b: bp_pre_counts[b]=bp_pre_counts.get(b,0)+1
bp_post_counts={}
for r in trialists:
    for b in r.get("benefit_perception_post","").split("|"):
        if b: bp_post_counts[b]=bp_post_counts.get(b,0)+1

# ── regional (split funnel) ──
regional={}
for reg in REGIONS:
    g  = [r for r in rows if r["region"]==reg]
    aw = [r for r in g if r["is_aware"]]
    tr = [r for r in g if r["is_trialist"]]
    regional[reg]={"n":len(g),"aware_pct":pct(len(aw),len(g)),"trial_pct":pct(len(tr),len(aw)) if aw else 0}

# ── regional BUMO funnel ──
regional_bumo = {}
for reg in REGIONS:
    regional_bumo[reg] = {}
    for bumo in BUMO_GROUPS:
        g  = [r for r in rows if r["region"]==reg and r["bumo"]==bumo]
        aw = [r for r in g if r["is_aware"]]
        tr = [r for r in g if r["is_trialist"]]
        regional_bumo[reg][bumo] = {
            "n":len(g),"aware_pct":pct(len(aw),len(g)),
            "trial_pct":pct(len(tr),len(aw)) if aw else 0
        }

# ── regional awareness channels ──
regional_channels = {}
for reg in REGIONS:
    cc={}
    for r in aware:
        if r["region"]==reg:
            c=r["awareness_channel"]; cc[c]=cc.get(c,0)+1
    regional_channels[reg]=sorted(cc.items(),key=lambda x:-x[1])[:6]

# ── regional trial drivers/barriers ──
regional_drivers  = {}
regional_barriers = {}
for reg in REGIONS:
    tr_reg  = [r for r in trialists if r["region"]==reg]
    ntr_reg = [r for r in non_tri   if r["region"]==reg]
    regional_drivers[reg]  = top_counts("trial_drivers",  tr_reg)[:4]
    regional_barriers[reg] = top_counts("trial_barriers", ntr_reg)[:4]

oar_counts={}
for r in trialists:
    v=r.get("overall_product_rating","")
    if v: oar_counts[int(v)]=oar_counts.get(int(v),0)+1

sup_counts={}
for r in trialists:
    s=r.get("product_superiority","")
    if s: sup_counts[s]=sup_counts.get(s,0)+1

ri_counts={}
for r in trialists:
    ri=r.get("repeat_intent","")
    if ri: ri_counts[ri]=ri_counts.get(ri,0)+1

pack_counts={}
for r in trialists:
    ps=r.get("pack_size_bought","")
    if ps: pack_counts[ps]=pack_counts.get(ps,0)+1

n_tri=len(trialists); n_ntr=len(non_tri)

summary = {
    "total_n":N,
    "aware_n":len(aware),"aware_pct":pct(len(aware),N),
    "trial_n":n_tri,"trial_pct":pct(n_tri,len(aware)),
    "repeat_n":len(repeaters),"repeat_pct":pct(len(repeaters),n_tri),
    "funnel_by_bumo": funnel_by_bumo,
    "awareness_channels": awareness_channels,
    "regional_channels": regional_channels,
    "benefits_by_bumo": benefits_by_bumo,
    "trial_drivers":  [(d,n,round(n/n_tri*100,1))  for d,n in top_counts("trial_drivers",trialists)[:6]],
    "trial_barriers": [(b,n,round(n/n_ntr*100,1))  for b,n in top_counts("trial_barriers",non_tri)[:6]],
    "attr_ratings": attr_ratings,
    "benefit_perception": {
        "pre": {b:pct(c,n_ntr) for b,c in sorted(bp_pre_counts.items(),key=lambda x:-x[1])},
        "post":{b:pct(c,n_tri)  for b,c in sorted(bp_post_counts.items(),key=lambda x:-x[1])}
    },
    "oar_distribution": {k:pct(v,n_tri) for k,v in sorted(oar_counts.items(),key=lambda x:-x[0])},
    "superiority": {k:pct(v,n_tri) for k,v in sup_counts.items()},
    "improvements": [(a,n,round(n/n_tri*100,1)) for a,n in top_counts("suggested_improvements",trialists)[:6]],
    "repeat_intent": {k:pct(v,n_tri) for k,v in ri_counts.items()},
    "regional": regional,
    "regional_bumo": regional_bumo,
    "regional_drivers": regional_drivers,
    "regional_barriers": regional_barriers,
    "pack_sizes": sorted(pack_counts.items(),key=lambda x:-x[1])
}

with open(os.path.join(out_dir,"summary.json"),"w") as f:
    json.dump(summary,f,indent=2)
print(f"✓ summary.json written")
print(f"Funnel: {N} → {len(aware)} aware ({pct(len(aware),N)}%) → {n_tri} trial ({pct(n_tri,len(aware))}%) → {len(repeaters)} repeat ({pct(len(repeaters),n_tri)}%)")
