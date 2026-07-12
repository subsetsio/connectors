-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Countries can have multiple monitoring schemes, while countries without a scheme are represented by a placeholder row with scheme_index 0.
SELECT
    "country_code",
    "country",
    "scheme_index",
    "scheme_name",
    "map_status",
    "website",
    "organisation",
    "status",
    "start_year",
    "number_of_fieldworkers",
    "species_count",
    "habitats_record",
    "methods",
    "selection_of_plots",
    "sustainable_support",
    "reference",
    "contact",
    "note"
FROM "pecbms-monitoring-schemes"
