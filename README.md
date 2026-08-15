# frhd-download
Download script to download the full IGN LiDAR HD MNT datasets as GeoTiffs

## Get The Files
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

## Make a Mapterhorn Source Tarball

```bash
git submodule init --recursive
```

Once those files look good, create bounds.csv files with:

```bash
uv run python source_bounds.py frhd2154a
uv run python source_bounds.py frhd2154b
uv run python source_bounds.py frhd2154c
uv run python source_bounds.py frhd2154d
uv run python source_bounds.py frhd2154e
uv run python source_bounds.py frhd2975
uv run python source_bounds.py frhd5490
```


## File Lists Folder

The file lists folder is too big to be checked into GitHub. Download it instead from https://github.com/wipfli/frhd-download/releases/tag/v0.0.1 etc.