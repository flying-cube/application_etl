import pandas as pd
from sqlalchemy import create_engine
from config import config, create_connection_string


def main():
    home = config("config/paths.ini", "home")["path"]
    file = f"{home}/data/excel_table.xlsm"
    config_file = f"{home}/database.ini"

    postgresql_schema = "raw"
    postgresql_table_name = "applications"

    ############
    ## EXTRACT
    ############

    # extract data from the Excel file
    df = pd.read_excel(file, sheet_name="Gesamte Tabelle", usecols="A, C, D, E, F, G, H, I, J, K, L, M, N, O, P, R")

    ############
    ## TRANSFORM
    ############

    # for datetime columns, convert to date format and fill NaN values with None
    # for string columns, fill NaN values with empty string
    for col in df.columns:
        if df[col].dtype == "datetime64[us]":
            df[col] = (pd.to_datetime(df[col]).dt.date).fillna(value=None)
        elif df[col].dtype == "string":
            df[col] = df[col].fillna(value="")


    ############
    ## LOAD
    ############

    # establish connection to the database
    conn_string = create_connection_string(config_file, "postgresql")
    engine = create_engine(conn_string, echo=False)

    # load dataframe into database using SQLAlchemy
    # replace entire table for now
    df.to_sql(postgresql_table_name,
              con=engine,
              schema=postgresql_schema,
              if_exists="replace",
              index=False)

    # verify that the data was loaded successfully by counting the number of rows in the table
    with engine.connect() as connection:
        row_count = connection.exec_driver_sql(
            f'SELECT COUNT(*) FROM "{postgresql_schema}"."{postgresql_table_name}"'
        ).scalar_one()
    print(f"Wrote {row_count} rows to {postgresql_schema}.{postgresql_table_name}")

if __name__ == "__main__":
    main()