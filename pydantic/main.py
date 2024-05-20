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
        statement = select(MetadataCategory).where(MetadataCategory.projectid == settings.project_id).where(MetadataCategory.metadatacategoryid == 74)
        result = session.exec(statement).one()

        model, model_name = generate_model(result)

        return model, model_name
     
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

        if descriptor.fieldtype_python == "Enum":
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
            field = Field(title=title, description=description)
        
        else:
            field = Field(default=default, title=title, description=description, json_schema_extra=pop_default)

        attributes[name] = (type, field)
    
    return create_model(model_name, **attributes, __config__=config), model_name

def generate_json_schema(model, model_name):
    schema_file_path = f"scratch/{model_name}.json"

    with open (schema_file_path, "w") as ft:
        print(json.dumps(model.model_json_schema(), indent=2), file = ft)

def main():
    model, model_name = select_category()
    generate_json_schema(model, model_name)

if __name__ == "__main__":
    main()