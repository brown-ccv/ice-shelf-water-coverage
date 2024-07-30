import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
import numpy as np

def calculate_water_coverage(shapefile_path, binary_image_path):
    # Calculates the percentage of water coverage within the ice shelf boundary based on a shapefile and GeoTIFF.
    # shapefile_path (str): Path to the shapefile containing the ice shelf boundary.
    # binary_image_path (str): Path to the binary GeoTIFF image where 0 represents water.
    # Returns: Percentage of water coverage within the ice shelf boundary.
  
    try:
        # Read shapefile using geopandas
        ice_shelf_boundary = gpd.read_file(shapefile_path)

        # Open GeoTIFF using raterio 
        with rasterio.open(binary_image_path) as src:
            # Read image as numpy array using first band of raster data
            binary_image = src.read(1)
            
            # Gets transformation to relate pixel coordinates to geographic coordinates
            transform = src.transform
            
            # Rasterize the ice shelf boundary to create a mask sets the ice shelf boundary to true 
            # everything else outside boundary to false
            ice_shelf_mask = geometry_mask(
                ice_shelf_boundary.geometry,
                out_shape=binary_image.shape,
                transform=transform,
                invert=True
            )
            
            # Apply the mask to the binary image to get pixels within the ice shelf boundary
            water_pixels_in_boundary = binary_image[ice_shelf_mask]
        
        # Calculate the percentage of water coverage
        #total counts number of pixels in self
        #water pixels counts number of water pixels in shelf
        total_pixels_within_boundary = water_pixels_in_boundary.size
        water_pixels_in_boundary_count = (water_pixels_in_boundary == 0).sum()

        # calculates % of water pixels out of the total number of pixels

        if total_pixels_within_boundary > 0:
            water_coverage_percent = (water_pixels_in_boundary_count / total_pixels_within_boundary) * 100
        # Handle case when no pixels are within the boundary
        else:
            water_coverage_percent = 0.0 

        return water_coverage_percent
    # handles errors and prints error message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# calls paths to shape file and GeoTiff and prints percentage of water coverage
shapefile_path = '/Users/chollid1/Desktop/TimeLine_Shapefiles_gl/2015_08-07.shp'
binary_image_path = '/Users/chollid1/Desktop/2015_08-07_GeoTiff.tif'

water_coverage_percent = calculate_water_coverage(shapefile_path, binary_image_path)
if water_coverage_percent is not None:
    print(f"Water coverage within ice shelf boundary: {water_coverage_percent:.2f}%")

    