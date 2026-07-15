-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "school_name",
    "url_address",
    "address",
    "postal_code",
    "telephone_no",
    "telephone_no_2",
    "fax_no",
    "fax_no_2",
    "email_address",
    "mrt_desc",
    "bus_desc",
    "principal_name",
    "first_vp_name",
    "second_vp_name",
    "third_vp_name",
    "fourth_vp_name",
    "fifth_vp_name",
    "sixth_vp_name",
    "dgp_code",
    "zone_code",
    "type_code",
    "nature_code",
    "session_code",
    "mainlevel_code",
    "sap_ind",
    "autonomous_ind",
    "gifted_ind",
    "ip_ind",
    "mothertongue1_code",
    "mothertongue2_code",
    "mothertongue3_code"
FROM "sg-data-d-688b934f82c1059ed0a6993d2a829089"
