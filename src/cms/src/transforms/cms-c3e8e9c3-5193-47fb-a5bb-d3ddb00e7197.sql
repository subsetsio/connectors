-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("practice_id" AS BIGINT) AS practice_id,
    "state",
    "num_eps_vm",
    CAST("mssp" AS BIGINT) AS mssp,
    CAST("gpro" AS BIGINT) AS gpro,
    "elig_up_adjust",
    "category",
    "vm_payment_adj",
    "updated_vm",
    "cost_comp_tier_text",
    "qual_comp_tier_text",
    "zb_cost_cmpscr_pool_rnd",
    "zb_qual_cmpscr_pool_rnd"
FROM "cms-c3e8e9c3-5193-47fb-a5bb-d3ddb00e7197"
