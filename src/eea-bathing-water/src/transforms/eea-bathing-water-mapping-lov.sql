-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Vocabulary rows cover multiple coded fields; filter by tableName or notation before joining labels to a fact table.
SELECT
    "altLabel" AS altlabel,
    "broader",
    "broadMatch" AS broadmatch,
    "definition",
    "id",
    "label",
    "notation",
    "sameAs" AS sameas,
    "statusCode" AS statuscode,
    strptime("statusDate", '%Y-%m-%d')::DATE AS statusdate,
    "statusRemarks" AS statusremarks,
    "tableName" AS tablename,
    "URI" AS uri
FROM "eea-bathing-water-mapping-lov"
