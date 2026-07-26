-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cmt_corner_id",
    "street_name1",
    "street_name2",
    "borough",
    "community_district",
    "block",
    "lot",
    "complaint_id",
    "complaint_date",
    "temp_repair_feasible",
    "temp_repair_date",
    "temp_repair_type",
    "second_temp_repair_needed",
    "date_second_temp_repair",
    "bulkcomplaint"
FROM "nyc-open-data-jagj-gttd"
