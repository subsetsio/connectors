-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("organizationtypeid" AS BIGINT) AS organizationtypeid,
    "organizationcode",
    "name",
    CAST("startdate" AS TIMESTAMP) AS startdate,
    CAST("enddate" AS TIMESTAMP) AS enddate
FROM "u-s-department-of-transportation-rx2s-7tqf"
