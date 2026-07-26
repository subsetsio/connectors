-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "status",
    "featuretype",
    "propertyname",
    "subpropertyname",
    "gispropnum",
    "omppropid",
    "borough",
    "district",
    "x",
    "y"
FROM "nyc-open-data-h2bn-gu9k"
