-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Academic year" AS academic_year,
    "EQGRP" AS eqgrp,
    "Equality group" AS equality_group,
    "FSMSEN" AS fsmsen,
    "SEN and free school meals" AS sen_and_free_school_meals,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-desceq"
