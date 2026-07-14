-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Total" AS total,
    "10335962.426199907" AS "10335962_426199907",
    "1630579.6604999949" AS "1630579_6604999949",
    "1808840.0394999948" AS "1808840_0394999948",
    "3403804.473200014" AS "3403804_473200014",
    "719106.8868999999" AS "719106_8868999999",
    "831421.4303000008" AS "831421_4303000008",
    "source_resource"
FROM "idb-urban-informal-economy-survey-ecinf-aggregated-data-for-brazil-2003"
