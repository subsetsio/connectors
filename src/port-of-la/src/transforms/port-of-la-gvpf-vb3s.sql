-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "harbor",
    CAST("pp1" AS BIGINT) AS pp1,
    CAST("pp2" AS BIGINT) AS pp2,
    CAST("pp3" AS BIGINT) AS pp3,
    CAST("pp4" AS BIGINT) AS pp4,
    CAST("pp5" AS BIGINT) AS pp5,
    CAST("pp6" AS BIGINT) AS pp6,
    CAST("pp7" AS BIGINT) AS pp7,
    CAST("pp8" AS BIGINT) AS pp8,
    CAST("pp9" AS BIGINT) AS pp9,
    CAST("pp10" AS BIGINT) AS pp10,
    CAST("pp11" AS BIGINT) AS pp11,
    CAST("pp12" AS BIGINT) AS pp12,
    CAST("pp13" AS BIGINT) AS pp13,
    CAST("pp14" AS BIGINT) AS pp14,
    CAST("pp15" AS BIGINT) AS pp15,
    CAST("pp16" AS BIGINT) AS pp16,
    CAST("pp17" AS BIGINT) AS pp17,
    CAST("pp18" AS BIGINT) AS pp18,
    CAST("pp19" AS BIGINT) AS pp19,
    CAST("pp20" AS BIGINT) AS pp20,
    CAST("pp21" AS BIGINT) AS pp21,
    CAST("pp22" AS BIGINT) AS pp22,
    CAST("pp23" AS BIGINT) AS pp23,
    CAST("pp24" AS BIGINT) AS pp24,
    CAST("pp25" AS BIGINT) AS pp25,
    CAST("pp26" AS BIGINT) AS pp26,
    CAST("ytd_totals" AS BIGINT) AS ytd_totals,
    CAST("pp27" AS BIGINT) AS pp27
FROM "port-of-la-gvpf-vb3s"
