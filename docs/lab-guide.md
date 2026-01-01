diff --git a/docs/lab-guide.md b/docs/lab-guide.md
index ae5ee8d7347e1cea6ed139e7d832e29edd109704..c5f46bb483368ebb881ca8754eaaa35852de55f9 100644
--- a/docs/lab-guide.md
+++ b/docs/lab-guide.md
@@ -1,60 +1,59 @@
-diff --git a/docs/lab-guide.md b/docs/lab-guide.md
-new file mode 100644
-index 0000000000000000000000000000000000000000..a391c65f21f9da0d7d1c9bd05377851ce5a0668d
---- /dev/null
-+++ b/docs/lab-guide.md
-@@ -0,0 +1,54 @@
-+# Zero-Trust Network Segmentation Lab Guide
-+
-+This guide provides an end-to-end lab plan for building a micro-segmented network with explicit allow rules, identity-aware policies, and continuous validation.
-+
-+## Objectives
-+
-+- Build a segmented network with distinct user, server, management, and security zones.
-+- Enforce least-privilege traffic flows using default-deny rules.
-+- Validate that east-west traffic is blocked unless explicitly allowed.
-+- Capture telemetry for SIEM-style monitoring.
-+
-+## Lab Topology
-+
-+| Zone | Subnet | Description |
-+| --- | --- | --- |
-+| User | 10.10.10.0/24 | Employee endpoints and VDI |
-+| Server | 10.20.10.0/24 | Application and database workloads |
-+| Management | 10.30.10.0/24 | Admin jump hosts |
-+| Security | 10.40.10.0/24 | Logging/SIEM tooling |
-+
-+## Steps
-+
-+1. **Design the segmentation plan**
-+   - Start from `configs/segmentation-plan.json` and update zones, assets, and rules to match your lab.
-+   - Enumerate each required flow and note the purpose, identity requirement, and logging intent.
-+
-+2. **Deploy the firewall**
-+   - Install pfSense or OPNsense in a VM with at least 4 interfaces.
-+   - Assign each interface to a dedicated VLAN or virtual network.
-+
-+3. **Implement least-privilege rules**
-+   - Set a default deny rule for every interface.
-+   - Add allow rules based on the segmentation plan. Use the render tool for quick tables:
-+     ```bash
-+     ./tools/render_firewall_rules.py --plan configs/segmentation-plan.json
-+     ```
-+
-+4. **Integrate identity-aware controls**
-+   - Connect the firewall to LDAP/RADIUS.
-+   - Restrict administrative access to the management zone using group-based rules.
-+
-+5. **Validate and test**
-+   - Use `scripts/validate-segmentation.sh` to run basic reachability checks.
-+   - Confirm unauthorized traffic is blocked and logged.
-+
-+6. **Monitor and refine**
-+   - Forward logs to your SIEM or log collector.
-+   - Review denied traffic and tune rules as needed.
-+
-+## Deliverables
-+
-+- Updated segmentation plan JSON with your environment details.
-+- A firewall rule table exported from the render tool.
-+- Validation results showing blocked vs. allowed traffic.
+# Geospatial Change-Detection Lab Guide
+
+This guide walks analysts through designing and executing a repeatable change-detection workflow using open satellite imagery and GIS tools.
+
+## Objectives
+
+- Define a defensible region of interest (ROI) and time windows for before/after imagery.
+- Prepare imagery for analysis (atmospheric correction, cloud masking, alignment, and clipping).
+- Detect change using NIR and NDVI differencing, then classify change vs. no-change.
+- Validate results and produce an analytic note grounded in GEOINT tradecraft.
+
+## Lab Inputs
+
+- `configs/lab-plan.json` for the ROI, imagery windows, and analysis parameters.
+- Public imagery sources (Sentinel-2 L2A or Landsat Collection 2).
+- GIS software (QGIS recommended).
+
+## Steps
+
+1. **Define the ROI and timeline**
+   - Update the `roi` section in `configs/lab-plan.json` with a precise bounding box and CRS.
+   - Select matching seasons for before/after imagery to reduce false change.
+
+2. **Acquire imagery**
+   - Download imagery from Copernicus Open Access Hub, USGS EarthExplorer, or Google Earth Engine.
+   - Record acquisition dates and cloud cover for traceability.
+
+3. **Pre-process imagery**
+   - Apply cloud masking using the scene classification layer (SCL) or QA bands.
+   - Resample and align imagery to a common grid (10 m for Sentinel-2).
+   - Clip imagery to the ROI plus a small buffer for context.
+
+4. **Run change detection**
+   - Compute NIR differencing: `nir_after - nir_before`.
+   - Compute NDVI for each date and subtract: `ndvi_after - ndvi_before`.
+   - Apply thresholds from `analysis.change_thresholds` to classify change vs. no-change.
+
+5. **Validate results**
+   - Cross-check with high-resolution basemaps or alternate imagery.
+   - Flag ambiguous areas for manual review.
+   - Document confidence and potential sources of error.
+
+6. **Deliverables**
+   - Create maps showing before/after imagery, change rasters, and change polygons.
+   - Write a short analytic note describing observed changes, timing, and implications.
+
+## Helpful Commands
+
+Render a quick summary of the lab plan:
+
+```bash
+python3 tools/render_lab_plan.py --plan configs/lab-plan.json
+```
+
+Validate the lab plan structure:
+
+```bash
+./scripts/validate-lab.sh
+```
