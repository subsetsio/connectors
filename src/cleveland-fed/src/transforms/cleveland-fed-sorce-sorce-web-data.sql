-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per SORCE collection date; the survey covers firms in the Fourth Federal Reserve District (Ohio and parts of Pennsylvania, West Virginia and Kentucky), not the US as a whole.
-- caution: Every column is a diffusion index (share reporting an increase minus share reporting a decrease, roughly -100 to 100), so values are not levels and must not be summed.
-- caution: The `manu_`, `oth_` and `total_` prefixes are industry cuts of the same question: `total_` is the all-firms index, NOT the sum of the manufacturing and other-industry indexes.
-- caution: Questions were added to the survey over time, so early collection dates have no observation for the later question blocks.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "manu_cap_ex_di",
    "oth_cap_ex_di",
    "total_cap_ex_di",
    "manu_conditions_di",
    "oth_conditions_di",
    "total_conditions_di",
    "manu_employment_di",
    "oth_employment_di",
    "total_employment_di",
    "manu_expect_cond_di",
    "oth_expect_cond_di",
    "total_expect_cond_di",
    "manu_expect_costs_di",
    "oth_expect_costs_di",
    "total_expect_costs_di",
    "manu_expect_employment_di",
    "oth_expect_employment_di",
    "total_expect_employment_di",
    "manu_nonlabor_costs_di",
    "oth_nonlabor_costs_di",
    "total_nonlabor_costs_di",
    "manu_prices_di",
    "oth_prices_di",
    "total_prices_di",
    "manu_wages_di",
    "oth_wages_di",
    "total_wages_di"
FROM "cleveland-fed-sorce-sorce-web-data"
