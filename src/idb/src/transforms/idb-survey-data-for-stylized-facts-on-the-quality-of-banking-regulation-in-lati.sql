-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Question_Code" AS question_code,
    "Question" AS question,
    "Argentina" AS argentina,
    "The_Bahamas" AS the_bahamas,
    "Belize" AS belize,
    "Brazil" AS brazil,
    "Chile" AS chile,
    "Colombia" AS colombia,
    "Costa_Rica" AS costa_rica,
    "Dominican_Republic" AS dominican_republic,
    "Ecuador" AS ecuador,
    "Honduras" AS honduras,
    "Jamaica" AS jamaica,
    "Mexico" AS mexico,
    "Panama" AS panama,
    "Peru" AS peru,
    "Paraguay" AS paraguay,
    "El_Salvador" AS el_salvador,
    "Trinidad_and_Tobago" AS trinidad_and_tobago,
    "Uruguay" AS uruguay,
    "source_resource"
FROM "idb-survey-data-for-stylized-facts-on-the-quality-of-banking-regulation-in-lati"
