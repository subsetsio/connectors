-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "description",
    "date_of_vac_order",
    "bldg_tx_boro",
    "aka_address",
    "bldg_community_dist",
    "council_district",
    "bin",
    "bbl",
    "lst_compl_insp_date",
    "status_change_date",
    "ocpcy_desc"
FROM "nyc-open-data-n5xc-7jfa"
