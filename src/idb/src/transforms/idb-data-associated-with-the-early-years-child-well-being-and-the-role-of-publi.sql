-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Figure_Table" AS figure_table,
    "Title" AS title,
    "Indicator" AS indicator,
    "Sub-indicator" AS sub_indicator,
    "Year" AS year,
    "Quintile" AS quintile,
    "Country" AS country,
    CAST("Value" AS DOUBLE) AS value,
    "Source" AS source,
    "Notes" AS notes,
    "source_resource"
FROM "idb-data-associated-with-the-early-years-child-well-being-and-the-role-of-publi"
