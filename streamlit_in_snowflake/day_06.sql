ALTER GIT REPOSITORY IF EXISTS dsmdavid_github_30days FETCH;
SET challenge_day = '06';
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

CREATE STREAMLIT IF NOT EXISTS IDENTIFIER('dsmdavid_30days_day_' || $challenge_day)
  FROM @THIRTY_DAYS.COMMON.DSMDAVID_GITHUB_30DAYS/branches/main/app
  MAIN_FILE = 'day' || $challenge_day || '.py'
  QUERY_WAREHOUSE = COMPUTE_WH
;

ALTER STREAMLIT IDENTIFIER('dsmdavid_30days_day_' || $challenge_day)  ADD LIVE VERSION FROM LAST;