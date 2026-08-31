from pathlib import Path

from sqlalchemy import create_engine

from config import config, create_connection_string
from etl_excel import extract, transform, load, validate_load
from pipeline_utils import configure_logger, execute_sql


def pipeline(
    config_file="config/paths.ini",
    file_path="data/excel_table.xlsm",
    sheet_name="Gesamte Tabelle",
    usecols="A, C, D, E, F, G, H, I, J, K, L, M, N, O, P, R",
    schema="raw",
    table_name="applications",
):
    home = Path(config(config_file, "home")["path"])
    database_ini_path = home / "config" / "database.ini"
    log_file = home / "logs" / "pipeline.log"

    logger = configure_logger(log_file)
    logger.info("Pipeline started.")
    logger.info("Configuration home: %s", home)
    logger.info("Database config path: %s", database_ini_path)

    try:
        logger.info("Starting data extraction...")
        df = extract(
            config_file=config_file,
            file_path=file_path,
            sheet_name=sheet_name,
            usecols=usecols,
        )
        logger.info("Extraction complete. Rows extracted: %s", len(df))

        logger.info("Starting data transformation...")
        df_transformed = transform(df)
        logger.info("Transformation complete. Rows after transformation: %s", len(df_transformed))

        logger.info("Creating database engine...")
        engine = create_engine(
            create_connection_string(filename=database_ini_path, section="postgresql")
        )
        logger.info("Database engine created successfully.")

        logger.info("Loading data into database: %s.%s", schema, table_name)
        load(df_transformed, engine, schema=schema, table_name=table_name)
        logger.info("Data load complete.")

        logger.info("Validating data load...")
        row_count = validate_load(engine, schema, table_name)
        logger.info("Validation complete. %s rows present in %s.%s.", row_count, schema, table_name)

        logger.info("Executing staging SQL script...")
        execute_sql(engine, logger, home / "sql" / "staging.sql")

        logger.info("Executing core SQL script...")
        execute_sql(engine, logger, home / "sql" / "core.sql")

        logger.info("Pipeline execution complete.")

    except Exception:
        logger.exception("Pipeline failed.")
        raise


if __name__ == "__main__":
    pipeline()
