-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per parcel-line of a mutation, NOT one row per transaction: a single sale (id_mutation) spans multiple rows when it covers several parcels, lots, or local types. valeur_fonciere is the total value of the whole mutation and is REPEATED on every row of that id_mutation - never SUM valeur_fonciere across rows without first deduplicating to one row per id_mutation, or you multiply the sale value by its parcel-line count.
-- caution: The file has no natural primary key and can contain exact duplicate rows; treat it as a keyless observation log and dedupe on id_mutation (or the full row) for transaction-level analysis.
-- caution: Coverage is statutorily incomplete: Alsace-Moselle (Bas-Rhin, Haut-Rhin, Moselle) and Mayotte are excluded from DVF by law, so code_departement will never contain 57/67/68/976.
SELECT
    "id_mutation",
    strptime("date_mutation", '%Y-%m-%d')::DATE AS date_mutation,
    "numero_disposition",
    "nature_mutation",
    "valeur_fonciere",
    "adresse_numero",
    "adresse_suffixe",
    "adresse_nom_voie",
    "adresse_code_voie",
    "code_postal",
    "code_commune",
    "nom_commune",
    "code_departement",
    "ancien_code_commune",
    "ancien_nom_commune",
    "id_parcelle",
    "ancien_id_parcelle",
    "numero_volume",
    "lot1_numero",
    "lot1_surface_carrez",
    "lot2_numero",
    "lot2_surface_carrez",
    "lot3_numero",
    "lot3_surface_carrez",
    "lot4_numero",
    "lot4_surface_carrez",
    "lot5_numero",
    "lot5_surface_carrez",
    "nombre_lots",
    "code_type_local",
    "type_local",
    "surface_reelle_bati",
    "nombre_pieces_principales",
    "code_nature_culture",
    "nature_culture",
    "code_nature_culture_speciale",
    "nature_culture_speciale",
    "surface_terrain",
    "longitude",
    "latitude"
FROM "dvf-transactions"
