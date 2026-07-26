-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "visits",
    "new_visitors",
    "google_social_media",
    "online_safety",
    "neigh_serv",
    "family_justice_center",
    "city_state_services",
    "learn_gbv",
    "signs_gbv",
    "helping_ohters"
FROM "nyc-open-data-q7bn-wnne"
