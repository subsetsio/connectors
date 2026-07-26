-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "event_name",
    "event_description",
    "event_url",
    "local_start_time",
    "local_end_time",
    "capacity",
    "status",
    "category_name",
    "subcategory_name",
    "format_name",
    "address_1",
    "address_2",
    "city",
    "region",
    "postal_code",
    "country",
    "venue_name",
    "ticket_name",
    "ticket_description",
    "ticket_on_sale_status",
    "ticket_quantity_total",
    "ticket_quantity_sold",
    "ticket_sales_start",
    "ticket_sales_end",
    "organizer_name",
    "organizer_description",
    "organizer_url"
FROM "nyc-open-data-de8q-estm"
