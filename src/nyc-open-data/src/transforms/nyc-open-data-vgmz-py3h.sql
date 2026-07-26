-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "geographic_district",
    "city_council_district",
    "bldg_code",
    "break_concat",
    "cc_district",
    "org_id",
    "org_name",
    "meal",
    "number_of_periods"
FROM "nyc-open-data-vgmz-py3h"
