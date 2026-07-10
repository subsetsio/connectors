SELECT
    CAST("alternative" AS VARCHAR) AS "alternative",
    CAST("book_title" AS VARCHAR) AS "book_title",
    CAST("comment" AS VARCHAR) AS "comment",
    CAST("created" AS VARCHAR) AS "created",
    CAST("editor" AS VARCHAR) AS "editor",
    CAST("id_dc" AS VARCHAR) AS "id_dc",
    CAST("isbn" AS VARCHAR) AS "isbn",
    CAST("journal_issue" AS VARCHAR) AS "journal_issue",
    CAST("journal_title" AS VARCHAR) AS "journal_title",
    CAST("publisher" AS VARCHAR) AS "publisher",
    CAST("reference" AS VARCHAR) AS "reference",
    CAST("source" AS VARCHAR) AS "source",
    CAST("title" AS VARCHAR) AS "title",
    CAST("url" AS VARCHAR) AS "url"
FROM "european-environment-agency-eunis.eunis-dc-index"
