-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "GeneesmiddelengroepATC" AS geneesmiddelengroepatc,
    "Perioden" AS perioden,
    "PersonenMetVerstrekteGeneesmiddelen_1" AS personenmetverstrektegeneesmiddelen_1,
    "PersonenMetGeneesmiddelenRelatief_2" AS personenmetgeneesmiddelenrelatief_2,
    "GedefinieerdeDagdosesDDD_3" AS gedefinieerdedagdosesddd_3,
    "GedefinieerdeDagdosesDDDRelatief_4" AS gedefinieerdedagdosesdddrelatief_4,
    "Geslacht_label" AS geslacht_label,
    "Leeftijd_label" AS leeftijd_label,
    "GeneesmiddelengroepATC_label" AS geneesmiddelengroepatc_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81071ned"
