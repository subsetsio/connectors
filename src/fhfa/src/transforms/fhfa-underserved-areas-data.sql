-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Underserved-area releases are annual geography snapshots; filter release_year before treating tract designations as current.
-- caution: The raw files drift between county and cnty columns across release years, so use both fields when constructing county-level geography keys.
SELECT
    "state",
    "cnty",
    "tract",
    CAST("msa2023" AS BIGINT) AS msa2023,
    CAST("lya" AS BIGINT) AS lya,
    CAST("pctmin" AS DOUBLE) AS pctmin,
    CAST("min_trct" AS BIGINT) AS min_trct,
    CAST("ceninc" AS BIGINT) AS ceninc,
    CAST("medinc" AS BIGINT) AS medinc,
    CAST("dda" AS BIGINT) AS dda,
    CAST("release_year" AS BIGINT) AS release_year,
    "source_file",
    "source_url",
    CAST("msa2018" AS BIGINT) AS msa2018,
    CAST("msa2013" AS BIGINT) AS msa2013,
    CAST("msa2003" AS BIGINT) AS msa2003,
    "county",
    CAST("ami" AS BIGINT) AS ami,
    "aian",
    CAST("served" AS BIGINT) AS served,
    "stusab",
    "cnty_nm"
FROM "fhfa-underserved-areas-data"
