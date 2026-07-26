-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_system" AS system,
    "df_activated",
    "fountaintype",
    "fountaincount",
    "painted",
    "filter_installed",
    "position",
    "outdoor",
    "gispropnum",
    "propertyname",
    "omppropid",
    "subpropertyname",
    "parkdistrict",
    "borough",
    "ampsid",
    "ampsclass",
    "ampsstatus",
    "ampsparentid",
    "ampsname",
    "communityboard",
    "councildistrict",
    "precinct",
    "zipcode",
    "x",
    "y"
FROM "nyc-open-data-wxhr-qbhz"
