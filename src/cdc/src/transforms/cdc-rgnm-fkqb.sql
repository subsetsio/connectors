-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Mmwrweek_end" AS mmwrweek_end,
    "Level" AS level,
    "State" AS state,
    "Tests" AS tests,
    "Detections" AS detections,
    "Percent_pos" AS percent_pos,
    "Subtype" AS subtype,
    "Pathogen" AS pathogen,
    "Posted" AS posted,
    "Tests_3wma" AS tests_3wma,
    "Detections_5wma" AS detections_5wma,
    "Percent_Pos_3wma" AS percent_pos_3wma
FROM "cdc-rgnm-fkqb"
