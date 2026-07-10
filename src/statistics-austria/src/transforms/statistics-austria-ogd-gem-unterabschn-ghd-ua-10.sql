-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "commune_2413",
    "estimate_of_costs_sections",
    "expenditures",
    "revenues"
FROM "statistics-austria-ogd-gem-unterabschn-ghd-ua-10"
