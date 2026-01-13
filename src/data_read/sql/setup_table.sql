CREATE TABLE IF NOT EXISTS weatherHistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    timestamp TEXT,
    snapshot_temperature SMALLINT,
)