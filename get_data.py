#%%
from clickhouse_driver import Client

client = Client(
    host="localhost",
    port="9015",
    settings={"use_numpy": True},
)


#%%
client.query_dataframe(
    "SELECT * FROM floats WHERE key='Label0000' LIMIT 1000"
).set_index("time").plot()

# %%
