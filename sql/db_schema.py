from sqlalchemy import create_engine, inspect, text

engine = create_engine(
    "mssql+pyodbc://@localhost/Northwind?"
    "driver=ODBC+Driver+18+for+SQL+Server&"
    "trusted_connection=yes&"
    "TrustServerCertificate=yes"
)


def get_schema():
    inspector = inspect(engine)

    schema = ""

    for table in inspector.get_table_names():
        schema += f"\nTABLE: {table}\n"

        for column in inspector.get_columns(table):
            schema += f"  - {column['name']} ({column['type']})\n"

    return schema


def execute_sql(sql):
    with engine.connect() as conn:
        result = conn.execute(text(sql))

        rows = [dict(row._mapping) for row in result]

        return rows