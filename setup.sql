CREATE DATABASE IF NOT EXISTS THIRTY_DAYS;
CREATE SCHEMA IF NOT EXISTS THIRTY_DAYS.COMMON;
USE SCHEMA THIRTY_DAYS.COMMON;

CREATE SECRET IF NOT EXISTS dsmdavid_git_30days
    TYPE = password
    USERNAME = 'dsmdavid'
    PASSWORD = '<github_pat_token>';

CREATE API INTEGRATION IF NOT EXISTS dsmdavid_github
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/dsmdavid')
  ALLOWED_AUTHENTICATION_SECRETS = ( THIRTY_DAYS.COMMON.dsmdavid_git_30days )
  ENABLED = TRUE
  COMMENT = 'Integration for 30 days of AI - Snowflake'
  ;


CREATE GIT REPOSITORY IF NOT EXISTS dsmdavid_github_30days
  ORIGIN = 'https://github.com/dsmdavid/30daysofai-snowflake'
  API_INTEGRATION = dsmdavid_github
  GIT_CREDENTIALS = THIRTY_DAYS.COMMON.dsmdavid_git_30days
  COMMENT = 'David''s Repository for 30 days of AI - Snowflake'
  ;

ALTER GIT REPOSITORY IF EXISTS dsmdavid_github_30days FETCH;
