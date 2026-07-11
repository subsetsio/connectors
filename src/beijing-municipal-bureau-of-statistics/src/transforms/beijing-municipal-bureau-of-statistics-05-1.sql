-- Diagnostic transform for a source-catalog report that currently returns no observation data.
SELECT
    '1' AS "report_number",
    '0200' AS "subject",
    '05' AS "sort",
    'upstream_unavailable' AS "status",
    'Source catalog/viewer exists, but the verified REST data path returns no publishable observation rows.' AS "detail"
