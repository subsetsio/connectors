SELECT
    CAST("author" AS VARCHAR) AS "author",
    CAST("author_accepted" AS VARCHAR) AS "author_accepted",
    CAST("code_2000" AS VARCHAR) AS "code_2000",
    CAST("code2000_accepted" AS VARCHAR) AS "code2000_accepted",
    CAST("col_dataset" AS VARCHAR) AS "col_dataset",
    CAST("col_id" AS VARCHAR) AS "col_id",
    CAST("id_eunis" AS VARCHAR) AS "id_eunis",
    CAST("id_eunis_accepted" AS VARCHAR) AS "id_eunis_accepted",
    CAST("is_accepted_name" AS VARCHAR) AS "is_accepted_name",
    CAST("scientific_name" AS VARCHAR) AS "scientific_name",
    CAST("scientific_name_accepted" AS VARCHAR) AS "scientific_name_accepted",
    CAST("species_group_name" AS VARCHAR) AS "species_group_name",
    CAST("status_name" AS VARCHAR) AS "status_name",
    CAST("taxonomy_level_name" AS VARCHAR) AS "taxonomy_level_name",
    CAST("taxonomy_tree" AS VARCHAR) AS "taxonomy_tree"
FROM "european-environment-agency-eunis.species-information"
