-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Multiple observations may describe the same country and reporting period because rows preserve distinct upstream sources, data types, classifications, and model-use flags; do not treat country-period as unique.
SELECT
    "country",
    "iso",
    "yearstart",
    "yearend",
    "region",
    "subregion",
    "numberofabortions",
    "abortionrate",
    "perc_p_ending_in_a",
    "spontaneous",
    "datatype",
    "datasource",
    "complete",
    "classification",
    "modelused",
    "marriedonly",
    "notes"
FROM "guttmacher-institute-5k7fp"
