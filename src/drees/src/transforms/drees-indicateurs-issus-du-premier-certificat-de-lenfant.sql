-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tableau",
    "url_de_consultation"
FROM "drees-indicateurs-issus-du-premier-certificat-de-lenfant"
