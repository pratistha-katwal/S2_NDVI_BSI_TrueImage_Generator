import ee
from shapely.geometry import Point

ee.Authenticate()
ee.Initialize(project="pratistha111")


class Sentinel2BestImage:
    def __init__(self, aoi, start_date, end_date, buffer_m=20000, max_cloud=5):

        # Handle AOI
        if isinstance(aoi, Point):
            self.point = ee.Geometry.Point([aoi.x, aoi.y])
        elif isinstance(aoi, ee.Geometry):
            self.point = aoi
        else:
            raise TypeError("AOI must be shapely.geometry.Point or ee.Geometry")

        self.AOI = self.point.buffer(buffer_m)
        self.start_date = start_date
        self.end_date = end_date
        self.max_cloud = max_cloud
        self.collection = None

    # -----------------------------
    # Load Sentinel-2 collection
    # -----------------------------
    def load_collection(self):
        self.collection = (
            ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
            .filterBounds(self.AOI)
            .filterDate(self.start_date, self.end_date)
            .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", self.max_cloud))
            .select(["B2", "B3", "B4", "B8", "B11"])
        )

        count = self.collection.size().getInfo()
        print(f"Images found ({self.start_date} → {self.end_date}): {count}")
        return count

    # -----------------------------
    # Get best image (least cloud)
    # -----------------------------
    def get_best_image(self):
        if self.collection is None:
            self.load_collection()

        if self.collection.size().getInfo() == 0:
            raise ValueError("No images found for given filters")

        sorted_col = self.collection.sort("CLOUDY_PIXEL_PERCENTAGE")
        best_img = ee.Image(sorted_col.first())

        info = best_img.getInfo()
        date = info["properties"].get("SENSING_TIME", "N/A")
        cloud = info["properties"].get("CLOUDY_PIXEL_PERCENTAGE", "N/A")

        print(f"Best image → Date: {date}, Cloud %: {cloud}")

        # Use mosaic for spatial completeness
        mosaic = sorted_col.mosaic()
        return mosaic

    # -----------------------------
    # Products
    # -----------------------------
    @staticmethod
    def true_color(img):
        # IMPORTANT: visualization handled in QGIS
        return img.select(["B4", "B3", "B2"])

    @staticmethod
    def ndvi(img):
        return img.normalizedDifference(["B8", "B4"]).rename("NDVI")

    @staticmethod
    def bsi(img):
        return img.expression(
            "((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))",
            {
                "SWIR": img.select("B11"),
                "RED": img.select("B4"),
                "NIR": img.select("B8"),
                "BLUE": img.select("B2"),
            },
        ).rename("BSI")

    # -----------------------------
    # Export to Google Drive
    # -----------------------------
    @staticmethod
    def export_image(img, aoi, description, filename, scale=10):
        task = ee.batch.Export.image.toDrive(
            image=img.clip(aoi),
            description=description,
            folder="Automated_S2_Exports",
            fileNamePrefix=filename,
            scale=scale,
            maxPixels=1e13,
        )
        task.start()
        print(f"Export started → {description}")
