-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Year" AS BIGINT) AS year,
    CAST("Avg ASC-1 Nat Rate*" AS DOUBLE) AS avg_asc_1_nat_rate,
    CAST("Median ASC-1 Nat Rate*" AS DOUBLE) AS median_asc_1_nat_rate,
    CAST("Avg ASC-2 Nat Rate*" AS DOUBLE) AS avg_asc_2_nat_rate,
    CAST("Median ASC-2 Nat Rate*" AS DOUBLE) AS median_asc_2_nat_rate,
    CAST("Avg ASC-3 Nat Rate*" AS DOUBLE) AS avg_asc_3_nat_rate,
    CAST("Median ASC-3 Nat Rate*" AS DOUBLE) AS median_asc_3_nat_rate,
    CAST("Avg ASC-4 Nat Rate*" AS DOUBLE) AS avg_asc_4_nat_rate,
    CAST("Median ASC-4 Nat Rate*" AS DOUBLE) AS median_asc_4_nat_rate,
    CAST("Avg ASC-9 Nat Rate*" AS DOUBLE) AS avg_asc_9_nat_rate,
    CAST("Median ASC-9 Nat Rate*" AS DOUBLE) AS median_asc_9_nat_rate,
    CAST("Avg ASC-11 Nat Rate*" AS DOUBLE) AS avg_asc_11_nat_rate,
    CAST("Median ASC-11 Nat Rate*" AS DOUBLE) AS median_asc_11_nat_rate,
    CAST("ASC-12 Nat Rate" AS DOUBLE) AS asc_12_nat_rate,
    CAST("ASC-12 Better" AS BIGINT) AS asc_12_better,
    CAST("ASC-12 No Different" AS BIGINT) AS asc_12_no_different,
    CAST("ASC-12 Worse" AS BIGINT) AS asc_12_worse,
    CAST("ASC-12 Too Small" AS BIGINT) AS asc_12_too_small,
    CAST("Avg ASC-13 Nat Rate*" AS DOUBLE) AS avg_asc_13_nat_rate,
    CAST("Median ASC-13 Nat Rate*" AS DOUBLE) AS median_asc_13_nat_rate,
    CAST("Avg ASC-14 Nat Rate*" AS DOUBLE) AS avg_asc_14_nat_rate,
    CAST("Median ASC-14 Nat Rate*" AS DOUBLE) AS median_asc_14_nat_rate,
    CAST("ASC-17 Nat Rate" AS DOUBLE) AS asc_17_nat_rate,
    CAST("ASC-17 Better" AS BIGINT) AS asc_17_better,
    CAST("ASC-17 No Different" AS BIGINT) AS asc_17_no_different,
    CAST("ASC-17 Worse" AS BIGINT) AS asc_17_worse,
    CAST("ASC-17 Too Small" AS BIGINT) AS asc_17_too_small,
    CAST("ASC-18 Nat Rate" AS DOUBLE) AS asc_18_nat_rate,
    CAST("ASC-18 Better" AS BIGINT) AS asc_18_better,
    CAST("ASC-18 No Different" AS BIGINT) AS asc_18_no_different,
    CAST("ASC-18 Worse" AS BIGINT) AS asc_18_worse,
    CAST("ASC-18 Too Small" AS BIGINT) AS asc_18_too_small,
    CAST("ASC-19 Nat Rate" AS DOUBLE) AS asc_19_nat_rate,
    CAST("ASC-19 Better" AS BIGINT) AS asc_19_better,
    CAST("ASC-19 No Different" AS BIGINT) AS asc_19_no_different,
    CAST("ASC-19 Worse" AS BIGINT) AS asc_19_worse,
    CAST("ASC-19 Too Small" AS BIGINT) AS asc_19_too_small
FROM "cms-wue8-3vwe"
