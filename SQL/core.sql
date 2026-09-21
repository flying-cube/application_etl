DROP TABLE core.applications;

CREATE TABLE core.applications AS
SELECT
	application_id,
	is_active,
	status,
	CASE
		WHEN status IN ('Waiting for response') THEN 'Waiting'
		WHEN status IN ('Interview', 'Waiting for next response') THEN 'Interview Process'
		WHEN status IN ('Rejected', 'Rejected after Interview') THEN 'Rejected'
		WHEN status IN ('No answer', 'Lost interest', 'Not available') THEN 'Closed'
		ELSE status
	END as short_status,
	CASE
		WHEN status IN ('Rejected', 'Rejected after Interview', 'Interview', 'No answer', 'Offer', 'Waiting for response', 'Waiting for next response')
		THEN TRUE
		ELSE FALSE
	END as was_sent,
	CASE
		WHEN status IN ('Rejected', 'Rejected after Interview', 'No answer')
		THEN TRUE
		ELSE FALSE
	END as is_rejected,
	CASE
		WHEN status IN ('Interview', 'Waiting for next response', 'Rejected after Interview')
		THEN TRUE
		ELSE FALSE
	END as is_interview,
	"position",
	company,
	country,
	city,
	start_date,
	next_step_date,
	next_step,
	application_date,
	CURRENT_DATE - application_date as days_since_application
FROM staging.applications;

ALTER TABLE core.applications
ADD PRIMARY KEY (application_id);