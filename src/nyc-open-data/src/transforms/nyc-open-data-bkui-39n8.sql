-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "borough",
    "geographic_subset",
    "geographic_identifier",
    "total_referred",
    "total_ineligible",
    "total_referred_borough",
    "total_ineligible_borough",
    "total_referred_citywide",
    "total_ineligible_citywide"
FROM "nyc-open-data-bkui-39n8"
