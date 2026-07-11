-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "SEMS EPA ID" AS sems_epa_id,
    "Facility Information" AS facility_information,
    "SITE NAME" AS site_name,
    "ADDRESS" AS address,
    "COUNTY" AS county,
    "FEDERAL FACILITY" AS federal_facility,
    "NPL STATUS" AS npl_status,
    "NON-NPL STATUS" AS non_npl_status,
    "LATITUDE/LONGITUDE" AS latitude_longitude
FROM "instituto-de-estad-sticas-de-puerto-rico-sems"
