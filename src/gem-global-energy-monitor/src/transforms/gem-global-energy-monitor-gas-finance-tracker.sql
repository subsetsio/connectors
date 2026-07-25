-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Gas finance rows represent project-financier records but no stable unique transaction key was verified; aggregate only after choosing the appropriate finance dimensions.
SELECT
    "country",
    "gem_terminal_id",
    "gem_combo_id",
    "project_name",
    "alternate_project_name_s",
    "local_language_name_s",
    "train_unit_name",
    "terminal_type",
    "status",
    "capacity_mtpa",
    "expected_start_year",
    "project_cost_us_million",
    "fid_status",
    "fid_date",
    "owner",
    "parent_company",
    "financier",
    "type_of_financier",
    "public_private",
    "financier_hq_country",
    "all_known_project_finance_this_terminal_us_million",
    "this_financier_s_total_share_us_million",
    "finance_type",
    "finance_status",
    "close_year",
    "loan_arranger_financial_advisor",
    "epc_contractor",
    "gem_wiki_link"
FROM "gem-global-energy-monitor-gas-finance-tracker"
