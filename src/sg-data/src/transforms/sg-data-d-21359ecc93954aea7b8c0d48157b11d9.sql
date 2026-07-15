-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "Course_Id" AS course_id,
    "Course_Title" AS course_title,
    "Event_URL" AS event_url,
    "Course_Organiser" AS course_organiser,
    "Start_Date" AS start_date,
    "End_Date" AS end_date,
    "Category" AS category,
    "Branch" AS branch,
    "PDU" AS pdu
FROM "sg-data-d-21359ecc93954aea7b8c0d48157b11d9"
