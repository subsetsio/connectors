-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "borough",
    "community_district",
    "adult_family_comm_hotel",
    "adult_family_shelter",
    "adult_shelter",
    "adult_shelter_comm_hotel",
    "fwc_cluster",
    "fwc_comm_hotel",
    "fwc_shelter"
FROM "nyc-open-data-3qem-6v3v"
