-- Stream with Power ON/OFF events from iVAC Tool Plus
CREATE STREAM ivac_power_events WITH (KAFKA_TOPIC='power_events', PARTITIONS=1) AS
SELECT
  'A1ToolPlus' AS key,
  asset_uuid,
  value,
  ROWTIME AS ts
FROM ASSETS_STREAM
WHERE asset_uuid = 'VIRTUAL-IVAC-TOOL-PLUS' AND id = 'A1ToolPlus'
EMIT CHANGES;

-- Table with latest state
CREATE TABLE latest_ivac_power_state AS
SELECT
  key,
  LATEST_BY_OFFSET(value) AS last_value,
  LATEST_BY_OFFSET(ts) AS last_ts
FROM ivac_power_events
GROUP BY key;

-- Stream with ON/OFF events and their duration
CREATE STREAM ivac_power_durations AS
SELECT
  ivac_event.key,
  s.last_value AS state_just_ended,
  (ivac_event.ts - s.last_ts) / 1000 AS duration_sec
FROM ivac_power_events ivac_event
JOIN latest_ivac_power_state s
  ON ivac_event.key = s.key
WHERE ivac_event.value != s.last_value  -- only when the state changes
EMIT CHANGES;

-- Table with total ON/OFF tool per tool monitored by the iVAC Power Tool
CREATE TABLE ivac_power_state_totals AS
SELECT
  ivac_event_key + '_' + state_just_ended AS ivac_power_key,  -- key
  SUM(duration_sec) AS total_duration_sec
FROM ivac_power_durations
GROUP BY ivac_event_key + '_' + state_just_ended
EMIT CHANGES;
