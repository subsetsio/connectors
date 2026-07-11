-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes forecast geography levels; filter `level` before treating rows as comparable areas.
SELECT
    "code",
    "level",
    "name_ja",
    "name_en",
    "office_name",
    "parent"
FROM "japan-meteorological-agency-forecast-areas"
