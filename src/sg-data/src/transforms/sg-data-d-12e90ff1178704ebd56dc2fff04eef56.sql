-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ozone_maximum_8hour_mean"
FROM "sg-data-d-12e90ff1178704ebd56dc2fff04eef56"
