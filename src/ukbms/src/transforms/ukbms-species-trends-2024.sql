-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is a species-level trend summary for the annual release rather than an annual observation series.
SELECT
    "COMMON_NAME" AS common_name,
    "SCI_NAME" AS sci_name,
    "NYEARS" AS nyears,
    "F_LIN_B" AS f_lin_b,
    "F_LIN_SE" AS f_lin_se,
    "F_LIN_P" AS f_lin_p,
    "F_TRENDDETAIL" AS f_trenddetail,
    "F_FULL_R" AS f_full_r,
    "T20_LIN_B" AS t20_lin_b,
    "T20_LIN_SE" AS t20_lin_se,
    "T20_LIN_P" AS t20_lin_p,
    "T20_TRENDDETAIL" AS t20_trenddetail,
    "T20_20_R" AS t20_20_r,
    "T10_LIN_B" AS t10_lin_b,
    "T10_LIN_SE" AS t10_lin_se,
    "T10_LIN_P" AS t10_lin_p,
    "T10_TRENDDETAIL" AS t10_trenddetail,
    "T10_10_R" AS t10_10_r
FROM "ukbms-species-trends-2024"
