-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    CAST("LocationID" AS BIGINT) AS locationid,
    "LocationType" AS locationtype,
    "MainTopic" AS maintopic,
    "TopicID" AS topicid,
    "SubTopic" AS subtopic,
    "SubTopicID" AS subtopicid,
    "Qnum" AS qnum,
    "PEXCode" AS pexcode,
    "Qtype" AS qtype,
    "VarName" AS varname,
    "Keyword" AS keyword,
    "ShortNav" AS shortnav,
    "Question" AS question,
    "SummaryText" AS summarytext,
    "QuestionID" AS questionid,
    "SubQuestion" AS subquestion,
    "SubQuestionID" AS subquestionid,
    "Footnote" AS footnote,
    CAST("SampleSize" AS BIGINT) AS samplesize,
    CAST("LowConfidenceLimit" AS DOUBLE) AS lowconfidencelimit,
    CAST("HighConfidenceLimit" AS DOUBLE) AS highconfidencelimit,
    CAST("DataValue" AS DOUBLE) AS datavalue,
    "DataValueFootnoteSymbol" AS datavaluefootnotesymbol,
    "DataValueFootnote" AS datavaluefootnote,
    "GeoLocation" AS geolocation,
    "Census" AS census
FROM "cdc-yn8z-e2cm"
