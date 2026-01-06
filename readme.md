# To run locally:

## install python venv
`uv venv --python 3.10 ` getting errors with 3.11/3.12 locally, 3.11 seems to be alright for SiS

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


# To run from Snowflake:
    copy the `setup.sql` into a Snowflake worksheet and run it -- this will create the git repo inside snowflake.
    Then execute each sql file to create the relevant streamlit application. e.g.
    ```sql
    EXECUTE IMMEDIATE FROM @THIRTY_DAYS.COMMON.DSMDAVID_GITHUB_30DAYS/branches/main/streamlit_in_snowflake/day_04.sql;
    ```
    The app is now created and ready to be used from snowsight > projects > streamlit
