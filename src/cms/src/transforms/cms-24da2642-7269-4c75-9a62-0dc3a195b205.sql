-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Name of Initiative" AS name_of_initiative,
    "Participating Practice" AS participating_practice,
    "Participating Practice Location" AS participating_practice_location,
    "State" AS state,
    "City" AS city,
    "Geographic Reach" AS geographic_reach,
    "Street Address" AS street_address,
    "Zip Code" AS zip_code
FROM "cms-24da2642-7269-4c75-9a62-0dc3a195b205"
