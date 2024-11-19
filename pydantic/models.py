from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

class MetadataCategory(SQLModel, table=True):
    __tablename__ = 'metadata_category'
    __table_args__ = (
        UniqueConstraint('category', 'projectid', name='metadata_category_category_projectid_key'),
    )

    metadatacategoryid: int | None = Field(default=None, primary_key=True)
    projectid: int
    category: str | None = Field(default=None)
    uiname: str | None = Field(default=None)
    description: str | None = Field(default=None)
    canonical_type: str | None = Field(default=None)
    csvtemplate_name: str | None = Field(default=None)
    categorytype: str | None = Field(default=None)
    os_cp_id: str | None = Field(default=None)

    category_descriptors: list["CategoryDescriptor"] = Relationship(back_populates="metadata_category")

class CategoryDescriptor(SQLModel, table=True):
    __tablename__ = "category_descriptors"
    __table_args__ = (
        UniqueConstraint('fieldname', 'metadatacategoryid', name='category_descriptors_fieldname_metadatacategoryid_key'),
        )

    categorydescriptorid: int | None = Field(default=None, primary_key=True)
    metadatacategoryid: int = Field(foreign_key="metadata_category.metadatacategoryid")
    importance: int
    fieldname: str | None = Field(default=None)
    fieldpropertyiri: str | None = Field(default=None)
    description: str | None = Field(default=None)
    fieldtype_schema: str | None = Field(default=None)
    ontologyname: str | None = Field(default=None)
    ontologybranch: str | None = Field(default=None)
    ontologyiri: str | None = Field(default=None)
    controlledvocabulary: str | None = Field(default=None)
    dateloaded: datetime | None = Field(default=None)
    pittable: str | None = Field(default=None)
    pitmilestone: str | None = Field(default=None)
    pharosspec: str | None = Field(default=None)
    metadataspec: str | None = Field(default=None)
    fieldcardinality: str | None = Field(default=None)
    dataupdated: datetime | None = Field(default=None)
    fieldtype_cedar: str | None = Field(default=None)
    custom_importance: str | None = Field(default=None)
    associated_milestone_link: str | None = Field(default=None)
    fieldtype_os: str | None = Field(default=None)
    default_value: str | None = Field(default=None)
    date_format: str | None = Field(default=None)
    range_min: str | None = Field(default=None)
    range_max: str | None = Field(default=None)
    datafile_field: str | None = Field(default=None)
    dcc_field: str | None = Field(default=None)
    fieldtype_dcc: str | None = Field(default=None)
    dcc_importance: str | None = Field(default=None)
    dcc_units: str | None = Field(default=None)
    dcc_validation: str | None = Field(default=None)
    dcc_logic: str | None = Field(default=None)
    numberfractiondigits: int | None = Field(default=None)
    showwhen: str | None = Field(default=None)
    capturetime_os: str | None = Field(default=None)
    fieldtype_python: str | None = Field(default=None)
    uiname: str | None = Field(default=None)
    metadata_tier: str | None = Field(default=None)
    hidden: bool

    metadata_category: MetadataCategory | None = Relationship(back_populates="category_descriptors")