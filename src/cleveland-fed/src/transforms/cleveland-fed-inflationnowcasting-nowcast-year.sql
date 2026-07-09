SELECT
    "label" AS update_label,
    series,
    percent_change
FROM (
    UNPIVOT "cleveland-fed-inflationnowcasting-nowcast-year"
    ON COLUMNS(* EXCLUDE ("label"))
    INTO NAME series VALUE percent_change
)
