-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "team_name",
    "cd_name",
    "cd_number",
    "cert_status",
    "updated"
FROM "nyc-open-data-b2gb-nkrq"
