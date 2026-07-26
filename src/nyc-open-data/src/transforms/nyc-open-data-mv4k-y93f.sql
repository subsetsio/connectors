-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "summons_key",
    "summons_date",
    "offense_description",
    "law_section_number",
    "law_description",
    "summons_category_type",
    "age_group",
    "sex",
    "race",
    "jurisdiction_code",
    "boro",
    "precinct_of_occur",
    "x_coordinate_cd",
    "y_coordinate_cd",
    "latitude",
    "longitude",
    "new_georeferenced_column"
FROM "nyc-open-data-mv4k-y93f"
