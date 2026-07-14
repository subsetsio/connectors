-- compiled by `hardened compile-transforms`, then curated at the model stage:
--   * `obs_time` dropped: the download node writes it as a verbatim copy of
--     whichever dimension PxWeb tags role=time -- here `time`.
SELECT
    "transaction account" AS transaction_account,
    "purpose account" AS purpose_account,
    "finance act" AS finance_act,
    "type of result" AS type_of_result,
    CAST("time" AS BIGINT) AS time,
    "obs_value"
FROM "statistics-greenland-ofxlanrn"
