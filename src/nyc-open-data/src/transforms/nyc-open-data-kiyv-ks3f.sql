-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "loccode",
    "prek_type",
    "borough",
    "locname",
    "note",
    "phone",
    "address",
    "postcode",
    "day_length",
    "seats",
    "x",
    "y",
    "email",
    "website",
    "meals",
    "indoor_outdoor",
    "extended_day",
    "sems_code",
    "latitude",
    "longitude",
    "community_board",
    "council_district",
    "census_tract",
    "bin",
    "bbl",
    "nta"
FROM "nyc-open-data-kiyv-ks3f"
