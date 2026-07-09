-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: RTPD LMP rows are limited to the benchmark nodes selected by the connector, not the full CAISO node universe.
SELECT
    "INTERVALSTARTTIME_GMT" AS intervalstarttime_gmt,
    "INTERVALENDTIME_GMT" AS intervalendtime_gmt,
    "OPR_DT" AS opr_dt,
    "OPR_HR" AS opr_hr,
    "NODE_ID_XML" AS node_id_xml,
    "NODE_ID" AS node_id,
    "NODE" AS node,
    "MARKET_RUN_ID" AS market_run_id,
    "LMP_TYPE" AS lmp_type,
    "XML_DATA_ITEM" AS xml_data_item,
    "PNODE_RESMRID" AS pnode_resmrid,
    "GRP_TYPE" AS grp_type,
    "POS" AS pos,
    "PRC" AS prc,
    "OPR_INTERVAL" AS opr_interval,
    "GROUP" AS group
FROM "caiso-prc-rtpd-lmp"
