diff --git a/labs/early_crisis_warning_fusion/README.md b/labs/early_crisis_warning_fusion/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..7509e042fa18d118c7830a2b2809f583e1b8ad64
--- /dev/null
+++ b/labs/early_crisis_warning_fusion/README.md
@@ -0,0 +1,73 @@
+# Early Crisis Warning Fusion Lab
+
+This lab walks through building an **early warning fusion workflow** that combines climate stress, market pressures, conflict activity, and population exposure into a single, interpretable crisis-risk signal. The goal is to teach analysts how to fuse disparate indicators into a transparent, auditable score that can be monitored over time.
+
+## Learning objectives
+
+By the end of this lab, you will be able to:
+- Normalize multi-source indicators to a common scale.
+- Weight and fuse indicators into a composite early warning score.
+- Flag elevated risk periods for a region of interest (ROI).
+- Communicate findings in a short analytic summary.
+
+## Scenario
+
+You are supporting an early warning cell monitoring multiple districts. You have monthly indicators from open sources:
+- **Rainfall anomalies** (proxy for drought/flood stress)
+- **Market price anomalies** (proxy for food access)
+- **Conflict events** (proxy for instability)
+- **Population exposure** (proxy for human impact)
+
+Your task is to fuse these indicators and identify regions showing sustained stress.
+
+## Data inputs
+
+The lab expects CSVs with the following schemas:
+
+| File | Required columns | Example |
+| --- | --- | --- |
+| `rainfall_anomaly.csv` | `region_id`, `date`, `anomaly_z` | `R01,2024-01-01,-1.2` |
+| `market_prices.csv` | `region_id`, `date`, `price_anomaly_z` | `R01,2024-01-01,0.8` |
+| `conflict_events.csv` | `region_id`, `date`, `events` | `R01,2024-01-01,4` |
+| `population_exposure.csv` | `region_id`, `population` | `R01,120000` |
+
+Sample inputs are provided in `data/`.
+
+## Workflow
+
+1. **Inspect the indicators** to ensure dates and regions align.
+2. **Normalize each indicator** into a 0–1 scale for fusion.
+3. **Apply weights** to reflect analytic priorities.
+4. **Fuse indicators** into a composite score.
+5. **Assign risk tiers** (low/medium/high).
+6. **Write a short analytic note** explaining the top drivers.
+
+## Running the fusion pipeline
+
+From the repository root:
+
+```bash
+python labs/early_crisis_warning_fusion/fusion_pipeline.py \
+  --rainfall labs/early_crisis_warning_fusion/data/rainfall_anomaly.csv \
+  --market labs/early_crisis_warning_fusion/data/market_prices.csv \
+  --conflict labs/early_crisis_warning_fusion/data/conflict_events.csv \
+  --population labs/early_crisis_warning_fusion/data/population_exposure.csv \
+  --output labs/early_crisis_warning_fusion/output/fused_risk_scores.csv
+```
+
+The pipeline will create an output CSV with the fused score and risk tier for each region-month.
+
+## Deliverables
+
+- `fused_risk_scores.csv` produced by the pipeline.
+- A short analytic summary (1–2 paragraphs) describing:
+  - Which regions are trending high risk.
+  - Which indicators are driving the risk.
+  - Any notable changes compared with previous months.
+
+## Extension ideas
+
+- Replace min-max scaling with z-score normalization.
+- Add satellite-derived vegetation stress (NDVI anomalies).
+- Add displacement data to refine exposure weighting.
+- Visualize results in QGIS using a joined shapefile.
