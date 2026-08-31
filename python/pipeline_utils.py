import logging
from pathlib import Path


def configure_logger(log_file: Path) -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("applications_pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def execute_sql(engine, logger: logging.Logger, path: Path) -> None:
    logger.info("Executing SQL script: %s", path)

    try:
        sql = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.exception("SQL script not found: %s", path)
        raise
    except OSError:
        logger.exception("Unable to read SQL script: %s", path)
        raise

    try:
        with engine.raw_connection() as raw_conn:
            with raw_conn.cursor() as cur:
                cur.execute(sql)
            raw_conn.commit()
        logger.info("SQL script completed successfully: %s", path.name)
    except Exception:
        logger.exception("Failed to execute SQL script: %s", path)
        raise
