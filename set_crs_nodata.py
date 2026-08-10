from glob import glob

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

def set_single_crs_nodata(filepath, crs, nodata):
    run_command(f'mv "{filepath}" "{filepath}.bak"', silent=SILENT)
    run_command(f'gdal_translate -a_srs {crs} -a_nodata {nodata} -of COG -co BLOCKSIZE=512 -co OVERVIEWS=NONE -co SPARSE_OK=YES -co BIGTIFF=YES -co COMPRESS=LERC -co MAX_Z_ERROR=0.001 "{filepath}.bak" "{filepath}"', silent=SILENT)
    run_command(f'rm "{filepath}.bak"', silent=SILENT)

def set_all_crs_nodata(source, crs, nodata):
    filepaths = sorted(glob(f'source-store/{source}/*.tif'))
    argument_tuples = []
    for filepath in filepaths:
        argument_tuples.append((filepath, crs, nodata))
    
    with Pool() as pool:
        pool.starmap(set_single_crs_nodata, argument_tuples, chunksize=1)

if __name__ == '__main__':
    set_all_crs_nodata('frhd2154a', 'EPSG:2154', -9999.0)
    set_all_crs_nodata('frhd2154b', 'EPSG:2154', -9999.0)
    set_all_crs_nodata('frhd2154c', 'EPSG:2154', -9999.0)
    set_all_crs_nodata('frhd2154d', 'EPSG:2154', -9999.0)
    set_all_crs_nodata('frhd2154e', 'EPSG:2154', -9999.0)
    set_all_crs_nodata('frhd2975', 'EPSG:2975', -9999.0)