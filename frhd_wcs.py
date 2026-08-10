# Written by ChatGPT 5.3

import requests
import json
import os

WFS_URL = "https://data.geopf.fr/wfs/ows"

PARAMS = {
    "SERVICE": "WFS",
    "VERSION": "2.0.0",
    "REQUEST": "GetFeature",
    "TYPENAMES": "IGNF_MNT-LIDAR-HD:dalle",
    "OUTPUTFORMAT": "application/json",
    "COUNT": 1000  # batch size
}

def fetch_all_features():
    start_index = 0
    total_fetched = 0
    all_features = []

    while True:
        params = PARAMS.copy()
        params["STARTINDEX"] = start_index

        print(f"\n--- Fetching batch starting at {start_index} ---")

        response = requests.get(WFS_URL, params=params, stream=True)
        response.raise_for_status()

        data = response.json()
        features = data.get("features", [])

        if not features:
            print("No more features.")
            break

        all_features += features

        for feature in features:
            print(feature)  # print as soon as loaded
            total_fetched += 1

        start_index += len(features)

        # Stop if fewer features returned than requested (last page)
        if len(features) < PARAMS["COUNT"]:
            break

    with open('frhd_features.json', 'w') as f:
        json.dump(all_features, f, indent=2)

    print(f"\nTotal features fetched: {total_fetched}")


def get_group(filename):
    parts = filename.split('_')
    x = int(parts[2])
    y = int(parts[3])
    is_corsica = (x >= 1156)
    is_left = (x < 686)
    is_bottom = (y < 6584)

    if is_corsica:
        return 'e'
    if is_left:
        if is_bottom:
            return 'c'
        else:
            return 'a'
    else:
        if is_bottom:
            return 'd'
        else:
            return 'b'

def check_crses():
    features = []
    with open('frhd_features.json') as f:
        features = json.load(f)

    source_to_features = {
        'frhd2975': [],
        'frhd5490': [],
        'frhd2154a': [],
        'frhd2154b': [],
        'frhd2154c': [],
        'frhd2154d': [],
        'frhd2154e': [],
    }

    for feature in features:
        crs = feature['properties']['projection']
        source = None
        if crs == 'EPSG:2154':
            group = get_group(feature['properties']['name'])
            source = f'frhd2154{group}'
        else:
            source = f'frhd{crs.replace("EPSG:", "")}'
        source_to_features[source].append(feature)

    for source in source_to_features.keys():
        lines = []
        known_names = set()
        for feature in source_to_features[source]:
            name = feature['properties']['name_download']
            if name in known_names:
                continue
            known_names.add(name)
            lines.append(f'{name} {feature["properties"]["url"]}')
        lines.sort()
        os.makedirs(source, exist_ok=True)
        with open(f'file-lists/{source}/files.csv', 'w') as f:
            f.write('\n'.join(lines))
        with open(f'file-lists/{source}/files.geojson', 'w') as f:
            json.dump({'type': 'FeatureCollection', 'features': source_to_features[source]}, f, indent=2)
    

if __name__ == "__main__":
    # fetch_all_features()
    check_crses()