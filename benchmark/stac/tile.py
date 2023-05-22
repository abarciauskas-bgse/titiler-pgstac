from geojson_pydantic import Polygon
import morecantile
from typing import Any, Dict, List, Optional, Tuple
from titiler.pgstac.mosaic import PGSTACBackend
from psycopg_pool import ConnectionPool
from rio_tiler.mosaic import mosaic_reader
from rio_tiler.models import ImageData

pool = ConnectionPool(conninfo="postgresql://postgres:postgres@localhost:5439/postgres") 
# TypeError: __init__() missing 1 required positional argument: 'input'
backend = PGSTACBackend(pool=pool)

def assets_for_tile(x: int, y: int, z: int) -> List[Dict]:
    """Retrieve assets for tile."""
    bbox = backend.tms.bounds(morecantile.Tile(x, y, z))
    return backend.get_assets(Polygon.from_bounds(*bbox))

"""Create map tile."""
def tile(
    tile_x: int,
    tile_y: int,
    tile_z: int,
    reverse: bool = False,
    scan_limit: Optional[int] = None,
    items_limit: Optional[int] = None,
    time_limit: Optional[int] = None,
    exitwhenfull: Optional[bool] = None,
    skipcovered: Optional[bool] = None,
    **kwargs: Any,
) -> Tuple[ImageData, List[str]]:
    """Get Tile from multiple observation."""
    mosaic_assets = assets_for_tile(
        tile_x,
        tile_y,
        tile_z,
        scan_limit=scan_limit,
        items_limit=items_limit,
        time_limit=time_limit,
        exitwhenfull=exitwhenfull,
        skipcovered=skipcovered,
    )

    # if not mosaic_assets:
    #     raise NoAssetFoundError(
    #         f"No assets found for tile {tile_z}-{tile_x}-{tile_y}"
    #     )

    if reverse:
        mosaic_assets = list(reversed(mosaic_assets))

    def _reader(
        item: Dict[str, Any], x: int, y: int, z: int, **kwargs: Any
    ) -> ImageData:
        with backend.reader(item, tms=backend.tms, **backend.reader_options) as src_dst:
            return src_dst.tile(x, y, z, **kwargs)

    return mosaic_reader(mosaic_assets, _reader, tile_x, tile_y, tile_z, **kwargs)

tile(0, 0, 0)