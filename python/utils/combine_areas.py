import json
import requests

LONDON_URL = 'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/electoral/eng/wpc_by_lad/E090000%s.json'
# LONDON_URL = 'https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/electoral/eng/wards_by_lad/E090000%s.json'


DATA = '''
{
    "type": "FeatureCollection",
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
    "features": %s
}
'''


features = []

for i in range(1, 34):
    data = json.loads(requests.get(LONDON_URL % str(i).zfill(2)).text)
    fs = []

    for j, f in enumerate(data.get('features')):
        f['properties']['id'] = 'E%s-%s' % (i, j);
        fs.append(f)

    features.extend(fs)


with open('../../static/london.json', 'w') as f:
    f.write(DATA % json.dumps(features))


