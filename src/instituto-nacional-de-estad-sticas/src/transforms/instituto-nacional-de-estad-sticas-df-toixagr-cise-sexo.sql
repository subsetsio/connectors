-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "DATAFLOW" AS dataflow,
    "INDICADOR" AS indicador,
    "FREQ" AS freq,
    "AREA_REF" AS area_ref,
    "CISE" AS cise,
    "SEXO" AS sexo,
    "TIME_PERIOD" AS time_period,
    "OBS_VALUE" AS obs_value,
    "DECIMALS" AS decimals,
    "NOTAS_INDICADOR" AS notas_indicador,
    "OBS_STATUS" AS obs_status,
    "MULT" AS mult,
    "UNIDAD" AS unidad,
    "FUENTE" AS fuente,
    "NOTAS" AS notas
FROM "instituto-nacional-de-estad-sticas-df-toixagr-cise-sexo"
