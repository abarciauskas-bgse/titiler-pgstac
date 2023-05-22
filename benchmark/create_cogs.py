import rasterio
from rasterio.transform import from_origin
from rasterio.crs import CRS
import numpy as np
import datetime
from rasterio.io import MemoryFile
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

# Define the spatial resolution
res = (0.25, 0.25)

# Generate dates for filenames
start_date = datetime.date(1990, 1, 1)
dates = [start_date + datetime.timedelta(days=i) for i in range(10)]

for date in dates:
    # Define raster dimensions
    width = int(360 / res[0])  # let's create global cover for simplicity
    height = int(180 / res[1])

    # Generate random data
    data = np.random.rand(height, width).astype(rasterio.float32)

    # Define the GeoTIFF metadata
    transform = from_origin(-180, 90, *res)
    crs = CRS.from_string('EPSG:4326')  # WGS84 geographic coordinate system

    src_profile = dict(
        driver="GTiff",
        dtype="float32",
        count=1,
        height=height,
        width=width,
        crs="epsg:4326",
        transform=transform,
    )

    with MemoryFile() as memfile:
        with memfile.open(**src_profile) as mem:
            # Populate the input file with numpy array
            mem.write(data, 1)

            dst_profile = cog_profiles.get("deflate")
            cog_translate(
                mem,
                f'data/random_data_{date}.tif',
                dst_profile,
                in_memory=True,
                quiet=True,
            )