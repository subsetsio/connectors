-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows span several levels of the pathology hierarchy (patho_niv1/2/3 via `top`) and of the spending-post hierarchy (`dep_niv_1` → `dep_niv_2`); summing `montant` across levels double-counts.
-- caution: `ntop` (patients with the pathology) repeats on every spending-post row of that pathology.
-- caution: National-level only: this table has no territory dimension.
SELECT
    "annee",
    "patho_niv1",
    "patho_niv2",
    "patho_niv3",
    "top",
    "dep_niv_1",
    "dep_niv_2",
    "montant",
    "ntop",
    "n_recourant_au_poste",
    "montant_moy",
    "niveau_prioritaire",
    "tri",
    "type_somme"
FROM "cnam-depenses"
