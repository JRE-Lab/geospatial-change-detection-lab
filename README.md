# Geospatial Change-Detection Lab

This repository contains materials for a geospatial change-detection lab. It guides you through using open satellite imagery and GIS tools to identify changes in a region of interest (ROI) between two time periods. The lab emphasises GEOINT tradecraft – understanding physical changes through measurement of digital number differences in remote sensing imagery.

## Overview

You will:
- Define a ROI and select before and after satellite images (e.g., Sentinel-2 or Landsat) for the same area and season.
- Pre-process the imagery (atmospheric correction, cropping, aligning) and load into a GIS software such as QGIS.
- Run image differencing by subtracting pixel values in the near-infrared band to highlight change and set thresholds for change/no-change classification.
- Optionally compute NDVI for each date and subtract to detect vegetation changes.
- Classify and visualise change maps, validate results, and write a short analytic note explaining observed changes and their implications.
- All data used in this lab comes from public sources. The scripts and documentation show how GEOINT change detection can inform intelligence analysis.
