-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "docket_number",
    CAST("usdot_number" AS BIGINT) AS usdot_number,
    "rfc_number",
    "op_auth_type",
    "op_auth_status",
    CAST("min_cov_amount" AS DOUBLE) AS min_cov_amount,
    "cargo_req",
    "bond_req",
    CAST("bipd_file" AS DOUBLE) AS bipd_file,
    "cargo_file",
    "bond_file",
    "bus_undeliverable_mail",
    "mail_undeliverable_mail",
    "dba_name",
    "legal_name",
    "bus_street_po",
    "bus_colonia",
    "bus_city",
    "bus_state_code",
    "bus_ctry_code",
    "bus_zip_code",
    "bus_telno",
    "mail_street_po",
    "mail_colonia",
    "mail_city",
    "mail_state_code",
    "mail_ctry_code",
    "mail_zip_code"
FROM "u-s-department-of-transportation-nakq-58th"
