-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "parameter_name",
    "unit_of_measure",
    "parameter_group_code",
    "parameter_description",
    "medium",
    "statistical_basis",
    "time_basis",
    "weight_basis",
    "particle_size_basis",
    "sample_fraction",
    "temperature_basis",
    "epa_equivalence",
    "_lon" AS lon,
    "_lat" AS lat
FROM "usgs-parameter-codes"
