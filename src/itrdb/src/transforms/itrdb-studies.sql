-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Study records mix tree-ring measurements, chronologies, reconstructions, fire-history entries, and metadata-only links; filter by data_type and related descriptors before treating rows as a homogeneous study set.
SELECT
    "study_id",
    "xml_id",
    "uuid",
    "entry_id",
    "study_name",
    "study_code",
    "doi",
    "data_publisher",
    "data_type",
    "investigators",
    "version",
    "study_notes",
    "online_resource_link",
    "dif_metadata_link",
    "iso_metadata_link",
    "original_source",
    "data_type_information",
    "reconstruction",
    "contribution_date",
    "earliest_year_bp",
    "most_recent_year_bp",
    "earliest_year_ce",
    "most_recent_year_ce",
    "science_keywords_json",
    "funding_json",
    "publication_json",
    "reference_json",
    "data_license_description",
    "data_license_url"
FROM "itrdb-studies"
