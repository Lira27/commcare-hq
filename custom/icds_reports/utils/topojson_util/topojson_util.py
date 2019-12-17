import json
import os
from pathlib import Path

import attr

@attr.s
class TopojsonFile:
    path = attr.ib()
    topojson_text = attr.ib()
    topojson = attr.ib()

    def get_formatted_topojson(self):
        return json.dumps(self.topojson, indent=2)


def get_topojson_directory():
    return os.path.join(Path(__file__).parent.parent.parent, 'static', 'js', 'topojsons')


def _get_topojson_file(filename, truncate_before):
    path = os.path.join(get_topojson_directory(), filename)
    with open(path) as f:
        content = f.read()
        # strip off e.g. 'var BLOCK_TOPOJSON = ' from the front of the file and '\n;' from the end
        topojson_text = content[truncate_before:][:-2]
        return TopojsonFile(path, topojson_text, json.loads(topojson_text))


def get_block_topojson_file():
    return _get_topojson_file('blocks_v3.topojson.js', truncate_before=21)


def get_district_topojson_file():
    return _get_topojson_file('districts_v2.topojson.js', truncate_before=24)


def get_state_topojson_file():
    return _get_topojson_file('states_v2.topojson.js', truncate_before=21)


def get_state_v3_topojson_file():
    return _get_topojson_file('states_v3_small.topojson.js', truncate_before=21)


def get_topojson_file_for_level(level):
    level_function_map = {
        "state": get_state_topojson_file,
        "district": get_district_topojson_file,
        "block": get_block_topojson_file,
    }
    if level not in level_function_map:
        raise ValueError("Level must be one of: {}".format(', '.join(level_function_map.keys())))

    return level_function_map[level]()

def get_topojson_for_district(district):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

    district_topojson_data_path = os.path.join(path, 'district_topojson_data.json')
    district_topojson_data = json.loads(open(district_topojson_data_path, encoding='utf-8').read())

    for state, data in district_topojson_data.items():
        if district in data['districts']:
            with open(os.path.join(path, 'blocks/' + data['file_name']), encoding='utf-8') as f:
                return json.loads(f.read())
