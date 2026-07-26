-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `value` column has different units by resource_type: ASN counts for asn rows, IPv4 address counts for ipv4 rows, and IPv6 prefix size/count semantics from the delegated-stats file for ipv6 rows.
SELECT
    "registry",
    "cc",
    "resource_type",
    "start",
    "value",
    strptime("date", '%Y%m%d')::DATE AS date,
    "status",
    "opaque_id"
FROM "apnic-delegated-resources"
