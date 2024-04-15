from sqlalchemy import create_engine, select, Table, MetaData
from sqlmodel import SQLModel, Field
import inflection

def get_rows(engine, table_name):
    metadata = MetaData()
    metadata.reflect(engine)
    table = metadata.tables[table_name]
    with engine.connect() as conn:
        query = select([table])
        result = conn.execute(query)
        rows = result.fetchall()
    return rows

def create_sqlmodel_class(table_name, columns):
    fields = {}
    for column in columns:
        column_name = column['name']
        python_type = column['type'].python_type
        # Convert column names to snake_case
        field_name = inflection.underscore(column_name)
        fields[field_name] = (python_type, Field(default=None))

    class_name = inflection.camelize(table_name, uppercase_first_letter=True)
    return type(class_name, (SQLModel,), fields)

if __name__ == "__main__":
    # Connect to the PostgreSQL database
    DATABASE_URL = "postgresql://username:password@localhost/database_name"
    engine = create_engine(DATABASE_URL)

    # Specify the table name
    table_name = "your_table_name"

    # Retrieve column information for the specified table
    metadata = MetaData()
    metadata.reflect(engine)
    columns_info = metadata.tables[table_name].columns

    # Dynamically create a SQLModel class for the table
    sqlmodel_class = create_sqlmodel_class(table_name, columns_info)

    # Retrieve rows from the specified table
    rows = get_rows(engine, table_name)

    # Instantiate SQLModel objects dynamically for each row
    sqlmodel_objects = []
    for row in rows:
        obj = sqlmodel_class(**dict(row))
        sqlmodel_objects.append(obj)

    # Optionally, perform operations with the instantiated objects
    for obj in sqlmodel_objects:
        print(obj)