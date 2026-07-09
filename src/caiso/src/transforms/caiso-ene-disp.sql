-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Exceptional-dispatch observations include price and energy measures by TAC area and instruction type; filter the measure and instruction dimensions before summing.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "TAC_AREA_NAME" AS tac_area_name,
    "DISP_TYPE" AS disp_type,
    "XML_DATA_ITEM" AS xml_data_item,
    "INSTRUCTION_TYPE" AS instruction_type,
    "MW" AS mw,
    "GROUP" AS group
FROM "caiso-ene-disp"
