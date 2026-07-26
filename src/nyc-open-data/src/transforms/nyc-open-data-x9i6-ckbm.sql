-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nta",
    "nta_name",
    "borough",
    "boro_code",
    "company",
    "conduit_route_mileage",
    "street_mileage",
    "conduit_mileage_total",
    "conduit_mileage_available",
    "conduit_mileage_available_1",
    "cd_overlap_1",
    "cd_overlap_2",
    "cd_overlap_3",
    "cd_overlap_4",
    "cd_overlap_5",
    "cd_overlap_6"
FROM "nyc-open-data-x9i6-ckbm"
