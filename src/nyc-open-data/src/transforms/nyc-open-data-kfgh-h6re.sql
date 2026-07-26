-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "insptn_typ_cd_fk",
    "inspecting_unit_code",
    "borough",
    "latitude",
    "longitude",
    "communitydistrict",
    "citycouncildistrict",
    "insptn_ops_detail_pk",
    "insp_inspect_dt_fk",
    "bldg_current_bin_fk",
    "bbl"
FROM "nyc-open-data-kfgh-h6re"
