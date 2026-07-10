-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes aggregate origin groupings such as all states alongside individual countries; filter these out before country-level totals.
SELECT
    CAST("county_id" AS BIGINT) AS county_id,
    "country_code",
    "country_name",
    "country_ip5",
    "country_ue",
    "country_epo_member",
    "country_population"
FROM "epo-countries"
