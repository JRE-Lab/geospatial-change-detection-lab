diff --git a/tools/render_lab_plan.py b/tools/render_lab_plan.py
new file mode 100755
index 0000000000000000000000000000000000000000..a7fd9b273497cd172cee34713ac89bc0e7141dad
--- /dev/null
+++ b/tools/render_lab_plan.py
@@ -0,0 +1,124 @@
+#!/usr/bin/env python3
+"""Render a markdown summary of the geospatial change-detection lab plan."""
+
+import argparse
+import json
+from pathlib import Path
+from typing import Any, Dict
+
+
+def load_plan(path: Path) -> Dict[str, Any]:
+    with path.open("r", encoding="utf-8") as handle:
+        return json.load(handle)
+
+
+def render_roi(plan: Dict[str, Any]) -> str:
+    roi = plan.get("roi", {})
+    bbox = roi.get("bbox", [])
+    bbox_text = ", ".join(str(value) for value in bbox) if bbox else "-"
+    return "\n".join(
+        [
+            "## ROI",
+            "",
+            "| Field | Value |",
+            "| --- | --- |",
+            f"| Name | {roi.get('name', '-')} |",
+            f"| CRS | {roi.get('crs', '-')} |",
+            f"| BBOX | {bbox_text} |",
+            f"| Notes | {roi.get('notes', '-')} |",
+        ]
+    )
+
+
+def render_imagery(plan: Dict[str, Any]) -> str:
+    imagery = plan.get("imagery", {})
+    before = imagery.get("before", {})
+    after = imagery.get("after", {})
+    lines = [
+        "## Imagery",
+        "",
+        "| Field | Before | After |",
+        "| --- | --- | --- |",
+        f"| Source | {before.get('source', '-')} | {after.get('source', '-')} |",
+        f"| Collection | {before.get('collection', '-')} | {after.get('collection', '-')} |",
+        f"| Acquisition window | {before.get('acquisition_window', '-')} | {after.get('acquisition_window', '-')} |",
+        f"| Cloud cover max | {before.get('cloud_cover_max', '-')} | {after.get('cloud_cover_max', '-')} |",
+        f"| Path | {before.get('path', '-')} | {after.get('path', '-')} |",
+    ]
+    return "\n".join(lines)
+
+
+def render_analysis(plan: Dict[str, Any]) -> str:
+    analysis = plan.get("analysis", {})
+    methods = ", ".join(analysis.get("methods", [])) or "-"
+    thresholds = analysis.get("change_thresholds", {})
+    threshold_lines = ["## Analysis", "", "| Method | Thresholds |", "| --- | --- |"]
+    if thresholds:
+        for method, values in thresholds.items():
+            threshold_lines.append(f"| {method} | {values} |")
+    else:
+        threshold_lines.append("| - | - |")
+    return "\n".join(
+        [
+            "## Analysis Summary",
+            "",
+            f"- Methods: {methods}",
+            "",
+            "\n".join(threshold_lines),
+        ]
+    )
+
+
+def render_deliverables(plan: Dict[str, Any]) -> str:
+    deliverables = plan.get("deliverables", [])
+    lines = ["## Deliverables", ""]
+    if deliverables:
+        lines.extend([f"- {item}" for item in deliverables])
+    else:
+        lines.append("- -")
+    return "\n".join(lines)
+
+
+def parse_args() -> argparse.Namespace:
+    parser = argparse.ArgumentParser(
+        description="Render a markdown summary of a geospatial change-detection lab plan."
+    )
+    parser.add_argument(
+        "--plan",
+        type=Path,
+        default=Path("configs/lab-plan.json"),
+        help="Path to the lab plan JSON file.",
+    )
+    parser.add_argument(
+        "--output",
+        type=Path,
+        default=None,
+        help="Optional output file to write the markdown summary.",
+    )
+    return parser.parse_args()
+
+
+def main() -> None:
+    args = parse_args()
+    plan = load_plan(args.plan)
+    sections = [
+        f"# {plan.get('lab_name', 'Lab Plan')}",
+        "",
+        render_roi(plan),
+        "",
+        render_imagery(plan),
+        "",
+        render_analysis(plan),
+        "",
+        render_deliverables(plan),
+        "",
+    ]
+    output = "\n".join(sections)
+    if args.output:
+        args.output.write_text(output, encoding="utf-8")
+    else:
+        print(output)
+
+
+if __name__ == "__main__":
+    main()
