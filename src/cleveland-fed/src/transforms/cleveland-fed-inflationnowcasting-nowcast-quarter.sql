SELECT
    "label" AS update_label,
    series,
    percent_change
FROM (
    UNPIVOT "cleveland-fed-inflationnowcasting-nowcast-quarter"
    ON COLUMNS(* EXCLUDE ("label"))
    INTO NAME series VALUE percent_change
)
