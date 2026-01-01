diff --git a/scripts/validate-segmentation.sh b/scripts/validate-segmentation.sh
new file mode 100755
index 0000000000000000000000000000000000000000..6b400c078452645c057c3e5c0acb2cc80d68ec7d
--- /dev/null
+++ b/scripts/validate-segmentation.sh
@@ -0,0 +1,39 @@
+#!/usr/bin/env bash
+set -euo pipefail
+
+PLAN_FILE=${1:-configs/segmentation-plan.json}
+
+if [[ ! -f "${PLAN_FILE}" ]]; then
+  echo "Segmentation plan not found: ${PLAN_FILE}" >&2
+  exit 1
+fi
+
+if ! command -v jq >/dev/null 2>&1; then
+  echo "jq is required to parse the plan. Install jq and retry." >&2
+  exit 1
+fi
+
+if ! command -v nmap >/dev/null 2>&1; then
+  echo "nmap is not installed. Install nmap or run manual validation." >&2
+  exit 1
+fi
+
+if [[ -z "${SOURCE_HOST:-}" || -z "${DEST_HOST:-}" ]]; then
+  cat <<'MESSAGE'
+Set SOURCE_HOST and DEST_HOST to run basic tests.
+Example:
+  SOURCE_HOST=10.10.10.25 DEST_HOST=10.20.10.15 ./scripts/validate-segmentation.sh
+MESSAGE
+  exit 1
+fi
+
+ALLOWED_PORTS=$(jq -r '[.rules[] | select(.logging == "allow") | .ports[]] | unique | join(",")' "${PLAN_FILE}")
+
+if [[ -z "${ALLOWED_PORTS}" ]]; then
+  echo "No allowed ports found in the plan." >&2
+  exit 1
+fi
+
+echo "Running nmap scan from ${SOURCE_HOST} to ${DEST_HOST} for allowed ports: ${ALLOWED_PORTS}"
+
+nmap -Pn -p "${ALLOWED_PORTS}" "${DEST_HOST}"
