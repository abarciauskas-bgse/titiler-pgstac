import boto3
import json
from pystac import Catalog, Collection, Item, Asset, MediaType
from datetime import datetime
import rio_stac
from pprint import pprint

# Get an instance of the S3 client
s3 = boto3.client('s3')

# Get list of objects in the bucket
bucket_name = 'nex-gddp-cmip6-cog'
prefix = 'monthly/CMIP6_ensemble_median/tas/'
objects = s3.list_objects(Bucket=bucket_name, Prefix=prefix)

collection_json = json.loads(open('cmip6_stac_collection.json').read())
collection = Collection.from_dict(collection_json)

# For each object, create an Item and add it to the Catalog
with open('cmip6_stac_items.ndjson', 'w') as f:
    for obj in objects['Contents'][0:10]:
        # Assume the datetime is now, replace this with your own logic
        filename = obj['Key'].split('/')[-1]
        input_datetime = filename.split('_')[-1].replace('.tif', '')
        datetime_ = datetime.strptime(input_datetime, '%Y%m')

        # Create a new Item
        item = rio_stac.create_stac_item(
                id=obj['Key'].split('/')[-1],
                source=f"s3://{bucket_name}/{obj['Key']}",
                collection=collection.id,
                input_datetime=datetime_,
                with_proj=True,
                with_raster=True,
                asset_name="data",
                asset_roles=["data"],
                asset_media_type="image/tiff; application=geotiff; profile=cloud-optimized"
            )
        f.write(json.dumps(item.to_dict()) + '\n')
