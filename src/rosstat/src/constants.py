"""Dataset-id selections for the rosstat connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "7708234640-IKT-twenty-twenty-five", "7708234640-IKT-twenty-twenty-four",
    "7708234640-IKT-twenty-twenty-three", "7708234640-IKT-twenty-twenty-two",
    "7708234640-codingtable", "7708234640-dispans2years-2021",
    "7708234640-dispanse-2021", "7708234640-employees2022",
    "7708234640-employees2024", "7708234640-employeesactivity2022",
    "7708234640-employeesactivity2023", "7708234640-employeesactivity2024",
    "7708234640-employeesactivity2025", "7708234640-employeessubject2022",
    "7708234640-employeessubject2023", "7708234640-employeessubject2024",
    "7708234640-employeessubject2025", "7708234640-healthRussia-2021",
    "7708234640-healthage-2021", "7708234640-healthregions-2021",
    "7708234640-indicatorsprograms2020", "7708234640-intsport-2021",
    "7708234640-nationalprojects", "7708234640-nosmoke-2021",
    "7708234640-numberofmunicipalities2021", "7708234640-okato",
    "7708234640-okei", "7708234640-okfs", "7708234640-okogu",
    "7708234640-okopf", "7708234640-oktmo", "7708234640-okvedva",
    "7708234640-orgsport-2021", "7708234640-placesforsports-2021",
    "7708234640-population", "7708234640-population2010",
    "7708234640-smokingnow-2021", "7708234640-sport-2021",
    "7708234640-unemploymentrate4", "7708234640-unemploymentrate6",
    "7708234640-urid", "7708234640-vegetablesfruits-2021",
    "7708234640-workingconditions2022", "7708234640-workingconditionsreg2022",
    "7708234640-zoh-2021", "7708234640-zohgood-2021",
]
