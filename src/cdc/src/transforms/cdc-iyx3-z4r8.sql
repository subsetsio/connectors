-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "UniqueID" AS uniqueid,
    "WherePrepName" AS whereprepname,
    CAST("EtiologyKnown" AS BIGINT) AS etiologyknown,
    "GenusName" AS genusname,
    "SpeciesName" AS speciesname,
    "SerotypeName" AS serotypename,
    strptime("DateFirstIll", '%m/%d/%Y')::DATE AS datefirstill
FROM "cdc-iyx3-z4r8"
