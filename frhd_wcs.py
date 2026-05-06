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


def check_crses():
    features = []
    with open('frhd_features.json') as f:
        features = json.load(f)
    crs_to_features = {}
    for feature in features:
        crs = feature['properties']['projection']
        if crs not in crs_to_features:
            crs_to_features[crs] = []
        crs_to_features[crs].append(feature)
    
    for crs in crs_to_features.keys():
        lines = []
        for feature in crs_to_features[crs]:
            lines.append(f'{feature["properties"]["name_download"]},{feature["properties"]["url"]}')
        lines.sort()
        folder = f'frhd{crs.replace("EPSG:", "")}'
        os.makedirs(folder, exist_ok=True)
        with open(f'{folder}/files.csv', 'w') as f:
            f.write('\n'.join(lines))
    

if __name__ == "__main__":
    # fetch_all_features()
    check_crses()