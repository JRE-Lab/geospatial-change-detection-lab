diff --git a/docs/operations-checklist.md b/docs/operations-checklist.md
new file mode 100644
index 0000000000000000000000000000000000000000..150eff7ed90eb89e286c1bb61748c24240bd7a12
--- /dev/null
+++ b/docs/operations-checklist.md
@@ -0,0 +1,25 @@
+# Zero-Trust Segmentation Operations Checklist
+
+## Pre-flight
+
+- [ ] Confirm IP plan and VLAN IDs.
+- [ ] Inventory lab systems and assign them to zones.
+- [ ] Validate identity provider connectivity.
+
+## Firewall Build
+
+- [ ] Map interfaces to zones.
+- [ ] Enable logging on default-deny rules.
+- [ ] Tag rules with descriptions and ticket references.
+
+## Validation
+
+- [ ] Test allowed flows from each zone.
+- [ ] Confirm denied flows are blocked and logged.
+- [ ] Capture packet traces for at least one allowed and denied flow.
+
+## Monitoring
+
+- [ ] Forward logs to SIEM/log collector.
+- [ ] Build a dashboard for allowed vs denied traffic.
+- [ ] Review logs daily during lab execution.
