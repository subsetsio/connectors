-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("Year" AS BIGINT) AS year,
    CAST("Total FT" AS BIGINT) AS total_ft,
    CAST("Male FT" AS BIGINT) AS male_ft,
    CAST("Female FT" AS BIGINT) AS female_ft,
    CAST("Total PT" AS BIGINT) AS total_pt,
    CAST("Male PT" AS BIGINT) AS male_pt,
    CAST("Female PT" AS BIGINT) AS female_pt,
    CAST("Grand Total" AS BIGINT) AS grand_total,
    CAST("Tenure" AS BIGINT) AS tenure,
    CAST("On tenure track" AS BIGINT) AS on_tenure_track,
    CAST("total" AS BIGINT) AS total,
    "%" AS percent
FROM "instituto-de-estad-sticas-de-puerto-rico-facultad-conservatorio-de-musica11"
