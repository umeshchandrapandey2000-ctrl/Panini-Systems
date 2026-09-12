# Panini Systems | Applied Mathematics Consulting
> **Quantitative Architecture & Game Mathematics Consultancy**

Welcome to the foundational repository of **Panini Systems**. Named in honor of Pāṇini—the ancient scholar who invented formal generative systems and algorithmic linguistics—Panini Systems provides rigorous mathematical modeling, combinatorial design, and computational validation to high-growth industries.

While structured as an overarching applied mathematics consultancy (expanding into Operations Research, Quantitative Finance, and Scientific Computing), the firm's active flagship practice is **Game Mathematics & Probabilistic Economy Systems**.

---

## 🏛️ Repository Architecture

```
Panini Systems/
├── docs/                               # Business & Consulting Infrastructure
│   ├── brand_and_positioning.md        # Firm mission, credentials, value proposition
│   ├── services_catalog.md             # Tiered consulting packages & deliverables
│   ├── client_engagement_agreement.md  # Standard MSA & SOW contract template
│   └── how_to_edit_website.md          # Guide on editing text, email & phone settings
│
├── web/                                # Interactive Client Showcase Web Platform
│   ├── index.html                      # Sleek dark-mode quantitative web portal
│   ├── styles.css                      # Mathematical typography & glassmorphic styling
│   └── app.js                          # In-browser slot math & gacha Markov simulator
│
├── panini_math/                        # Proprietary Game Math Computational Engine
│   ├── __init__.py                     # Package metadata & exports
│   ├── combinatorics.py                # Exact analytical payline & RTP solver
│   ├── monte_carlo.py                  # High-throughput statistical simulation & VI
│   ├── par_sheet.py                    # Automated PAR sheet generator (CSV/JSON/MD)
│   ├── gacha_markov.py                 # Absorbing Markov chain gacha pity model
│   └── cli.py                          # Terminal CLI tool for quick audits
│
└── deliverables/                       # Sample Client Deliverables & Blueprints
    └── sample_slot_audit_report.md     # GLI-11/19 certified slot audit report
```

---

## 🚀 Quick Start: Interactive Showcase Platform

The web platform features **live in-browser mathematical simulators** that allow prospective clients, studio heads, and game designers to explore RTP, paytables, volatility indices, and gacha pity curves in real time.

### How to Run:
Simply double-click or open `web/index.html` in any web browser (Google Chrome, Microsoft Edge, Brave, Firefox, Safari):

```bash
# Or from PowerShell / Command Prompt:
start web/index.html
```

### Key Interactive Features:
1. **Slot Machine & PAR Sheet Engine:**
   - Real-time combinatorial RTP, hit frequency, and cycle calculations.
   - Run 10k–100k Monte Carlo spins with live progress bars and distribution histograms.
   - **Export PAR Sheet (.CSV)** directly to Excel.
2. **Gacha & Loot Box Pity Curve Visualizer:**
   - Sliders for base drop rate ($p_0$), soft pity threshold ($K_s$), and hard pity ($K_h$).
   - Live probability density (PMF) and cumulative chance (CDF) chart.
   - Spend quantiles (Median, 90th, 99th percentiles).
3. **Client Scoping & Project Brief Generator:**
   - Interactive questionnaire for studios to submit game specifications and generate formal engagement briefs.

---

## 🧮 Python Mathematical Engine (`panini_math`)

The `panini_math` package is written in pure, clean Python without third-party dependency requirements.

### Running the CLI Suite:
```bash
# Theoretical combinatorial evaluation:
python -m panini_math.cli --mode eval

# High-throughput Monte Carlo simulation:
python -m panini_math.cli --mode sim --spins 100000

# Automated PAR sheet generation:
python -m panini_math.cli --mode par

# Gacha pity distribution analysis:
python -m panini_math.cli --mode gacha
```

### Programmatic Python Usage:
```python
from panini_math import SlotModel, MonteCarloSimulator, PARSheetGenerator

# Define your game reels and paytable
slot = SlotModel(
    name="My Slot Game",
    reel_strips=[reel1, reel2, reel3, reel4, reel5],
    paytable=paytable,
    num_paylines=25
)

# 1. Exact Combinatorics
eval_result = slot.evaluate_payline_combinatorics()
print(f"Exact RTP: {eval_result.total_rtp * 100:.2f}%")

# 2. Monte Carlo Verification
sim = MonteCarloSimulator(slot)
res = sim.run_simulation(num_spins=1_000_000)
print(f"Empirical RTP: {res.empirical_rtp * 100:.2f}%, VI95: {res.volatility_index_95:.2f}")

# 3. Export PAR Sheet
par_gen = PARSheetGenerator(slot)
with open("par_sheet.csv", "w") as f:
    f.write(par_gen.to_csv())
```

---

## 📄 Client Deliverables & Regulatory Compliance

* **Sample Audit Report:** See [`deliverables/sample_slot_audit_report.md`](deliverables/sample_slot_audit_report.md) for an example of a formal Mathematical Audit Report formatted according to **GLI-11** (Gaming Devices) and **GLI-19** (Interactive Gaming Systems) standards.
* **Consulting Agreements:** Use [`docs/client_engagement_agreement.md`](docs/client_engagement_agreement.md) for onboarding new studio clients.
* **Service Packages:** Review [`docs/services_catalog.md`](docs/services_catalog.md) to pitch fixed-scope or retainer packages.

---
© 2026 Panini Systems. All rights reserved.
