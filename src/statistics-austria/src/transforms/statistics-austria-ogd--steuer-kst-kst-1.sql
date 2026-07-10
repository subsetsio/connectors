-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "fallart",
    "stufen_des_zu_versteuernden_einkommens",
    "bundesland_politischer_bezirk_teilw_abo_ebene_1",
    "fallzahl_veranlagungsf_lle_insgesamt",
    "fallzahl_gesamtbetrag_der_eink_nfte",
    "gesamtbetrag_der_eink_nfte_eur",
    "fallzahl_verlustabzug",
    "verlustabzug_eur",
    "fallzahl_verluste_ausl_nd_gruppenmitglieder_abz_gl_nachzuversteuernde_verluste",
    "verluste_ausl_nd_gruppenmitglieder_abz_gl_nachzuversteuernde_verluste_eur",
    "fallzahl_zu_versteuerndes_einkommen",
    "zu_versteuerndes_einkommen_eur",
    "fallzahl_anrechenbare_mindestk_rperschaftsteuer",
    "anrechenbare_mindestk_rperschaftsteuer_eur",
    "fallzahl_k_rperschaftsteuer",
    "k_rperschaftsteuer_eur",
    "fallzahl_anrechenbare_inl_ndische_kest",
    "anrechenbare_inl_ndische_kest_eur",
    "fallzahl_ausl_ndische_steuer",
    "ausl_ndische_steuer_eur",
    "fallzahl_spruchbetrag_abgabennachforderung_oder_gutschrift",
    "spruchbetrag_abgabennachforderung_oder_gutschrift_eur"
FROM "statistics-austria-ogd--steuer-kst-kst-1"
