-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "jurisdiction",
    "industry",
    "cartel_name",
    "dd_dim",
    "dd_id",
    "unit_measure",
    "sanction_type",
    "bid_rigging",
    "obs_status",
    "cartel_connor",
    "firm_number",
    "per_number",
    "case_number",
    "case_link",
    "authority",
    "start_date",
    "end_date",
    "cartel_duration",
    "discovery_date",
    "decision_date",
    "subsidiary_name",
    "parent_name",
    "parent_country",
    "currency",
    "amount_original",
    "exchange_rate",
    "value"
FROM "oecd-oecd.daf.comp:dsd-cartel-qdd@df-qdd-cartel"
