SELECT
    "label" AS update_label,
    series,
    percent_change
FROM (
    UNPIVOT "cleveland-fed-inflationnowcasting-nowcast-month"
    ON COLUMNS(* EXCLUDE ("label"))
    INTO NAME series VALUE percent_change
)
