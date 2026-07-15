-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "usr_mcno",
    "usr_mctype",
    "sub_mcno",
    "usr_mcstuen",
    "usr_devtname",
    "devt_location",
    "mcst_houseno",
    "mcst_roadname",
    "mcst_unitno",
    "mcst_buildingname",
    "mcst_postalcode",
    "mcst_telno",
    "ust_status",
    "mcst_stratalota",
    "managementname",
    "mc_form_date"
FROM "sg-data-d-1f9391a2f1476cdaf4f05a8d3a05c257"
