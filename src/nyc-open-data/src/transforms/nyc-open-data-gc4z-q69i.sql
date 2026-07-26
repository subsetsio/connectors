-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "updated",
    "media_outlet_name",
    "type_of_media",
    "languages_served",
    "geographic_focus",
    "community_served_general",
    "community_served_specific",
    "outlet_website",
    "outlet_email",
    "outlet_phone"
FROM "nyc-open-data-gc4z-q69i"
