-- Drop the final totals table
DROP TABLE ivac_power_state_totals DELETE TOPIC;

-- Drop the durations stream
DROP STREAM ivac_power_durations DELETE TOPIC;

-- Drop the latest state table
DROP TABLE latest_ivac_power_state DELETE TOPIC;

-- Drop the power events stream
DROP STREAM ivac_power_events DELETE TOPIC;
