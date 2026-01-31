#!/usr/bin/env python
"""Generate SQL deployment files for Streamlit apps.

Usage:
    python generate_sql.py --day 15
    python generate_sql.py --day 21

Output:
    Creates streamlit_in_snowflake/day_XX.sql
"""
import argparse
from pathlib import Path

TEMPLATE = """ALTER GIT REPOSITORY IF EXISTS dsmdavid_github_30days FETCH;
SET challenge_day = '{day}';
SET streamlit_identifier = 'dsmdavid_30days_day_' || $challenge_day;
SET file_id = 'day' || $challenge_day || '.py';
SET sql_stmnt = 'ALTER STREAMLIT ' || $streamlit_identifier || ' ADD LIVE VERSION FROM LAST';

/* the below does not work in trial accounts as external access is not supported
CREATE OR REPLACE NETWORK RULE dsmdavid_30days_day_05
  TYPE = HOST_PORT
  MODE = EGRESS
  VALUE_LIST = ('hpclaser.co.uk','bit.ly');


CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dsmdavid_30days_day_05
  ALLOWED_NETWORK_RULES = (dsmdavid_30days_day_05)
  ENABLED = TRUE;

CREATE STREAMLIT IF NOT EXISTS dsmdavid_30days_day_05
  FROM @THIRTY_DAYS.COMMON.DSMDAVID_GITHUB_30DAYS/branches/main/app
  MAIN_FILE = 'day05.py'
  QUERY_WAREHOUSE = COMPUTE_WH;
  EXTERNAL_ACCESS_INTEGRATIONS = (dsmdavid_30days_day_05);

-- end of comment to use the below instead of the above */

CREATE OR REPLACE STREAMLIT IDENTIFIER($streamlit_identifier)
  FROM @THIRTY_DAYS.COMMON.DSMDAVID_GITHUB_30DAYS/branches/main/app
  MAIN_FILE = $file_id
  QUERY_WAREHOUSE = COMPUTE_WH
;

-- this does not support the identifier
-- EXECUTE IMMEDIATE
-- ALTER STREAMLIT dsmdavid_30days_day_14  ADD LIVE VERSION FROM LAST;
EXECUTE IMMEDIATE $sql_stmnt;
"""


def main():
    parser = argparse.ArgumentParser(description="Generate SQL deployment file for a Streamlit app")
    parser.add_argument("--day", type=int, required=True, help="Day number (e.g., 15)")
    args = parser.parse_args()

    # Generate SQL content
    sql_content = TEMPLATE.format(day=args.day)

    # Determine output path (relative to this script's directory)
    script_dir = Path(__file__).parent
    output_dir = script_dir / "streamlit_in_snowflake"
    output_file = output_dir / f"day_{args.day:02d}.sql"

    # Write the file
    output_file.write_text(sql_content)
    print(f"Created: {output_file}")


if __name__ == "__main__":
    main()
