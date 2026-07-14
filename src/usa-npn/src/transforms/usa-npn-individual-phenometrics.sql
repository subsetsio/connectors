-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are summarized phenometric events at the individual organism level and carry denormalized species, genus, and phenophase labels; do not aggregate together with site-level or raw status/intensity observations as if they share one grain.
SELECT
    "site_id",
    "latitude",
    "longitude",
    "elevation_in_meters",
    "state",
    "species_id",
    "class_id",
    "order_id",
    "family_id",
    "genus_id",
    "genus",
    "species",
    "common_name",
    "kingdom",
    "individual_id",
    "phenophase_id",
    "phenophase_description",
    "first_yes_year",
    "first_yes_month",
    "first_yes_day",
    "first_yes_doy",
    "first_yes_julian_date",
    "numdays_since_prior_no",
    "last_yes_year",
    "last_yes_month",
    "last_yes_day",
    "last_yes_doy",
    "last_yes_julian_date",
    "numdays_until_next_no"
FROM "usa-npn-individual-phenometrics"
