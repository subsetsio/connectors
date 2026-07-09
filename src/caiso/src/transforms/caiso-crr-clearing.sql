-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: CRR clearing prices vary by market name, term, time of use, segment, and source/sink APNode; filter those dimensions before comparing prices.
SELECT
    "MARKET_NAME" AS market_name,
    "MARKET_TERM" AS market_term,
    "TIME_OF_USE" AS time_of_use,
    "START_DATE" AS start_date,
    "END_DATE" AS end_date,
    "START_DATE_GMT" AS start_date_gmt,
    "END_DATE_GMT" AS end_date_gmt,
    "APNODE_ID" AS apnode_id,
    "APNODE_ID_PRICE" AS apnode_id_price,
    "XML_DATA_ITEM" AS xml_data_item
FROM "caiso-crr-clearing"
