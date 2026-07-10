-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "name",
    "position_in_organisation",
    "organisation",
    "address",
    "town",
    "county",
    "postcode",
    "country",
    "year_of_award",
    "type_of_award_lifetime_l_standard_s_or_honorary_h",
    "citation",
    "qa_ref",
    "region",
    "notes"
FROM "dbt-kings-award-for-enterprise-recipients--kae--individuals"
