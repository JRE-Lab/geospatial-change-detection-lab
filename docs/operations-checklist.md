diff --git a/docs/operations-checklist.md b/docs/operations-checklist.md
index 658f746accf33174b0c716560df0ff4c2abe5f26..089475f0bd648318b30a521d1131d5ae4cd1385b 100644
--- a/docs/operations-checklist.md
+++ b/docs/operations-checklist.md
@@ -1,32 +1,26 @@
-diff --git a/docs/operations-checklist.md b/docs/operations-checklist.md
-new file mode 100644
-index 0000000000000000000000000000000000000000..150eff7ed90eb89e286c1bb61748c24240bd7a12
---- /dev/null
-+++ b/docs/operations-checklist.md
-@@ -0,0 +1,25 @@
-
-+# Zero-Trust Segmentation Operations Checklist
-+
-+## Pre-flight
-+
-+- [ ] Confirm IP plan and VLAN IDs.
-+- [ ] Inventory lab systems and assign them to zones.
-+- [ ] Validate identity provider connectivity.
-+
-+## Firewall Build
-+
-+- [ ] Map interfaces to zones.
-+- [ ] Enable logging on default-deny rules.
-+- [ ] Tag rules with descriptions and ticket references.
-+
-+## Validation
-+
-+- [ ] Test allowed flows from each zone.
-+- [ ] Confirm denied flows are blocked and logged.
-+- [ ] Capture packet traces for at least one allowed and denied flow.
-+
-+## Monitoring
-+
-+- [ ] Forward logs to SIEM/log collector.
-+- [ ] Build a dashboard for allowed vs denied traffic.
-+- [ ] Review logs daily during lab execution.
+# Geospatial Change-Detection Operations Checklist
+
+## Pre-flight
+
+- [ ] Confirm ROI bounding box, CRS, and timeline in `configs/lab-plan.json`.
+- [ ] Identify imagery sources and access credentials (Copernicus, USGS, GEE).
+- [ ] Establish a file naming convention for before/after imagery.
+
+## Data Preparation
+
+- [ ] Download cloud-minimized scenes for both dates.
+- [ ] Apply cloud/quality masks and document masking criteria.
+- [ ] Align imagery to a common grid and resolution.
+- [ ] Clip imagery to the ROI plus buffer.
+
+## Change Detection
+
+- [ ] Compute NIR and NDVI difference rasters.
+- [ ] Apply thresholds and produce change/no-change classification.
+- [ ] Vectorize change polygons for map-ready outputs.
+
+## Validation & Reporting
+
+- [ ] Cross-check results with alternate imagery or basemaps.
+- [ ] Record uncertainties and potential false positives.
+- [ ] Publish maps and analytic note with source citations.
