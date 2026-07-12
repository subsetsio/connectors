-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table includes species, races, and unidentified taxon groupings, so rows are BBS taxa rather than only biological species.
SELECT
    CAST("Seq" AS BIGINT) AS seq,
    "AOU" AS aou,
    "English_Common_Name" AS english_common_name,
    "French_Common_Name" AS french_common_name,
    "Order" AS order,
    "Family" AS family,
    "Genus" AS genus,
    "Species" AS species
FROM "north-american-breeding-bird-survey-species-list"
