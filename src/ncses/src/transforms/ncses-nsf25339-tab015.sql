-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State outlying area and institution" AS state_outlying_area_and_institution,
    "DOJ" AS doj,
    "DOT" AS dot,
    "ED" AS ed,
    "EPA" AS epa,
    "HHS" AS hhs,
    "NASA" AS nasa,
    "NRC" AS nrc,
    "NSF" AS nsf,
    "SSA" AS ssa,
    "USDA" AS usda
FROM "ncses-nsf25339-tab015"
