-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Field of doctorate" AS field_of_doctorate,
    "1994 - Number" AS 1994_number,
    "1994 - Percent" AS 1994_percent,
    "1999 - Number" AS 1999_number,
    "1999 - Percent" AS 1999_percent,
    "2004 - Number" AS 2004_number,
    "2004 - Percent" AS 2004_percent,
    "2009 - Number" AS 2009_number,
    "2009 - Percent" AS 2009_percent,
    "2014 - Number" AS 2014_number,
    "2014 - Percent" AS 2014_percent,
    "2019 - Number" AS 2019_number,
    "2019 - Percent" AS 2019_percent,
    "2024 - Number" AS 2024_number,
    "2024 - Percent" AS 2024_percent
FROM "ncses-nsf25349-tab001-003"
