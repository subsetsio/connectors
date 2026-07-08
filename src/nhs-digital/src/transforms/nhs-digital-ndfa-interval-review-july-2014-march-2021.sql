SELECT
    source_file,
    row_index,
    "column",
    value
FROM "nhs-digital-ndfa-interval-review-july-2014-march-2021"
WHERE value IS NOT NULL
