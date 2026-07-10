-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bbref_ID" AS bbref_id,
    "yearID" AS yearid,
    "gameNum" AS gamenum,
    "gameID" AS gameid,
    "lgID" AS lgid,
    "startingPos" AS startingpos,
    "OFF600" AS off600,
    "DEF600" AS def600,
    "PITCH200" AS pitch200,
    "asg_PA" AS asg_pa,
    "asg_IP" AS asg_ip,
    "OFFper9innASG" AS offper9innasg,
    "DEFper9innASG" AS defper9innasg,
    "PITper9innASG" AS pitper9innasg,
    "TOTper9innASG" AS totper9innasg
FROM "fivethirtyeight-mlb-allstar-teams-allstar-player-talent"
