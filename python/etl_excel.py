import pandas as pd
from config import config

def extract(config_file="config/paths.ini", file_path="data/excel_table.xlsm", sheet_name="Gesamte Tabelle", usecols="A, C, D, E, F, G, H, I, J, K, L, M, N, O, P, R"):
    home = config(config_file, "home")["path"]
    file = f"{home}/{file_path}"

    ############
    ## EXTRACT
    ############

    # extract data from the Excel file
    df = pd.read_excel(file, sheet_name=sheet_name, usecols=usecols)
    
    return df

def transform(df):
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
    
    return df

def load(df, engine, schema="raw", table_name="applications"):
    ############
    ## LOAD
    ############

    # load dataframe into database using SQLAlchemy
    # replace entire table for now
    df.to_sql(table_name,
              con=engine,
              schema=schema,
              if_exists="replace",
              index=False)

def validate_load(engine, schema="raw", table_name="applications"):
    # verify that the data was loaded successfully by counting the number of rows in the table
    with engine.connect() as connection:
        row_count = connection.exec_driver_sql(
            f'SELECT COUNT(*) FROM "{schema}"."{table_name}"'
        ).scalar_one()
        return row_count
