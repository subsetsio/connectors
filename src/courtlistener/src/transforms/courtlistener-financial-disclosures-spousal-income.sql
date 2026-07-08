SELECT
    TRY_CAST("id" AS BIGINT) AS "id",
    TRY_CAST("date_created" AS TIMESTAMP) AS "date_created",
    TRY_CAST("date_modified" AS TIMESTAMP) AS "date_modified",
    "source_type",
    "date_raw",
    "redacted",
    TRY_CAST("financial_disclosure_id" AS BIGINT) AS "financial_disclosure_id"
FROM "courtlistener-financial-disclosures-spousal-income"
