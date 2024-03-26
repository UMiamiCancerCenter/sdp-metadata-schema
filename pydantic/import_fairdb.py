import psycopg2
from psycopg2 import sql
from pydantic import BaseModel, create_model
import inflection
import json


def connect_to_database(host, database, user, password):
    try:
        conn = psycopg2.connect(
            host=host, database=database, user=user, password=password
        )
        return conn
    except psycopg2.Error as e:
        print("Unable to connect to the database.")
        print(e)
        return None


def get_columns_info(conn, table_name):
    cursor = conn.cursor()
    query = sql.SQL(
        """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
        """
    )
    cursor.execute(query, (table_name,))
    columns_info = cursor.fetchall()
    cursor.close()
    return columns_info


def get_python_type(sql_type):
    if "integer" in sql_type:
        return "int"
    elif "float" in sql_type or "numeric" in sql_type:
        return "float"
    elif "boolean" in sql_type:
        return "bool"
    else:
        return "str"


def create_pydantic_model(class_name, columns_info):
    fields = {}
    for column_name, data_type in columns_info:
        python_type = eval(get_python_type(data_type))
        print(column_name, python_type)
        # snake_case_name = inflection.underscore(column_name)
        fields[column_name] = (python_type, ...)
        print(fields)
    return create_model(class_name, **fields)


def save_model_to_file(model, file_name):
    with open(file_name, "w") as f:
        f.write(model.__repr__())


def generate_json_schema(model):
    return model.model_json_schema()


def save_json_schema_to_file(json_schema, file_name):
    with open(file_name, "w") as f:
        json.dump(json_schema, f, indent=4)


if __name__ == "__main__":
    # Database connection parameters
    host = "life.ccs.miami.edu"
    database = "FAIR_Standards"
    user = "readuser"
    password = "user12&4"

    # Table name and desired class name
    table_name = "category_descriptors"
    class_name = "TestModel"

    # Connect to the database
    conn = connect_to_database(host, database, user, password)
    if conn is None:
        exit()

    # Get column information from the database
    columns_info = get_columns_info(conn, table_name)
    print(columns_info)
    print(type(columns_info))

    # Create Pydantic model dynamically
    pydantic_model = create_pydantic_model(class_name, columns_info)
    print(pydantic_model.model_json_schema())

    # Save Pydantic model to Python file
    # pydantic_file_name = f"{class_name}.py"
    # save_model_to_file(pydantic_model, pydantic_file_name)

    # Generate and save JSON schema
    json_schema = generate_json_schema(pydantic_model)
    json_schema_file_name = f"{class_name}_schema.json"
    save_json_schema_to_file(json_schema, json_schema_file_name)

    # Close database connection
    conn.close()