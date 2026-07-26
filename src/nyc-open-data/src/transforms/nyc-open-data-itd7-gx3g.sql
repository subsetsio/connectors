-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "insptn_ops_detail",
    "insptn_typ_cd",
    "insp_inspect_dt",
    "inspecting_unit_code",
    "bldg_current_bin_fk",
    "borough",
    "latitude",
    "longitude",
    "communitydistrict",
    "citycouncildistrict",
    "bbl",
    "location_1"
FROM "nyc-open-data-itd7-gx3g"
