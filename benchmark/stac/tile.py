from titiler.pgstac.mosaic import PGSTACBackend
reader = PGSTACBackend
from titiler.pgstac.dependencies import (
    PgSTACParams,
)

def tile(
    searchid: str,
    z: int,
    x: int,
    y: int,
    pgstac_params: PgSTACParams,
):
    """Create map tile."""

    with reader(
        searchid,
    ) as src_dst:

        image, assets = src_dst.tile(
            x,
            y,
            z,
        )

    return image