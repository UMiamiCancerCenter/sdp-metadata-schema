from sqlmodel import SQLModel, Field

class CategoryDescriptor(SQLModel, table=True):
    __tablename__ = "category_descriptors"

    categorydescriptorid: int | None = Field(default=None, primary_key=True)
    metadatacategoryid: int
    fieldname: str | None = Field(default=None)