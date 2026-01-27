import streamlit as st
# import json
# import time
from snowflake.snowpark.functions import ai_complete

# Connect to Snowflake
print('creating session')
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

stg = session.get_session_stage()
print(stg)

res = session.sql('''
with base as (
select * exclude (L_EXTENDEDPRICE)
from temp.tst.lineitem
)

select hash_agg(*) from base
'''
)
print('res df created')
res.show()
print('res printed')


remote_file_path = f"{session.get_session_stage()}/full_hash.csv"
copy_result = res.write.csv(remote_file_path, overwrite=True, single=True)
print('res object saved to stage')
print(copy_result)
print('files in stage:')
files = session.sql(f'ls {stg}')
files.show()



full_df = session.sql('''
with base as (
select * exclude (L_EXTENDEDPRICE)
from temp.tst.lineitem
)

select hash(*) as hashed, * from base
'''
)

print('full_df created')
remote_file_path = f"{session.get_session_stage()}/all_hashes.csv"

copy_result = full_df.write.csv(remote_file_path, overwrite=True, single=False)

print('full_df saved')
print(copy_result)

print(full_df.count(), '\t records')

files = session.sql(f'ls {stg}')
files.show()
