-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "C0" AS c0,
    "FirstName" AS firstname,
    "SMITH" AS smith,
    "JOHNSON" AS johnson,
    "WILLIAMS" AS williams,
    "BROWN" AS brown,
    "JONES" AS jones,
    "GARCIA" AS garcia,
    "RODRIGUEZ" AS rodriguez,
    "MILLER" AS miller,
    "MARTINEZ" AS martinez,
    "DAVIS" AS davis,
    "HERNANDEZ" AS hernandez,
    "LOPEZ" AS lopez,
    "GONZALEZ" AS gonzalez,
    "WILSON" AS wilson,
    "ANDERSON" AS anderson,
    "THOMAS" AS thomas,
    "TAYLOR" AS taylor,
    "LEE" AS lee,
    "MOORE" AS moore,
    "JACKSON" AS jackson
FROM "fivethirtyeight-most-common-name-adjusted-name-combinations-matrix"
