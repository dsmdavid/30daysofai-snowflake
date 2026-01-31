# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a "30 Days of AI with Snowflake" challenge project containing Streamlit applications that demonstrate Snowflake AI/ML capabilities. Each day (`day01.py` through `day21.py`) is a standalone Streamlit app showcasing different features like Cortex ML functions, embeddings, RAG pipelines, and Cortex Search.

## Development Setup

```bash
# Create Python 3.10 virtual environment (3.11/3.12 have local compatibility issues)
uv venv --python 3.10
source .venv/bin/activate
uv pip install -r requirements.txt

# Create Snowflake connection config
# .streamlit/secrets.toml with [connections.snowflake] section
```

## Running Apps

```bash
# Run locally
streamlit run app/dayXX.py

# Deploy to Snowflake (in Snowflake worksheet)
EXECUTE IMMEDIATE FROM @THIRTY_DAYS.COMMON.DSMDAVID_GITHUB_30DAYS/branches/main/streamlit_in_snowflake/day_XX.sql;
```

## Architecture

### Dual-Environment Pattern
All apps use a try/except pattern to work in both environments:
```python
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()  # Streamlit in Snowflake
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()  # Local
```

### Directory Structure
- `app/` - Streamlit Python apps (one per challenge day)
- `streamlit_in_snowflake/` - SQL deployment scripts for each app
- `setup.sql` - Initial Snowflake setup (creates git repo integration in Snowflake)

### SQL Deployment Scripts
Each `day_XX.sql` uses variables to create/update Streamlit apps:
```sql
SET challenge_day = 'XX';
SET streamlit_identifier = 'dsmdavid_30days_day_' || $challenge_day;
CREATE OR REPLACE STREAMLIT IDENTIFIER($streamlit_identifier)
  FROM @THIRTY_DAYS.COMMON.DSMDAVID_GITHUB_30DAYS/branches/main/app
  MAIN_FILE = $file_id
  QUERY_WAREHOUSE = COMPUTE_WH;
EXECUTE IMMEDIATE $sql_stmnt;  -- For live version update
```

## Key Dependencies
- `streamlit` - Web app framework
- `snowflake-snowpark-python` - Snowflake Python API
- `snowflake-ml-python` - Snowflake ML functions (Cortex)
