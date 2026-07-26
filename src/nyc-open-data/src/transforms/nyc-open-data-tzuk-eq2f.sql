-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "status",
    "borough",
    "gispropnum",
    "omppropid",
    "subpropertyname",
    "propertyname",
    "feature",
    "_system" AS system,
    "featuretype",
    "district",
    "x",
    "y"
FROM "nyc-open-data-tzuk-eq2f"
