from google.cloud import bigquery
from dotenv import load_dotenv
import pprint

load_dotenv()

"""
this query filters 200 million rows from total 1 billion rows of data as outliers
based on fare amount and travel path. after that this shows row counts, minimum and maximum fares in the remaining rows
and average and standard deviation of the fare amount. we should get as close as possible to this average and stddev
in our prediction results
"""


def show_data_stats():
    client = bigquery.Client()

    query_job = client.query(
        """
        SELECT
  COUNT(fare_amount) AS num_fares,
  MIN(fare_amount) AS low_fare,
  MAX(fare_amount) AS high_fare,
  AVG(fare_amount) AS avg_fare,
  STDDEV(fare_amount) AS stddev
FROM
`nyc-tlc.yellow.trips`
WHERE trip_distance > 0 AND fare_amount BETWEEN 6 and 200 #only keeping usual prices
    AND pickup_longitude > -75 #limiting the taxis to newyork city only
    AND pickup_longitude < -73
    AND dropoff_longitude > -75
    AND dropoff_longitude < -73
    AND pickup_latitude > 40
    AND pickup_latitude < 42
    AND dropoff_latitude > 40
    AND dropoff_latitude < 42
    # 827,365,869 fares
        """
    )
    print("-- getting job results")
    results = query_job.result()
    for row in results:
        # print("{} : {} views".format(row.url, row.view_count))
        pprint.pprint(dict(row))


if __name__ == "__main__":
    show_data_stats()