-- imf-sdg: IMF endpoint returns degenerate/empty observations for this
-- dataflow (no dimensions, no numeric values). Publishes nothing; waived.
SELECT "dataflow" AS stub, CAST(NULL AS DOUBLE) AS "OBS_VALUE"
FROM "imf-sdg"
WHERE FALSE
