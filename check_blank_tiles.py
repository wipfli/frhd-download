from glob import glob
import rasterio
import numpy as np
from multiprocessing import Pool
import os
import shutil
from scipy.ndimage import label

import download

def true_regions_are_rectangular(arr):
    if not np.any(arr):
        return False
    
    structure = np.ones((3, 3), dtype=int)
    labeled, n_labels = label(arr, structure=structure)

    for i in range(1, n_labels + 1):
        ys, xs = np.where(labeled == i)
        y_min, y_max = ys.min(), ys.max()
        x_min, x_max = xs.min(), xs.max()

        expected_area = (y_max - y_min + 1) * (x_max - x_min + 1)
        actual_count = ys.size

        if actual_count != expected_area:
            return False

    return True

def has_blank(filepath):
    tile_size = 512
    with rasterio.env.Env(GDAL_CACHEMAX=256):
        with rasterio.open(filepath) as src:
            height = src.height
            width = src.width            
            
            for y in range(0, height, tile_size):
                for x in range(0, width, tile_size):
                    y_start = max(0, y)
                    y_end = min(height, y + tile_size)
                    x_start = max(0, x)
                    x_end = min(width, x + tile_size)
                    
                    window = rasterio.windows.Window(x_start, y_start, x_end - x_start, y_end - y_start)
                    
                    current_tile = None
                    with rasterio.open(filepath) as src:
                        current_tile = np.nan_to_num(src.read(1, window=window), nan=-9999)

                    nodata_pixel_count = np.sum(current_tile == -9999)
                    if nodata_pixel_count > tile_size:
                        return True

    return False

def has_rectangular_blank(i, filepath):
    if i % 100 == 0:
        print(f'{i:_}')
    if not has_blank(filepath):
        return False
    else:
        with rasterio.env.Env(GDAL_CACHEMAX=256):
            with rasterio.open(filepath) as src:
                return true_regions_are_rectangular(np.nan_to_num(src.read(1), nan=-9999) == -9999)
            
def check(source):
    folder = f'blank-checks/{source}'
    os.makedirs(folder, exist_ok=True)

    filepaths = glob(f'source-store/{source}/*.tif')
    argument_tuples = [(i, filepath) for i, filepath in enumerate(filepaths)]

    print(f'len(filepaths) = {len(filepaths):_}')

    with Pool(16) as pool:
        results = pool.starmap(has_rectangular_blank, argument_tuples, chunksize=1)

    for filepath, result in zip(filepaths, results):
        if result:
            filename = filepath.split('/')[-1]
            with open(f'{folder}/{filename}', 'w') as f:
                f.write('')

def redownload_single(i, filepath, url, crs, nodata):
    if i % 100 == 0:
        print(f'{i:_}')
    if os.path.isfile(f'{filepath}.done'):
        os.remove(f'{filepath}.done')
    if os.path.isfile(filepath):
        shutil.move(filepath, f'{filepath}.old')
    download.download(filepath, url, crs, nodata)

def redownload_blanks(source, crs, nodata):
    filepaths = glob(f'blank-checks/{source}/*')
    filename_potential_todos = [filepath.split('/')[-1] for filepath in filepaths]

    filename_todos = []
    for filename in filename_potential_todos:
        if has_rectangular_blank(1, f'source-store/{source}/{filename}'):
            filename_todos.append(filename)

    print(f'len(filename_todos) = {len(filename_todos)}')
    input('Press enter...')
    lines = []
    with open(f'file-lists/{source}/files.csv') as f:
        lines = [line.strip() for line in f.readlines()]

    filename_to_url = {}
    for line in lines:
        filename, url = line.split(' ')
        filename_to_url[filename] = url

    argument_tuples = []
    for i, filename in enumerate(filename_todos):
        filepath = f'source-store/{source}/{filename}'
        argument_tuples.append((i, filepath, filename_to_url[filename], crs, nodata))

    with Pool(10) as pool:
        pool.starmap(redownload_single, argument_tuples, chunksize=1)


if __name__ == '__main__':

    # source = 'frhd2154a'
    # crs = 'EPSG:2154'
    # nodata = '-9999'
    # check(source)
    # redownload_blanks(source, crs, nodata)

    source = 'frhd2154b'
    crs = 'EPSG:2154'
    nodata = '-9999'
    check(source)
    redownload_blanks(source, crs, nodata)

    # source = 'frhd2154c'
    # crs = 'EPSG:2154'
    # nodata = '-9999'
    # check(source)
    # redownload_blanks(source, crs, nodata)

    # source = 'frhd2154d'
    # crs = 'EPSG:2154'
    # nodata = '-9999'
    # check(source)
    # redownload_blanks(source, crs, nodata)

    # source = 'frhd2154e'
    # crs = 'EPSG:2154'
    # nodata = '-9999'
    # check(source)
    # redownload_blanks(source, crs, nodata)

    # source = 'frhd2975'
    # crs = 'EPSG:2975'
    # # nodata = '-9999'
    # # check(source)
    # redownload_blanks(source, crs, nodata)
    
    # source = 'frhd5490'
    # crs = 'EPSG:5490'
    # nodata = '-9999'
    # check(source)
    # redownload_blanks(source, crs, nodata)
