-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a current snapshot, not a historical time series; compare refreshes through run lineage rather than treating rows as dated observations.
-- caution: An Autonomous System can appear under more than one economy code in the APNIC Labs population estimate, so use `asn` with `cc` when identifying rows.
SELECT
    "rank",
    "asn",
    "description",
    "cc",
    "users",
    "pct_cc_pop",
    "pct_internet",
    "samples"
FROM "apnic-as-user-population"
