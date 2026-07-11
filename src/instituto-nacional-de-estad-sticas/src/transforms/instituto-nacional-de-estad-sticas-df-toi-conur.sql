-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "AREA_REF" AS area_ref,
    "FREQ" AS freq,
    "INDICADOR" AS indicador,
    "CONUR" AS conur,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "OBS_STATUS" AS obs_status,
    "NOTAS_INDICADOR" AS notas_indicador,
    "DECIMALS" AS decimals,
    "NOTAS" AS notas,
    "FUENTE" AS fuente,
    "UNIDAD" AS unidad,
    "MULT" AS mult
FROM "instituto-nacional-de-estad-sticas-df-toi-conur"
