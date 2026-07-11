-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country_code",
    "country_name_current",
    "official_name",
    "iso_alpha3",
    "iso_numeric3",
    "region",
    "subregion",
    "political_system",
    "population_in_thousands",
    "members_per_country",
    "inhabitants_per_parliament",
    "ppp_conversion_factor",
    "parliament_devoted_budget_perc",
    "ipu_membership",
    CAST("telephone_calling_code" AS BIGINT) AS telephone_calling_code
FROM "inter-parliamentary-union-countries"
