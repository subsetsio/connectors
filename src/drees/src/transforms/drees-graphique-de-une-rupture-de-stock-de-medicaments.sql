-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "mois",
    "mois_en_chiffre",
    "presentations_en_rupture_de_stock",
    "presentations_a_risque_de_rupture_de_stock",
    "date"
FROM "drees-graphique-de-une-rupture-de-stock-de-medicaments"
