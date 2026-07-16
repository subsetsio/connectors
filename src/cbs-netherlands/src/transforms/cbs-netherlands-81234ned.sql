-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BedrijfstakkenBranchesSBI2008" AS bedrijfstakkenbranchessbi2008,
    "Marges" AS marges,
    "Seizoencorrectie" AS seizoencorrectie,
    "Perioden" AS perioden,
    "Producentenvertrouwen_1" AS producentenvertrouwen_1,
    "VerwachteBedrijvigheid_2" AS verwachtebedrijvigheid_2,
    "OordeelOrderpositie_3" AS oordeelorderpositie_3,
    "OordeelVoorraden_4" AS oordeelvoorraden_4,
    "BedrijfstakkenBranchesSBI2008_label" AS bedrijfstakkenbranchessbi2008_label,
    "Marges_label" AS marges_label,
    "Seizoencorrectie_label" AS seizoencorrectie_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81234ned"
