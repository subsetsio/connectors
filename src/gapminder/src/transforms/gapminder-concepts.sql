SELECT
    concept,
    concept_type,
    name,
    name_short,
    description,
    unit,
    tags,
    scales,
    domain,
    source_url,
    repo
FROM "gapminder-concepts"
WHERE concept IS NOT NULL
