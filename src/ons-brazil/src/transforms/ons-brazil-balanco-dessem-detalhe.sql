-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: DESSEM detailed balances are semi-hourly programmed values by subsystem and energy source; filter the source/category columns before aggregating across generation components.
SELECT
    strptime("din_programacaodia", '%Y-%m-%d')::DATE AS din_programacaodia,
    "num_patamar",
    "cod_subsistema",
    CAST("val_demanda" AS DOUBLE) AS val_demanda,
    CAST("val_ger_hidraulica" AS DOUBLE) AS val_ger_hidraulica,
    CAST("val_ger_pch" AS DOUBLE) AS val_ger_pch,
    CAST("val_ger_termica" AS DOUBLE) AS val_ger_termica,
    CAST("val_ger_pct" AS DOUBLE) AS val_ger_pct,
    CAST("val_ger_eolica" AS DOUBLE) AS val_ger_eolica,
    CAST("val_ger_fotovoltaica" AS DOUBLE) AS val_ger_fotovoltaica,
    CAST("val_ger_mmgd" AS DOUBLE) AS val_ger_mmgd,
    CAST("val_cons_elevatoria" AS DOUBLE) AS val_cons_elevatoria
FROM "ons-brazil-balanco-dessem-detalhe"
