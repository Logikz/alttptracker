import json
import os

from pandas import DataFrame

import utils

with open(os.path.join(utils.get_data_dir(), 'good_item_by_location.json')) as f:
    item_by_location = json.load(f)
item_by_location_df = DataFrame(item_by_location)

item_by_location_df.to_parquet(os.path.join(utils.get_data_dir(), 'good_item_by_location.parquet.gzip'),
                               compression='gzip')