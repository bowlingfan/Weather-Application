DECLARE @maxRecords INT;

SET @maxRecords = 30;

INSERT INTO weatherHistory (date, timestamp, snapshot_temperature)
VALUES (?,?,?)

IF @maxRecords < ( SELECT COUNT(*) FROM weatherHistory )
    DELETE FROM weatherHistory WHERE id = 30;
ELSE 
    null;