-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table carries multiple providence-compliance indicators and aggregation levels; filter the characteristic and aggregation columns before comparing values.
SELECT
    "dsc_agregacao",
    "dsc_caracteristica",
    "din_referencia",
    "num_nprc_concluidas",
    "num_nprp_programadas",
    "num_nprat_atrasadas",
    "num_npra_antecipadas",
    "num_nprcp_concluidas_prazo",
    "val_ecpa",
    "val_pcpa"
FROM "ons-brazil-ind-providencia-ecpa-pcpa"
