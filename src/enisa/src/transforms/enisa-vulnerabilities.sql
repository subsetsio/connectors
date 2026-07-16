-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Raw crawl fragments can overlap when continuation runs resume; downstream consumers should use the published transform, which deduplicates the corpus on EUVD `id`.
-- caution: The `aliases` and `references` fields are newline-joined lists; use `enisa-cve-mapping` when a normalized EUVD-to-CVE crosswalk is needed.
-- row reshape: ROW_NUMBER keeps the newest copy of each EUVD id; unnest-equivalent cardinality change is intentional.
WITH ranked AS (
    SELECT
        "id",
        "enisa_uuid",
        "description",
        "date_published",
        "date_updated",
        "base_score",
        CAST("base_score_version" AS DOUBLE) AS base_score_version,
        "base_score_vector",
        "epss",
        "assigner",
        "aliases",
        "references",
        ROW_NUMBER() OVER (
            PARTITION BY "id"
            ORDER BY "date_updated" DESC NULLS LAST, "date_published" DESC NULLS LAST
        ) AS rn
    FROM "enisa-vulnerabilities"
)
SELECT
    "id",
    "enisa_uuid",
    "description",
    "date_published",
    "date_updated",
    "base_score",
    base_score_version,
    "base_score_vector",
    "epss",
    "assigner",
    "aliases",
    "references"
FROM ranked
WHERE rn = 1
