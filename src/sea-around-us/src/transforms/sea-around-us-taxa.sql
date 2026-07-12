SELECT
    "taxon_key",
    "scientific_name",
    "common_name",
    "functional_group",
    "commercial_group",
    "is_taxon_distribution_backfilled"
FROM "sea-around-us-taxa"
WHERE "taxon_key" IS NOT NULL
