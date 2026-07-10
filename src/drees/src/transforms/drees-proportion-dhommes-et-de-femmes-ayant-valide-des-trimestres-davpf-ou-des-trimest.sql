-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "generation_en",
    "trimestre_s_d_avpf_utiles",
    "trimestre_s_de_chomage_de_formation_de_preretraite_et_de_conversion_utiles",
    "trimestre_s_de_maladie_de_maternite_d_invalidite_et_d_accident_du_travail_utiles",
    "trimestres_d_avpf_de_chomage_de_formation_de_reconversion_de_preretraite_de_maladie_de_maternite_d_i",
    "genre"
FROM "drees-proportion-dhommes-et-de-femmes-ayant-valide-des-trimestres-davpf-ou-des-trimest"
