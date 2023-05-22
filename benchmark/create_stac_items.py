import datetime
import json
from pystac import Item, Asset, Collection, Extent, SpatialExtent, TemporalExtent
import os

# Define dates for filenames
start_date = datetime.date(1990, 1, 1)
dates = [start_date + datetime.timedelta(days=i) for i in range(10)]

# Define the bounding box and temporal extent for the collection
bbox = [-180, -90, 180, 90]
start_time = datetime.datetime(1990, 1, 1)
end_time = datetime.datetime(1990, 1, 10)
spatial_extent = SpatialExtent(bboxes=[bbox])
temporal_extent = TemporalExtent(intervals=[[start_time, end_time]])

collection = Collection(
    id="random_geotiffs",
    description="Collection of random GeoTIFFs",
    extent=Extent(temporal=temporal_extent, spatial=spatial_extent)
)
with open('stac/dates-collection.json', 'w') as f:
    f.write(json.dumps(collection.to_dict()))

# Write the STAC items to the NDJSON file
with open('stac/stac_items.ndjson', 'w') as f:
    for date in dates:
        # Define the item ID and the asset href
        item_id = f"random_data_{date}"
        asset_href = "./benchmark/data/" + os.path.relpath(f"{item_id}.tif")

        # Define the item bounding box and datetime
        item_datetime = datetime.datetime(date.year, date.month, date.day)
        geometry = {
            "type": "Polygon",
            "coordinates": [
                [[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]]
            ],
        }

        # Create the STAC item
        item = Item(
            id=item_id,
            geometry=geometry,
            bbox=bbox,
            datetime=item_datetime,
            properties={},
            collection="random_geotiffs"
        )

        # Add the item to the collection
        collection.add_item(item)

        # Define the asset and add it to the item
        asset = Asset(href=asset_href, media_type='image/tiff')
        item.add_asset('data', asset)

        # Write the item to the NDJSON file
        f.write(json.dumps(item.to_dict()) + '\n')
