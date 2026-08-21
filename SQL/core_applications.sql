DROP TABLE core.applications;

CREATE TABLE core.applications AS
SELECT
	application_id,
	is_active,
	status,
	"position",
	company,
	country,
	city,
	start_date,
	next_step_date,
	next_step,
	application_date,
	EXTRACT(WEEK FROM application_date) as application_week,
	CASE
		WHEN is_active THEN CURRENT_DATE - application_date
		ELSE NULL
	END as days_since_application
FROM staging.applications;

ALTER TABLE core.applications
ADD PRIMARY KEY (application_id);