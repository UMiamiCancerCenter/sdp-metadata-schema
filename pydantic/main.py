import json
from enum import Enum

from sqlmodel import create_engine, Session, select
from pydantic import ConfigDict, Field, create_model

from settings import Settings
from models import MetadataCategory

settings = Settings()

engine = create_engine(settings.pg_dsn)

def pop_default(s):
    s.pop('default')

def select_category():
    with Session(engine) as session:
        statement = select(MetadataCategory).where(MetadataCategory.projectid == settings.project_id)
        results = session.exec(statement)
        models = []
        for result in results:
            models.append(generate_model(result))

        return models
     
def generate_model(result: MetadataCategory):
    model_name = result.category
    config = ConfigDict(title=result.uiname, json_schema_extra={"description": result.description})
    attributes = {}
    result.category_descriptors.sort(key=lambda x: x.categorydescriptorid)

    for descriptor in result.category_descriptors:
        name = descriptor.fieldname
        print(name)
        title = descriptor.uiname
        description = descriptor.description
        importance = descriptor.importance
        default = descriptor.default_value

        if descriptor.fieldtype_python is None:
            
            type = str

        elif descriptor.fieldtype_python == "Enum":
            values = descriptor.controlledvocabulary.split(";")
            members = {}
            for value in values:
                members[value] = value

            type = Enum(name+"_enum", members)
        
        elif descriptor.fieldtype_python == "set[Enum]":
            values = descriptor.controlledvocabulary.split(";")
            members = {}
            for value in values:
                members[value] = value
            
            enum = Enum(name+"_enum", members)

            type = set[enum]

        else:
            type = eval(descriptor.fieldtype_python)


        if importance == 1:
            field_info = Field(title=title, description=description)
        
        else:
            field_info = Field(default=default, title=title, description=description, json_schema_extra=pop_default)

        attributes[name] = (type, field_info)
        
    attributes["entity"] = (str, Field(default=result.uiname, json_schema_extra={"const": result.uiname, "format": "hidden"}))
    
    return create_model(model_name, **attributes, __config__=config), model_name

def generate_json_schema(models):
    for model in models:
        schema_file_path = f"scratch/{settings.project_id}/{model[1]}.json"
        with open (schema_file_path, "w") as ft:
            print(json.dumps(model[0].model_json_schema(), indent=2), file = ft)

def main():
    models = select_category()
    generate_json_schema(models)

if __name__ == "__main__":
    main()