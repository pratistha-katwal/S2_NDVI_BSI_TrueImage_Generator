from pathlib import Path
from shapely.geometry import Point

from src.s2ndvi_bsi_dem.point_buffer import PointToBuffer
from src.s2ndvi_bsi_dem.drainage import Drainage
from src.s2ndvi_bsi_dem.sentinel2 import Sentinel2BestImage
from src.s2ndvi_bsi_dem.elevation import Elevation

# --------------------------------------------------
# 📂 Resolve project root & output directory
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"Project root: {PROJECT_ROOT}")
print(f"Output directory: {OUTPUT_DIR}")

# --------------------------------------------------
# Inputs
# --------------------------------------------------
lat, lon, buf = 11.465104, 76.134982, 20000
pt = Point(lon, lat)

# --------------------------------------------------
# 1️⃣ Point + buffer
# --------------------------------------------------
pb = PointToBuffer(lat, lon, buf)
gdf_point, gdf_buffer = pb.save_shapefiles(str(OUTPUT_DIR))

# --------------------------------------------------
# 2️⃣ Drainage
# --------------------------------------------------
drainage = Drainage.from_buffer(gdf_buffer)
Drainage.save_shapefile(drainage, str(OUTPUT_DIR))

# --------------------------------------------------
# 3️⃣ DEM
# --------------------------------------------------
Elevation.export_dem(pt, buf, folder="Automated_S2_Exports")

# --------------------------------------------------
# 3️⃣ Sentinel-2 BEFORE
# --------------------------------------------------
s2_before = Sentinel2BestImage(
    aoi=pt,
    start_date="2024-04-05",
    end_date="2024-07-25",
    buffer_m=buf
)

best_before = s2_before.get_best_image()

# Compute indices and save to variables
ndvi_before = Sentinel2BestImage.ndvi(best_before)
bsi_before = Sentinel2BestImage.bsi(best_before)

Sentinel2BestImage.export_image(Sentinel2BestImage.true_color(best_before),
                                s2_before.AOI, "S2_TRUECOLOR_BEFORE", "truecolor_before")
Sentinel2BestImage.export_image(ndvi_before, s2_before.AOI, "S2_NDVI_BEFORE", "ndvi_before")
Sentinel2BestImage.export_image(bsi_before, s2_before.AOI, "S2_BSI_BEFORE", "bsi_before")

# --------------------------------------------------
# 4️⃣ Sentinel-2 AFTER
# --------------------------------------------------
s2_after = Sentinel2BestImage(
    aoi=pt,
    start_date="2024-08-01",
    end_date="2024-12-15",
    buffer_m=buf
)

best_after = s2_after.get_best_image()

# Compute indices and save to variables
ndvi_after = Sentinel2BestImage.ndvi(best_after)
bsi_after = Sentinel2BestImage.bsi(best_after)

Sentinel2BestImage.export_image(Sentinel2BestImage.true_color(best_after),
                                s2_after.AOI, "S2_TRUECOLOR_AFTER", "truecolor_after")
Sentinel2BestImage.export_image(ndvi_after, s2_after.AOI, "S2_NDVI_AFTER", "ndvi_after")
Sentinel2BestImage.export_image(bsi_after, s2_after.AOI, "S2_BSI_AFTER", "bsi_after")

# --------------------------------------------------
# 6️⃣ Compute difference (after - before)
# --------------------------------------------------
ndvi_diff = ndvi_after.subtract(ndvi_before).rename("NDVI_DIFF")
bsi_diff  = bsi_after.subtract(bsi_before).rename("BSI_DIFF")

Sentinel2BestImage.export_image(ndvi_diff, s2_after.AOI, "NDVI_DIFF", "ndvi_after_minus_before")
Sentinel2BestImage.export_image(bsi_diff, s2_after.AOI, "BSI_DIFF", "bsi_after_minus_before")
