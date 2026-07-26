-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "client_id",
    "lobbyist_id",
    "lobbyist_name",
    "lobbyist_po",
    "report_year",
    "client_name",
    "client_po",
    "lobbyist_employees",
    "lobbyist_activities",
    "lobbyist_targets",
    "lobbyist_is_colobbyist",
    "client_industry",
    "lobbyist_has_finacial_interest",
    "num_periods",
    "start_date",
    "end_date",
    "periodic_id",
    "registration_id",
    "period",
    "periodic_year",
    "compensation_total",
    "lobbying_expenses_total",
    "small_expense_total",
    "itemized_expense_total",
    "salary_expense_total",
    "reimbursed_expenses_total",
    "periodic_activities",
    "periodic_targets"
FROM "nyc-open-data-fmf3-knd8"
