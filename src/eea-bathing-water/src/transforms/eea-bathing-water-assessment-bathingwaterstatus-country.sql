-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are already country-level counts by season, specialised zone type, and quality class; do not join to bathing-water-level tables and then sum without preserving this aggregate grain.
SELECT
    "countryCode" AS countrycode,
    "numberOfBathingWaters" AS numberofbathingwaters,
    "quality",
    "season",
    "specialisedZoneType" AS specialisedzonetype
FROM "eea-bathing-water-assessment-bathingwaterstatus-country"
