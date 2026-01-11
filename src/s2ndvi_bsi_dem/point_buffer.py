import geopandas as gpd
from shapely.geometry import Point
import os

class PointToBuffer:
    def __init__(self, lat, lon, buffer_m):
        self.lat = lat
        self.lon = lon
        self.buffer_m = buffer_m

    def create_gdfs(self):
        """Create point and buffer GeoDataFrames"""
        gdf_point = gpd.GeoDataFrame(
            {"name": ["Landslide Crown Point"]},
            geometry=[Point(self.lon, self.lat)],
            crs="EPSG:4326"
        )
        gdf_buffer_geom = (
            gdf_point.to_crs("EPSG:3857").geometry.buffer(self.buffer_m).to_crs("EPSG:4326")
        )
        gdf_buffer = gpd.GeoDataFrame({"name": ["Buffer"]}, geometry=gdf_buffer_geom, crs="EPSG:4326")
        return gdf_point, gdf_buffer

    def save_shapefiles(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        gdf_point, gdf_buffer = self.create_gdfs()
        gdf_point.to_file(f"{output_dir}/crown_point.shp")
        gdf_buffer.to_file(f"{output_dir}/buffer_{self.buffer_m}m.shp")
        print("Point & buffer shapefiles saved.")
        return gdf_point, gdf_buffer
