diff --git a/tools/render_firewall_rules.py b/tools/render_firewall_rules.py
new file mode 100755
index 0000000000000000000000000000000000000000..942af14f2d9b2481ca9ccfeec5b1f3cc6dc9b911
--- /dev/null
+++ b/tools/render_firewall_rules.py
@@ -0,0 +1,70 @@
+#!/usr/bin/env python3
+"""Render firewall rules from the segmentation plan JSON."""
+
+import argparse
+import json
+from pathlib import Path
+from typing import Any, Dict, List
+
+
+def load_plan(path: Path) -> Dict[str, Any]:
+    with path.open("r", encoding="utf-8") as handle:
+        return json.load(handle)
+
+
+def format_ports(ports: List[int]) -> str:
+    return ", ".join(str(port) for port in ports)
+
+
+def render_rules(plan: Dict[str, Any]) -> str:
+    rules = plan.get("rules", [])
+    lines = [
+        "| Source Zone | Destination Zone | Protocol | Ports | Identity Required | Logging | Purpose |",
+        "| --- | --- | --- | --- | --- | --- | --- |",
+    ]
+    for rule in rules:
+        lines.append(
+            "| {source} | {destination} | {protocol} | {ports} | {identity} | {logging} | {purpose} |".format(
+                source=rule.get("source_zone", "-"),
+                destination=rule.get("destination_zone", "-"),
+                protocol=rule.get("protocol", "-"),
+                ports=format_ports(rule.get("ports", [])),
+                identity="yes" if rule.get("identity_required") else "no",
+                logging=rule.get("logging", "-"),
+                purpose=rule.get("purpose", "-"),
+            )
+        )
+    return "\n".join(lines)
+
+
+def parse_args() -> argparse.Namespace:
+    parser = argparse.ArgumentParser(
+        description="Render a markdown table of firewall rules from a segmentation plan JSON file."
+    )
+    parser.add_argument(
+        "--plan",
+        type=Path,
+        default=Path("configs/segmentation-plan.json"),
+        help="Path to the segmentation plan JSON file.",
+    )
+    parser.add_argument(
+        "--output",
+        type=Path,
+        default=None,
+        help="Optional output file to write the markdown table.",
+    )
+    return parser.parse_args()
+
+
+def main() -> None:
+    args = parse_args()
+    plan = load_plan(args.plan)
+    table = render_rules(plan)
+    if args.output:
+        args.output.write_text(table + "\n", encoding="utf-8")
+    else:
+        print(table)
+
+
+if __name__ == "__main__":
+    main()
