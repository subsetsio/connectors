-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dataset_id",
    "federated",
    "title",
    "description",
    "theme",
    "keyword",
    "license",
    "language",
    "timezone",
    "modified",
    "data_processed",
    "metadata_processed",
    "publisher",
    "references",
    "attributions",
    "update_frequency"
FROM "qatar-planning-and-statistics-authority-dataset-of-datasets"
