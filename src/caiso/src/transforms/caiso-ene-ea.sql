-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Expected-energy accounting contains multiple energy types in the same table; filter energy type before summing MWh.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "OPR_INTERVAL" AS opr_interval,
    "ENERGY_TYPE" AS energy_type,
    "XML_DATA_ITEM" AS xml_data_item,
    "POS" AS pos,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-ene-ea"
