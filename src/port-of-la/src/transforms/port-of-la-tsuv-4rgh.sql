-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month_year",
    CAST("date" AS TIMESTAMP) AS date,
    CAST("monthly_total_teus" AS DOUBLE) AS monthly_total_teus,
    CAST("cytd_total_teus" AS DOUBLE) AS cytd_total_teus,
    CAST("previous_year_cytd" AS DOUBLE) AS previous_year_cytd,
    CAST("change_total_teus_cytd" AS DOUBLE) AS change_total_teus_cytd
FROM "port-of-la-tsuv-4rgh"
