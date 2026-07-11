-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes countries, territories, gas baskets, source variants, scenarios, provenance methods, and IPCC categories; filter these dimensions before aggregating values.
SELECT
    "source",
    "scenario",
    "provenance",
    "area",
    "entity",
    "unit",
    "category",
    "year",
    "value",
    "release_version",
    "release_doi"
FROM "primap-hist-emissions"
