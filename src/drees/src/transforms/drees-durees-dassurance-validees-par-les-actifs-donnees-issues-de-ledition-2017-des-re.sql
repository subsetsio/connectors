-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "empty0",
    "empty1",
    "trimestres_cotises_en",
    "trimestres_d_avpf_en",
    "trimestres_de_maladie_maternite_invalidite_accidents_du_travail_en",
    "trimestres_de_chomage_formation_reconversion_preretraite_en",
    "trimestres_de_service_national_en",
    "autres_trimestres_trimestres_equivalents_rachats_trimestres_gratuits_pour_autres_motifs_en",
    "nombre_moyen_de_trimestres_valides_en_trimestres"
FROM "drees-durees-dassurance-validees-par-les-actifs-donnees-issues-de-ledition-2017-des-re"
