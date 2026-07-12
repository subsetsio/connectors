-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows describe dyad-issue-years, but the source contains duplicate issue classifications under the natural dyad/year/issue fields; do not assume one row per dyad-year issue.
SELECT
    "C0" AS c0,
    "dyad_id",
    "year",
    "conflict_id",
    "conflict",
    "location",
    "side_b_id",
    "side_b",
    "insurgent_subgroup",
    "umbrella",
    "splinter",
    "incompatibility",
    "active_year",
    "tier1",
    "tier2",
    "tier3",
    "tier4",
    "issue_text",
    "source",
    "dropped",
    "ethnicity_1",
    "ethnicity_2",
    "ethnicity_3",
    "ethnicity_4",
    "geography_1",
    "geography_2",
    "geography_3",
    "geography_4",
    "ideology_1",
    "ideology_2",
    "ideology_3",
    "ideology_4",
    "religion_1",
    "religion_2",
    "religion_3",
    "version"
FROM "ucdp-cid-dyadissueyear"
