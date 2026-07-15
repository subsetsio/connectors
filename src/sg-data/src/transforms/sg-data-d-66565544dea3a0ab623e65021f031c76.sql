-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MillionDollars_Ratio" AS milliondollars_ratio,
    "Importcontentfordomesticexports_Domesticexports" AS importcontentfordomesticexports_domesticexports,
    "Importcontentfordomesticexports_Importrequirementsfordomesticex" AS importcontentfordomesticexports_importrequirementsfordomesticex,
    "Importcontentfordomesticexports_Importrequirementsasaproportion" AS importcontentfordomesticexports_importrequirementsasaproportion
FROM "sg-data-d-66565544dea3a0ab623e65021f031c76"
