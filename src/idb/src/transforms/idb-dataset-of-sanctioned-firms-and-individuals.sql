-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Title" AS title,
    "Entity" AS entity,
    "Nationality" AS nationality,
    "Country" AS country,
    CAST("From" AS TIMESTAMP) AS from,
    "To" AS to,
    "Prohibited_Practice" AS prohibited_practice,
    "Source" AS source,
    "Tipo_de_sancion_del_BID" AS tipo_de_sancion_del_bid,
    "IDB_Sanction_Source" AS idb_sanction_source,
    "Other_Name" AS other_name,
    "source_resource"
FROM "idb-dataset-of-sanctioned-firms-and-individuals"
