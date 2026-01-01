diff --git a/labs/change_detection/change_detection_pipeline.py b/labs/change_detection/change_detection_pipeline.py
new file mode 100644
index 0000000000000000000000000000000000000000..5bf63d02961f996f4509cd9fc8997cbeacff92d2
--- /dev/null
+++ b/labs/change_detection/change_detection_pipeline.py
@@ -0,0 +1,82 @@
+#!/usr/bin/env python3
+"""Compute NIR and NDVI change layers from aligned rasters."""
+
+from __future__ import annotations
+
+import argparse
+from pathlib import Path
+
+import numpy as np
+import rasterio
+
+
+def parse_args() -> argparse.Namespace:
+    parser = argparse.ArgumentParser(
+        description="Generate NIR and NDVI change layers from before/after imagery."
+    )
+    parser.add_argument("--nir-before", required=True, help="Path to NIR before raster.")
+    parser.add_argument("--nir-after", required=True, help="Path to NIR after raster.")
+    parser.add_argument("--red-before", required=True, help="Path to Red before raster.")
+    parser.add_argument("--red-after", required=True, help="Path to Red after raster.")
+    parser.add_argument(
+        "--output-dir", required=True, help="Directory to write output rasters."
+    )
+    parser.add_argument(
+        "--threshold",
+        type=float,
+        default=0.2,
+        help="Absolute NDVI difference threshold for change mask.",
+    )
+    return parser.parse_args()
+
+
+def read_band(path: str) -> tuple[np.ndarray, dict]:
+    with rasterio.open(path) as dataset:
+        data = dataset.read(1).astype("float32")
+        profile = dataset.profile
+    return data, profile
+
+
+def compute_ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
+    numerator = nir - red
+    denominator = nir + red
+    with np.errstate(divide="ignore", invalid="ignore"):
+        ndvi = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator != 0)
+    return ndvi
+
+
+def write_raster(path: Path, data: np.ndarray, profile: dict) -> None:
+    output_profile = profile.copy()
+    output_profile.update(dtype="float32", count=1, nodata=None)
+    with rasterio.open(path, "w", **output_profile) as dst:
+        dst.write(data.astype("float32"), 1)
+
+
+def main() -> None:
+    args = parse_args()
+
+    nir_before, profile = read_band(args.nir_before)
+    nir_after, _ = read_band(args.nir_after)
+    red_before, _ = read_band(args.red_before)
+    red_after, _ = read_band(args.red_after)
+
+    if nir_before.shape != nir_after.shape or nir_before.shape != red_before.shape or nir_before.shape != red_after.shape:
+        raise ValueError("Input rasters must have the same shape. Pre-align them before running.")
+
+    nir_diff = nir_after - nir_before
+    ndvi_before = compute_ndvi(nir_before, red_before)
+    ndvi_after = compute_ndvi(nir_after, red_after)
+    ndvi_diff = ndvi_after - ndvi_before
+
+    change_mask = (np.abs(ndvi_diff) >= args.threshold).astype("float32")
+
+    output_dir = Path(args.output_dir)
+    output_dir.mkdir(parents=True, exist_ok=True)
+
+    write_raster(output_dir / "nir_diff.tif", nir_diff, profile)
+    write_raster(output_dir / "ndvi_diff.tif", ndvi_diff, profile)
+    write_raster(output_dir / "change_mask.tif", change_mask, profile)
+
+
+if __name__ == "__main__":
+    main()
