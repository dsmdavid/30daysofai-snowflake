# To run locally:

## install python venv
`uv venv --python 3.10 ` getting errors with 3.11/3.12.

`source .venv/bin/activate`
`uv pip install -r requirements.txt`

## config toml for streamlit connection
create file `.streamlit/secrets.toml`
```toml
[connections.snowflake]
account = "your_account_identifier"
user = "your_username"
password = "your_password"
role = "ACCOUNTADMIN"
warehouse = "COMPUTE_WH"
database = "your_database"
schema = "your_schema"
```

## running the streamlit apps
`source .venv/bin/activate`
`streamlit run app/day01.py`