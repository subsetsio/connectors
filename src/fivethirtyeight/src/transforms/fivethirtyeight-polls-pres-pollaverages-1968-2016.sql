-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cycle",
    "state",
    "modeldate",
    "candidate_name",
    "candidate_id",
    "pct_estimate",
    "pct_trend_adjusted",
    "timestamp",
    "comment",
    "election_date",
    "election_qdate",
    "last_qdate",
    "last_enddate",
    "_medpoly2" AS medpoly2,
    "trend_medpoly2",
    "_shortpoly0" AS shortpoly0,
    "trend_shortpoly0",
    "sum_weight_medium",
    "sum_weight_short",
    "sum_influence",
    "sum_nat_influence",
    "_minpoints" AS minpoints,
    "_defaultbasetime" AS defaultbasetime,
    "_numloops" AS numloops,
    "_state_houseeffects_weight" AS state_houseeffects_weight,
    "_state_trendline_weight" AS state_trendline_weight,
    "_out_of_state_house_discount" AS out_of_state_house_discount,
    "_house_effects_multiplier" AS house_effects_multiplier,
    "_attenuate_endpoints" AS attenuate_endpoints,
    "_nonlinear_polynomial_degree" AS nonlinear_polynomial_degree,
    "_shortpoly_combpoly_weight" AS shortpoly_combpoly_weight,
    "_nat_shortpoly_combpoly_weight" AS nat_shortpoly_combpoly_weight
FROM "fivethirtyeight-polls-pres-pollaverages-1968-2016"
