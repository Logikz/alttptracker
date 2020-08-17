import json
import os

import pandas
from flask import Flask, request, jsonify
from flask_cors import CORS
from pandas import DataFrame

import utils

app = Flask(__name__)
CORS(app)

print("Load the data")
# Load the dataset into a pandas dataframe
# with open(os.path.join(utils.get_data_dir(), 'good_item_by_location.json')) as f:
#     item_by_location = json.load(f)
# item_by_location_df = DataFrame(item_by_location)
item_by_location_df = pandas.read_parquet(os.path.join(utils.get_data_dir(), 'good_item_by_location.parquet.gzip'))
print("Data loaded")

@app.route('/predict', methods=['POST'])
def predict_route():
    """
    Do route prediction
    :return:
    """
    body = request.json
    app.logger.debug(body)

    # Load info from the body
    checked = body['current_state']
    available = body['available']

    # Figure out what we need to filter on
    sum_good_items = sum(checked.values())
    keys = checked.keys()

    print("Find similar seeds")

    good_seed_df = item_by_location_df[(item_by_location_df[keys].sum(axis=1) >= sum_good_items - 2) &
                                       (item_by_location_df[keys].sum(axis=1) <= sum_good_items + 2)]

    if len(good_seed_df.index) == 0:
        # Unable to come up with a prediction for this game state
        return []

    # Now sum up each column in 'available'
    available_strength = good_seed_df[available].sum(axis=0).apply(lambda x: x/len(good_seed_df.index))
    print("Seeds located")
    print("Sort the data")

    # Cluster similar areas together since each chest is an independent choice to get a good item, so we want to
    # go to clustered areas
    # find the set of unique areas
    areas = set()
    for location, strength in available_strength.items():
        # The area might be partitioned by dashes, so take everything but the last segment as a unique area
        if('Castle Tower' in location):
            continue
        if('C-Shaped' in location):
            areas.add(location)
        else:
            areas.add(''.join(location.split('-')[0]).strip())

    # Now for each unique area, create a tuple of that area with a count of how many good items appear in that area
    locations_by_priority = []
    for area in areas:
        area_sum = 0
        for location, strength in available_strength.items():
            if area in location:
                area_sum += strength
        locations_by_priority.append((area, round(area_sum, 2)))

    # now sort the areas by priority
    # priority_locations = sorted(locations_by_priority, key=lambda x: x[1], reverse=True)

    result = jsonify(dict(locations_by_priority))
    app.logger.debug(result)
    return result


if __name__ == '__main__':
    app.run(debug=False)
