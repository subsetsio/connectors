-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "entity_id",
    "full_name",
    "name",
    "name_local",
    "name_other",
    "abbreviation",
    "entity_type",
    "legal_entity_type",
    CAST("publiclylisted" AS BOOLEAN) AS publiclylisted,
    "home_page",
    "registration_country",
    "registration_subdivision",
    "headquarters_country",
    "headquarters_subdivision",
    "gem_parents",
    "gem_parents_ids",
    "brazil_national_registry_of_legal_entities_federal_revenue_service",
    "global_legal_entity_identifier_index",
    "india_corporate_identification_number_ministry_of_corporate_affairs",
    "permid_refinitiv_permanent_identifier",
    "russia_uniform_state_register_of_legal_entities_of_russian_federation",
    "s_p_capital_iq",
    "uk_companies_house",
    "us_sec_central_index_key",
    "us_eia"
FROM "gem-global-energy-monitor-energy-ownership-tracker"
