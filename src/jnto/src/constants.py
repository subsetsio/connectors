"""Dataset-id selections for the jnto connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "1_1_Basic_Data_of_CountryRegion",
    "2_1_VisitorArrivals",
    "3_1_Visitor_arrivals",
    "3_2_Facts_on_trips_to_Japan",
    "3_3_Number_of_visitors_by_prefecture",
    "3_4_Travel_Consumption_Amount",
    "3_5_Foreigners_Entries",
    "3_6_Satisfaction_with_visit_to_japan",
    "4_1_Number_of_foreign_visitors",
    "4_2_Number_of_Outbound_Departures",
    "5_1_Japanese_Oversea_Travelers",
    "5_2_Number_of_Japanese_Visitors",
    "6_1_Status_of_International_Conferences_Held_by_Year",
    "6_2_Status_of_International_Conferences_Held_by_Month",
    "6_3_Status_of_International_Conferences_Held_by_Field",
    "6_4_Status_of_International_Conferences_Held_by_Scale",
    "6_5_Status_of_International_Conferences_Held_by_City",
]
