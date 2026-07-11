-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Year" AS BIGINT) AS year,
    "ELB" AS elb,
    "Education and Library Board" AS education_and_library_board,
    CAST("comchange" AS BIGINT) AS comchange,
    "Components of population change" AS components_of_population_change,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-ppcopc01t04"
