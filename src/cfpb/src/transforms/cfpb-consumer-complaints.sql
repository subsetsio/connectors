-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each row is a complaint event; product, issue, company, geography, response, and submission channel are descriptive dimensions, not separate records.
-- caution: The raw extract contains repeated complaint_id values, so treat complaint_id as a source identifier, not a unique row key.
SELECT
    "date_received",
    "product",
    "sub_product",
    "issue",
    "sub_issue",
    "consumer_complaint_narrative",
    "company_public_response",
    "company",
    "state",
    "zip_code",
    "tags",
    "submitted_via",
    "date_sent_to_company",
    "company_response_to_consumer",
    "timely_response",
    "complaint_id"
FROM "cfpb-consumer-complaints"
