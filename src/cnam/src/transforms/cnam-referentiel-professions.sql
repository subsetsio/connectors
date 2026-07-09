-- Published pass-through of raw asset `cnam-referentiel-professions`.
-- `tri` (unaccented sort name), `column_11` (empty) and `taux_depassement` (constant `non`) are dropped. The remaining `in_*` flags are the portal's display rules, kept here because this is the portal's own reference table.
SELECT
    "profession_sante" AS profession,
    "menu" AS portal_menu,
    "vision_generale_all" AS in_general_view,
    "vision_generale_prescriptions" AS in_prescriptions_view,
    "vision_profession_territoire" AS in_profession_territory_view,
    "vision_honoraires_actes_niveau_2" AS in_fees_acts_level_2_view,
    "vision_honoraires_remunerations_niveau_2" AS in_fees_payments_level_2_view,
    "vision_honoraires_actescliniques_niveau_3" AS in_fees_clinical_acts_level_3_view,
    "vision_honoraires_actestechniques_niveau_3" AS in_fees_technical_acts_level_3_view
FROM "cnam-referentiel-professions"
