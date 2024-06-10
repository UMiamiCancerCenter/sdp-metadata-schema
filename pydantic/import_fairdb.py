from settings import Settings
from sqlalchemy import create_engine, select, MetaData
from pydantic import create_model

# def create_sqlmodel_class(table_name, columns):
#     fields = {}
#     for column in columns:
#         column_name = column.name
#         python_type = column.type.python_type
#         # with open ("scratch/category_descriptors_columns.txt", "a") as ft:
#         #     ft.write("name: {}, type: {}".format(column.name, column.type.python_type))
#         #     ft.write("\n")
#         # Convert column names to snake_case
#         # field_name = inflection.underscore(column_name)
#         fields[column_name] = (python_type, Field(default=None))
#     class_name = inflection.camelize(table_name, uppercase_first_letter=True)
#     return create_model(class_name, **fields)

# Retrieve column information for the specified table
# metadata = MetaData()
# metadata.reflect(engine)
# columns_info = metadata.tables[table_name].columns

# Dynamically create a SQLModel class for the table
# sqlmodel_class = create_sqlmodel_class(table_name, columns_info)
# print(sqlmodel_class.__private_attributes__)

# Instantiate SQLModel objects dynamically for each row
# sqlmodel_objects = []
# for row in rows:
#     obj = sqlmodel_class(**dict(row))
#     sqlmodel_objects.append(obj)
# print(sqlmodel_objects)

#     # Optionally, perform operations with the instantiated objects
#     for obj in sqlmodel_objects:
#         print(obj)

settings = Settings()

engine = create_engine(settings.pg_dsn, echo=True)

def get_rows(engine, table_name):
    metadata = MetaData()
    metadata.reflect(engine)
    table = metadata.tables[table_name]
    with engine.connect() as conn:
        query = select(table).where(table.c.metadatacategoryid == 74)
        result = conn.execute(query)
        rows = result.fetchall()
    return rows

if __name__ == "__main__":

    table_name = "category_descriptors"

    rows = get_rows(engine, table_name)

    for row in rows:
        row_map = row._mapping
    

