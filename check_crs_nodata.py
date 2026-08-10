import rasterio
import os
from multiprocessing import Pool
import json
from glob import glob
import warnings
from rasterio.errors import NotGeoreferencedWarning

warnings.filterwarnings("error", category=NotGeoreferencedWarning)

def check_single(i, source, filename):

    if i % 100 == 0:
        print(f'{i:_}')
    filepath = f'source-store/{source}/{filename}'
    crs = ''
    nodata = 0
    try:
        with rasterio.open(filepath) as src:
            crs = str(src.crs)
            nodata = src.nodata
    except Exception as e:
        print(f'source-store/{source}/{filename}')
        raise e
    with open(f'checks/{source}/{filename}.json', 'w') as f:
        json.dump({'crs': crs, 'nodata': nodata}, f, indent=2)
            
def check_all(source):
    os.makedirs(f'checks/{source}', exist_ok=True)
    filenames = []
    with open(f'file-lists/{source}/files.csv') as f:
        filenames = [line.split(' ')[0] for line in f.readlines()]
    
    for i, filename in enumerate(filenames):
        check_single(i, source, filename)


def analyze(source):
    filepaths = glob(f'checks/{source}/*.json')
    groups = {}
    for filepath in filepaths:
        data = {}
        with open(filepath) as f:
            data = json.load(f)
        fingerprint = (data['crs'], data['nodata'])
        if data['crs'] == 'None':
            print(filepath)
        if fingerprint not in groups.keys():
            groups[fingerprint] = []
        groups[fingerprint].append(filepath)

    print('source', source, len(groups.keys()), 'fingerprints (crs, nodata):')
    print()
    for key in groups.keys():
        print(key)
        print()



if __name__ == '__main__':
    
    # check_all('frhd2154a')
    # analyze('frhd2154a')

    # check_all('frhd2154b')
    # analyze('frhd2154b')

    # check_all('frhd2154c')
    # analyze('frhd2154c')

    # check_all('frhd2154d')
    # analyze('frhd2154d')

    # check_all('frhd2154e')
    # analyze('frhd2154e')

    # check_all('frhd2975')
    # analyze('frhd2975')

    check_all('frhd5490')
    analyze('frhd5490')
