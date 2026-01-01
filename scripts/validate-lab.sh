diff --git a/scripts/validate-lab.sh b/scripts/validate-lab.sh
new file mode 100755
index 0000000000000000000000000000000000000000..26c54869ef58544ede07e4b68b7b49819b83a729
--- /dev/null
+++ b/scripts/validate-lab.sh
@@ -0,0 +1,41 @@
+#!/usr/bin/env bash
+set -euo pipefail
+
+PLAN_FILE=${1:-configs/lab-plan.json}
+
+if [[ ! -f "${PLAN_FILE}" ]]; then
+  echo "Lab plan not found: ${PLAN_FILE}" >&2
+  exit 1
+fi
+
+if ! command -v python3 >/dev/null 2>&1; then
+  echo "python3 is required to validate the plan." >&2
+  exit 1
+fi
+
+python3 - <<'PY' "${PLAN_FILE}"
+import json
+import sys
+from pathlib import Path
+
+plan_path = Path(sys.argv[1])
+with plan_path.open("r", encoding="utf-8") as handle:
+    plan = json.load(handle)
+
+required_top = ["lab_name", "roi", "imagery", "bands", "processing", "analysis"]
+missing = [key for key in required_top if key not in plan]
+if missing:
+    raise SystemExit(f"Missing required top-level keys: {', '.join(missing)}")
+
+roi = plan.get("roi", {})
+for key in ("name", "bbox", "crs"):
+    if key not in roi:
+        raise SystemExit(f"ROI missing required field: {key}")
+
+imagery = plan.get("imagery", {})
+for key in ("before", "after"):
+    if key not in imagery:
+        raise SystemExit(f"Imagery missing required section: {key}")
+
+print("Lab plan validation passed.")
+PY
