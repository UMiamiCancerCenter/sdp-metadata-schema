import csv
from pydantic import BaseModel, create_model
import json


def create_pydantic_model(class_name, fields):
    attributes = {}
    for field in fields:
        field_name = field['fieldname']
        field_type = eval(field['fieldtype_schema'])
        attributes[field_name] = (field_type, None)
    return create_model(class_name, **attributes)


def generate_pydantic_class_file(class_name, fields):
    class_content = f"class {class_name}(BaseModel):\n"
    for field in fields:
        field_name = field['fieldname']
        field_type = field['fieldtype_schema']
        class_content += f"    {field_name}: {field_type}\n"
    return class_content


def import_csv_to_pydantic(file_path):
    # Extract class name from file name
    class_name = file_path.split('/')[-1].split('.')[0]

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        # Extract field names and types from the CSV
        fields = list(reader)

        # Create Pydantic model dynamically
        DynamicModel = create_pydantic_model(class_name, fields)

        # Convert Pydantic model to JSON schema
        json_schema = DynamicModel.model_json_schema()

        # Save JSON schema to a file
        schema_file_path = f"{class_name}.json"
        with open(schema_file_path, 'w') as schema_file:
            json.dump(json_schema, schema_file, indent=4)

        # Generate Pydantic class code
        pydantic_class_code = generate_pydantic_class_file(class_name, fields)

        # Save Pydantic class to a Python file
        class_file_path = f"{class_name}.py"
        with open(class_file_path, 'w') as class_file:
            class_file.write("from pydantic import BaseModel\n\n")
            class_file.write(pydantic_class_code)


if __name__ == "__main__":
    file_path = "cellLine.csv"  # Provide the path to your CSV file
    import_csv_to_pydantic(file_path)
