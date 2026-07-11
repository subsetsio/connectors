-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "col_0",
    CAST("Cons_D" AS BIGINT) AS cons_d,
    CAST("Cons_ND" AS BIGINT) AS cons_nd,
    CAST("Cons_S" AS BIGINT) AS cons_s,
    CAST("Cons" AS BIGINT) AS cons,
    CAST("I_ME" AS BIGINT) AS i_me,
    CAST("I_C" AS BIGINT) AS i_c,
    CAST("I_CI" AS BIGINT) AS i_ci,
    CAST("I" AS BIGINT) AS i,
    CAST("G" AS BIGINT) AS g,
    CAST("X_MS" AS BIGINT) AS x_ms,
    CAST("X_GV" AS BIGINT) AS x_gv,
    CAST("EX" AS BIGINT) AS ex,
    CAST("W" AS BIGINT) AS w,
    CAST("N" AS BIGINT) AS n,
    CAST("Q" AS BIGINT) AS q
FROM "instituto-de-estad-sticas-de-puerto-rico-matriz-insumo-producto-mip"
