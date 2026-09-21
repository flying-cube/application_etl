# Job Application Data Pipeline

## Overview
Deliberately overengineered ETL architecture for small personal dataset to practice data ingestion, PostgresSQL transformations, data quality checks and Power BI reporting.

## Pipeline

1. Manual entries into Excel
2. Python script to process raw data into database, validate source structure
3. Clean and standardize in staging
4. Add simple analytics logicin mart
5. Refresh Power BI dashboard

## Dashboard

![dashboard_overview](images/dashboard_full.png)
![dashboard_filtered_country](images/dashboard_filter_country.png)
![dashboard_filtered_status](images/dashboard_filter_status.png)

KPIs:
- Applications sent
- Active applications
- Interviews & Interview rate

Visuals:
- Applications per week
- Current Pipeline
- Outcomes per country
- Active applications table
