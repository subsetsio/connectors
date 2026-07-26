-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "borough",
    "community_districts",
    "census_type",
    "adult_family_commercial_hotel",
    "adult_family_shelter",
    "adult_shelter",
    "adult_shelter_commercial_hotel",
    "family_cluster",
    "family_with_children_commercial_hotel",
    "family_with_children_shelter"
FROM "nyc-open-data-veav-vj3r"
