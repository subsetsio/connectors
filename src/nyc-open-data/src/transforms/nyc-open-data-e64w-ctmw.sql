-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "agency_code",
    "agency_name",
    "initiative_type",
    "initative_grouping_record",
    "record_id",
    "initiative_name",
    "initiative_description",
    "initiative_savings_type",
    "initiative_savings_group_name",
    "funding",
    "fiscal_year",
    "number_of_years_presented",
    "amount_year_1",
    "amount_year_2",
    "amount_year_3",
    "amount_year_4",
    "amount_year_5"
FROM "nyc-open-data-e64w-ctmw"
