-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "seq_no",
    "instn_code",
    "instn_name",
    "instn_srvc_type_cde",
    "instn_srvc_type",
    "instn_blk_hse_no",
    "instn_street_name",
    "instn_flr_no",
    "instn_unit_no",
    "instn_bldg_name",
    "instn_pc",
    "instn_ofc_no",
    "instn_email",
    "ap_user_name"
FROM "sg-data-d-2509dfdb3d6b87606fe909dd72fbb9fb"
