-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "Indices_1" AS indices_1,
    "ChangesComparedToOneYearEarlier_2" AS changescomparedtooneyearearlier_2,
    "Indices_3" AS indices_3,
    "ChangesComparedToOneYearEarlier_4" AS changescomparedtooneyearearlier_4,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80334eng"
