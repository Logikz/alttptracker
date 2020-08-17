import json
import os

import postgres_connector


def generate_training_data():
    connector = postgres_connector.PostgresConnector()
    try:
        connection = connector.connect_to_db()

        details_data_frame = connector.execute_sql("select * from seed_details")
        # For each row, run sql on placements table for if location is good
        results = {
            'seed': []
        }
        for index, row in details_data_frame.iterrows():
            print(f"checking seed: {row['seed']}")
            results['seed'].append(int(row['seed']))
            for i in range(1, 232):
                col = f'loc{i}'
                col_name_sql = f"select name from locations where id={i}"
                # print(col_name_sql)
                col_name = connector.execute_sql(col_name_sql)

                sql = f"select distinct good_item from items, lateral item_good({row[col]}) good_item"
                # print(sql)
                good_item = connector.execute_sql(sql)

                results.setdefault(str(col_name['name'][0]), []).append(int(good_item['good_item']))
                #results.setdefault(str(col_name['name'][0]), []).append(int(row[col]))
        cwd = os.path.abspath(__file__)
        dir = os.path.abspath(os.path.join(cwd, os.pardir))
        filepath = os.path.join(dir, '..', 'data', 'good_item_by_location.json')
        with open(filepath, 'w+') as f:
            json.dump(results, f)
    finally:
        connector.cleanup()


generate_training_data()
