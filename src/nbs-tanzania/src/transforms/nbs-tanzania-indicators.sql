SELECT
    indicator_id,
    area,
    description,
    type,
    frequency,
    is_reported,
    sources,
    providers,
    definition,
    method_of_computation
FROM "nbs-tanzania-indicators"
WHERE indicator_id IS NOT NULL
