# frhd-download
Downlaod script to download the full IGN LiDAR HD MNT datasets as GeoTiffs

Run in a loop until you have all files:

```bash
uv run python download.py
uv run python check_count.py
```

Check that per source there is only one CRS and one NODATA value with:

```bash
uv run python check_crs_nodata.py
```

If a source has multiple CRSes / NODATA values, fix it with:

```bash
uv run python set_crs_nodata.py
```

Some files might have blank NODATA rectangles. Check for those and re-download them with:

```bash
uv run python check_blank_tiles.py
```