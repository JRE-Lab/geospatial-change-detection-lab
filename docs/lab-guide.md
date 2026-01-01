diff --git a/docs/lab-guide.md b/docs/lab-guide.md
new file mode 100644
index 0000000000000000000000000000000000000000..a391c65f21f9da0d7d1c9bd05377851ce5a0668d
--- /dev/null
+++ b/docs/lab-guide.md
@@ -0,0 +1,54 @@
+# Zero-Trust Network Segmentation Lab Guide
+
+This guide provides an end-to-end lab plan for building a micro-segmented network with explicit allow rules, identity-aware policies, and continuous validation.
+
+## Objectives
+
+- Build a segmented network with distinct user, server, management, and security zones.
+- Enforce least-privilege traffic flows using default-deny rules.
+- Validate that east-west traffic is blocked unless explicitly allowed.
+- Capture telemetry for SIEM-style monitoring.
+
+## Lab Topology
+
+| Zone | Subnet | Description |
+| --- | --- | --- |
+| User | 10.10.10.0/24 | Employee endpoints and VDI |
+| Server | 10.20.10.0/24 | Application and database workloads |
+| Management | 10.30.10.0/24 | Admin jump hosts |
+| Security | 10.40.10.0/24 | Logging/SIEM tooling |
+
+## Steps
+
+1. **Design the segmentation plan**
+   - Start from `configs/segmentation-plan.json` and update zones, assets, and rules to match your lab.
+   - Enumerate each required flow and note the purpose, identity requirement, and logging intent.
+
+2. **Deploy the firewall**
+   - Install pfSense or OPNsense in a VM with at least 4 interfaces.
+   - Assign each interface to a dedicated VLAN or virtual network.
+
+3. **Implement least-privilege rules**
+   - Set a default deny rule for every interface.
+   - Add allow rules based on the segmentation plan. Use the render tool for quick tables:
+     ```bash
+     ./tools/render_firewall_rules.py --plan configs/segmentation-plan.json
+     ```
+
+4. **Integrate identity-aware controls**
+   - Connect the firewall to LDAP/RADIUS.
+   - Restrict administrative access to the management zone using group-based rules.
+
+5. **Validate and test**
+   - Use `scripts/validate-segmentation.sh` to run basic reachability checks.
+   - Confirm unauthorized traffic is blocked and logged.
+
+6. **Monitor and refine**
+   - Forward logs to your SIEM or log collector.
+   - Review denied traffic and tune rules as needed.
+
+## Deliverables
+
+- Updated segmentation plan JSON with your environment details.
+- A firewall rule table exported from the render tool.
+- Validation results showing blocked vs. allowed traffic.
