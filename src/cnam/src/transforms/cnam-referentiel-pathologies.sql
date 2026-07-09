-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows sit at three levels of the pathology hierarchy (`niveau_de_l_arborescence` = 1, 2 or 3); a level-1 row is the parent of the level-2/3 rows below it, so the table is a tree, not a flat list.
SELECT
    "patho_niv1",
    "patho_niv2",
    "patho_niv3",
    "top",
    "top_facet",
    "niveau_prioritaire",
    "niveau_de_l_arborescence",
    "tri",
    "patho_niv1_comorb",
    "patho_niv2_comorb",
    "patho_niv3_comorb",
    "texte_d_avertissement"
FROM "cnam-referentiel-pathologies"
