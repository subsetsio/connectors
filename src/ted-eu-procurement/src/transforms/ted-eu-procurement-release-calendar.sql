-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The calendar includes scheduled future OJ S issue dates for the current year as well as already published issues.
SELECT
    "asset_id",
    "year",
    "ojs_issue_number",
    CAST("issue_token" AS BIGINT) AS issue_token,
    "publication_date"
FROM "ted-eu-procurement-release-calendar"
