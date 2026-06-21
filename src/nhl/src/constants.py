"""Dataset-id selections for the nhl connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "franchise",
    "goalie-advanced",
    "goalie-bios",
    "goalie-daysrest",
    "goalie-penaltyshots",
    "goalie-savesbystrength",
    "goalie-shootout",
    "goalie-startedvsrelieved",
    "goalie-summary",
    "season",
    "skater-bios",
    "skater-faceoffpercentages",
    "skater-faceoffwins",
    "skater-goalsforagainst",
    "skater-penalties",
    "skater-penaltykill",
    "skater-penaltyshots",
    "skater-percentages",
    "skater-powerplay",
    "skater-puckpossessions",
    "skater-realtime",
    "skater-scoringpergame",
    "skater-scoringrates",
    "skater-shootout",
    "skater-shottype",
    "skater-summary",
    "skater-summaryshooting",
    "skater-timeonice",
    "team",
    "team-daysbetweengames",
    "team-faceoffpercentages",
    "team-faceoffwins",
    "team-goalgames",
    "team-goalsagainstbystrength",
    "team-goalsagainstbystrengthgoaliepull",
    "team-goalsbyperiod",
    "team-goalsforbystrength",
    "team-goalsforbystrengthgoaliepull",
    "team-leadingtrailing",
    "team-outshootoutshotby",
    "team-penalties",
    "team-penaltykill",
    "team-penaltykilltime",
    "team-percentages",
    "team-powerplay",
    "team-powerplaytime",
    "team-realtime",
    "team-savepercentage",
    "team-scoretrailfirst",
    "team-shootout",
    "team-shottype",
    "team-summary",
    "team-summaryshooting",
]
