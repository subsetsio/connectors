-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record",
    "intake_date",
    "fiscal_month",
    "fy",
    "vrc_location",
    "affiliation",
    "postal_city",
    "state",
    "zip_code",
    "country",
    "borough",
    "branch",
    "discharge_status",
    "issuereason",
    "inquiry_source",
    "engagement_level",
    "close_date",
    "referral_made_to",
    "vetconnectnyc_yn",
    "post_engagement_date",
    "post_engagement_method",
    "council_district"
FROM "nyc-open-data-jup5-7fik"
