import os
import subprocess
from multiprocessing import Pool

SILENT = False

def run_command(command, silent=True, env=None):
    if env is None:
        env = os.environ.copy()
    if not silent:
        print(command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    stdout, stderr = p.communicate()
    err = stderr.decode()
    if err != '' and not silent:
        print(err)
    out = stdout.decode()
    if out != '' and not silent:
        print(out)
    return out, err

def download(filepath, url, crs, nodata):
    if os.path.isfile(f'{filepath}'):
        return
    
    print(f'downloading {filepath}')
    command = f'wget "{url}" -O "{filepath}.orig"'
    run_command(command, silent=SILENT)

    command = f'GDAL_CACHEMAX=512 gdal_translate -a_srs {crs} -a_nodata {nodata} -of COG -co BLOCKSIZE=512 -co OVERVIEWS=NONE -co SPARSE_OK=YES -co BIGTIFF=YES -co COMPRESS=LERC -co MAX_Z_ERROR=0.001 "{filepath}.orig" "{filepath}"'
    run_command(command, silent=SILENT)

    os.remove(f'{filepath}.orig')
    
    command = f'touch {filepath}.done'
    run_command(command, silent=SILENT)
    

def download_all(source, crs, nodata): 
    lines = []

    with open(f'file-lists/{source}/files.csv') as f:
        lines = [line.strip() for line in f.readlines()]

    filename_to_url = {}
    for line in lines:
        filename, url = line.split(' ')
        filename_to_url[filename] = url

    os.makedirs(f'source-store/{source}', exist_ok=True)
    argument_tuples = []
    for filename in filename_to_url.keys():
        filepath = f'source-store/{source}/{filename}'
        argument_tuples.append((filepath, filename_to_url[filename], crs, nodata))
    
    with Pool(4) as pool:
        pool.starmap(download, argument_tuples, chunksize=1)

if __name__ == '__main__':

    nodata = '-9999'

    crs = 'EPSG:2154'
    # download_all('frhd2154a', crs, nodata)
    # download_all('frhd2154b', crs, nodata)
    download_all('frhd2154c', crs, nodata)
    exit(0)
    download_all('frhd2154d', crs, nodata)
    download_all('frhd2154e', crs, nodata)

    crs = 'EPSG:2975'
    download_all('frhd2975', crs, nodata)

    crs = 'EPSG:5490'
    download_all('frhd5490', crs, nodata)