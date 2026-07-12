-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "code_ctp",
    "libelle_long",
    "format",
    "date_d_effet_de_la_completude",
    "code_de_base_assujettie_di_s21_g00_78_001",
    "type_de_composant_de_base_assujettie_di_s21_g00_79_001",
    "code_de_cotisation_individuelle_di_s21_g00_81_001",
    "identification_ops_di_s21_g00_81_002",
    "montant_d_assiette_di_s21_g00_81_003",
    "montant_de_cotisation_di_s21_g00_81_004",
    "code_insee_commune_di_s21_g00_81_005",
    "taux_de_cotisation_di_s21_g00_81_007",
    "valeur_cotetab_s21_g00_82_001",
    "code_de_cotisation_cotetab_s21_g00_82_002",
    "date_de_debut_de_rattachement_cotetab_s21_g00_82_003",
    "date_de_fin_de_rattachement_cotetab_s21_g00_82_004",
    "reference_reglementaire_ou_contactuelle_cotetab_s21_g00_82_005",
    "code_de_cotisation_da_s21_g00_23_001",
    CAST("qualifiant_d_assiette_da_s21_g00_23_002" AS BIGINT) AS qualifiant_d_assiette_da_s21_g00_23_002,
    "taux_de_cotisation_da_s21_g00_23_003",
    "montant_d_assiette_da_s21_g00_23_004",
    "montant_de_cotisation_da_s21_g00_23_005",
    "code_insee_commune_da_s21_g00_23_006",
    "precisions_complementaires",
    CAST("version_du_tableau" AS DOUBLE) AS version_du_tableau
FROM "urssaf-equivalence-dida"
