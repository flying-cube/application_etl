DROP TABLE staging.applications;

CREATE TABLE staging.applications AS
SELECT
	"Index"::INT AS application_id,
	CASE
		WHEN UPPER(TRIM("Aktiv")) IN ('JA', 'YES', 'Y', 'TRUE', '1') THEN TRUE
		WHEN UPPER(TRIM("Aktiv")) IN ('NEIN', 'NO', 'N', 'FALSE', '0') THEN FALSE
		ELSE NULL
	END as is_active,
	CASE
		WHEN "Status" = 'Neu' THEN 'NEW'
		WHEN "Status" = 'Abgelehnt' THEN 'Rejected'
		WHEN "Status" = 'Abgelehnt nach Interview' THEN 'Rejected after Interview'
		WHEN "Status" = 'Interview' THEN 'Interview'
		WHEN "Status" = 'Keine Antwort' THEN 'No answer'
		WHEN "Status" = 'Angebot' THEN 'Offer'
		WHEN "Status" = 'Kein Interesse mehr' THEN 'Lost interest'
		WHEN "Status" = 'Nicht mehr verfügbar' THEN 'Not available'
		WHEN "Status" = 'Warte auf Antwort' THEN 'Waiting for response'
		WHEN "Status" = 'Warte auf weitere Antwort' THEN 'Waiting for next response'
		ELSE "Status"
	END as status,
	"Position"::VARCHAR as "position",
	"Firma"::VARCHAR as company,
	CASE
		WHEN UPPER(TRIM("Land")) IN ('DE', 'D', 'DEUTSCHLAND', 'GER', 'GERMANY') THEN 'DE'
		WHEN UPPER(TRIM("Land")) IN ('CH', 'SCHWEIZ', 'SWITZERLAND') THEN 'CH'
		WHEN UPPER(TRIM("Land")) IN ('AT', 'ÖSTERREICH', 'AUSTRIA') THEN 'AT'
		ELSE NULL	
	END as country,
	"Stadt"::VARCHAR as city,
	"Start Datum"::date as start_date,
	"Nächster Schritt"::date as next_step_date,
	"Nächster Schritt Bemerkung"::VARCHAR as next_step,
	"Abgeschickt"::date as application_date
FROM raw.applications;