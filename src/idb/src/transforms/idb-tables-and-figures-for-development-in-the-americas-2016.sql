-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Year" AS year,
    "Latin_America_and_the_Caribbean" AS latin_america_and_the_caribbean,
    "Emerging_Asia" AS emerging_asia,
    "Advanced_economies" AS advanced_economies,
    "source_resource"
FROM "idb-tables-and-figures-for-development-in-the-americas-2016"
