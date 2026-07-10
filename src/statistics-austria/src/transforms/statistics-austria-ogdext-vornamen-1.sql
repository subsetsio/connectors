-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("jahr" AS BIGINT) AS jahr,
    "politischer_bezirk",
    "geschlecht",
    "vorname_normalisiert",
    "f_anzahl_lgeb"
FROM "statistics-austria-ogdext-vornamen-1"
