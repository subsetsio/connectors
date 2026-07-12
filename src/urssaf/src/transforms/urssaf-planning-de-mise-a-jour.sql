-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "thematique",
    "type_de_produit",
    "publication_associee",
    "datavisualisation_associee",
    "periodicite",
    "date_de_mise_a_jour",
    "precision",
    "nom_du_produit",
    "lien_vers_le_produit",
    "lien_vers_la_publication_associee",
    "lien_vers_la_datavisualisation_associee",
    "debut_date_de_mise_a_jour",
    "fin_date_de_mise_a_jour"
FROM "urssaf-planning-de-mise-a-jour"
