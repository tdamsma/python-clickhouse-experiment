#%%
import numpy as np
import pandas as pd
from time import time, sleep
from clickhouse_driver import Client
from random import randint


def intialize_db_client():
    client = Client(
        host="localhost",
        port="9015",
        settings={"use_numpy": True, "max_partitions_per_insert_block": n_columns},
    )
    # client.execute("DROP TABLE IF EXISTS floats")
    client.execute(
        "CREATE TABLE IF NOT EXISTS floats (time datetime64, key String, value Float32) ENGINE = MergeTree "
        "ORDER BY (key,time)"
    )
    return client


#%%
def generate_random_walks(n_rows, n_columns):
    """Generate random data."""
    return np.cumsum(
        np.random.standard_normal(
            (n_rows, n_columns),
        ),
        axis=0,
    )


def generate_data(start, end, n_columns, n_rows):
    timestamps = pd.date_range(
        start=start * 1000000000,
        end=end * 1000000000,
        periods=n_rows + 1,
        closed="left",
    )
    df = pd.DataFrame(
        index=timestamps,
        data=generate_random_walks(n_rows, n_columns),
        columns=(f"Label{n:04d}" for n in range(n_columns)),
    )
    # convert to time/key/value triplet
    return (
        df.melt(var_name="key", value_name="value", ignore_index=False)
        .reset_index()
        .rename(columns={"index": "time"})
    )


if __name__ == "__main__":
    t0 = time()
    t_prev = t0
    n_columns = 10000  # number of distinct columns/keys/labels
    n_rows = 1000  # number of rows to insert in a batch
    client = intialize_db_client()
    while True:
        sleep(randint(0, 2))
        t1 = time()
        time_key_value_array = generate_data(
            start=t_prev, end=time(), n_columns=n_columns, n_rows=n_rows
        )
        t2 = time()
        print(
            f"{len(time_key_value_array):,d} samples generated in {t2 - t1:0.3f}",
            end="",
        )
        client.insert_dataframe("INSERT INTO floats VALUES", time_key_value_array)
        t3 = time()
        print(f", inserted in {t3 - t2:0.3f}. Total: {t3 - t0:0.3f}")
        t_prev = t0
        t0 = time()
