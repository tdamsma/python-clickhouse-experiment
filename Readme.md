# Python/numpy/pandas/clickhouse/grafana

What a wonderful combination. This demo shows how to create and insert millions of datapoints from python to clickhouse, and view the result in a grafana dashboard.

## How to use

Requires docker-compose to be installed. Clickhouse server and grafana can be started with:

    docker-compose up 

To run the python script, make sure you are in a suitable environment (tested only with python3.10 but will probably work with many other versions). The script continuously uploads batches of 10M datapoints; 1,000 rows * 10,000 cols

    pip install -r requirements.txt
    python clickhouse-insert-load-test.py

To view the data in grafana:

 - open http://localhost:3000
 - use admin/admin, then skip account creation
 - Open Demo dashboard
 - Set time range to last 5 minutes

The dashboard shows one of the 10,000 rows. You can zoom in until millisecond resolution