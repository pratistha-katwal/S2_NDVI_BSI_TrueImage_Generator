import ee

class Elevation:
    @staticmethod
    def export_dem(point, buffer_m, folder, prefix="DEM"):
        geom = ee.Geometry.Point([point.x, point.y]).buffer(buffer_m)
        dem = ee.Image("USGS/SRTMGL1_003")
        task = ee.batch.Export.image.toDrive(
            image=dem.clip(geom),
            description=f'{prefix}_export',
            folder=folder,
            fileNamePrefix=prefix,
            region=geom,
            scale=30,
            crs='EPSG:4326',
            maxPixels=1e13
        )
        task.start()
        print(f"DEM export started to folder '{folder}'")
