# S2NDVI_BSI_DEM

**Automated Sentinel-2 Image Analysis for Landslide Monitoring**
*Case Study: Landslide Crown Point, Wayanad, India*

This Python project uses  **Google Earth Engine (GEE)** to analyze landslide-prone areas using Sentinel-2 imagery. Given any point of interest, the script automatically creates a buffer around it and generates key outputs for both **before-and-after analysis**, including:

* True Color imagery (visual RGB)
* NDVI (vegetation health)
* BSI (bare soil / landslide risk)
* Difference maps (after minus before) for NDVI and BSI

**For this study, I focused on the July 2024 Wayanad landslide crown point to examine changes caused by the landslide.**

---

## Features

* **Point & Buffer Creation** – Generate shapefiles for landslide crown points.
* **Drainage Extraction** – Retrieve waterways within the buffer using OpenStreetMap.
* **Sentinel-2 Processing** – Automatically select <5 Cloudcover images for **before and after given time periods**.
* **Indices Computation** – NDVI, BSI, and True Color composite.
* **DEM Export** – SRTM elevation data for terrain analysis.
* **Change Detection** – Compute difference maps (NDVI & BSI) to detect changes after events.

---

## Project Structure

```
S2NDVI_BSI_DEM/
├── main.py                  # Main execution script
├── output/                  # Generated shapefiles and outputs
├── src/s2ndvi_bsi_dem/      # Python modules
│   ├── point_buffer.py      # Point & buffer creation
│   ├── drainage.py          # Drainage extraction
│   ├── sentinel2.py         # Sentinel-2 processing (GEE)
│   └── elevation.py         # DEM export
├── cache/                   # GEE authentication files
├── tests/                   # Optional tests
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/pratistha-katwal/S2NDVI_BSI_DEM.git
cd S2NDVI_BSI_DEM
```

---

## Usage

Edit `main.py` to set the landslide crown point coordinates, buffer, and date ranges:

```python
lat, lon, buf = 11.465104, 76.134982, 20000  # Wayanad crown point
```

Run the script:

```bash
python main.py
```

Outputs:

* **Shapefiles**: `crown_point.shp`, `buffer.shp`, `drainage_lines.shp` → `output/`
* **Sentinel-2 Images**: True Color, NDVI, BSI for **before and after periods** → exported to Google Drive (Filename=Automated_S2_Exports)
* **DEM**: SRTM elevation data → exported to Google Drive(Filename=Automated_S2_Exports)
* **Difference Maps**: NDVI and BSI change (`after - before`) → exported to Google Drive (Filename=Automated_S2_Exports)

---

## Indices

| Index      | Bands                                     | Purpose                           |
| ---------- | ----------------------------------------- | --------------------------------- |
| True Color | B4, B3, B2                                | Visual RGB image                  |
| NDVI       | (B8 - B4)/(B8 + B4)                       | Vegetation health                 |
| BSI        | ((B11+B4) - (B8+B2))/((B11+B4) + (B8+B2)) | Bare soil / landslide risk        |
| Difference | NDVI & BSI                                | Change detection (after - before) |

---

