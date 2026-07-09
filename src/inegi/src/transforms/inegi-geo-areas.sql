-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Mixes three administrative levels in one column: '0000' national, 2-digit state codes, 5-digit municipality codes (state prefix + municipality suffix). Filter by code length before counting areas.
SELECT
    "code",
    "description"
FROM "inegi-geo-areas"
