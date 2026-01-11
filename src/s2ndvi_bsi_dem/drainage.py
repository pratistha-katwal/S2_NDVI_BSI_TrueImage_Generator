import osmnx as ox
import geopandas as gpd

class Drainage:
    @staticmethod
    def from_buffer(gdf_buffer):
        buffer_geom = gdf_buffer.geometry.iloc[0]
        # Fetch waterways from OSM
        waterways = ox.features_from_polygon(buffer_geom, tags={"waterway": True})
        drainage_lines = waterways[waterways.geometry.type.isin(["LineString", "MultiLineString"])]
        return drainage_lines.to_crs("EPSG:4326")

    @staticmethod
    def save_shapefile(drainage_lines, output_dir):
        drainage_lines.to_file(f"{output_dir}/drainage_lines.shp")
        print("Drainage shapefile saved.")
