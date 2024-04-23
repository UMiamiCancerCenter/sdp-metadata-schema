from settings import Settings
from sqlmodel import create_engine, Session, select
from models import CategoryDescriptor

settings = Settings()

engine = create_engine(settings.pg_dsn, echo=True)

def select_descriptors():
    with Session(engine) as session:
        statement = select(CategoryDescriptor).where(CategoryDescriptor.metadatacategoryid == 74)
        results = session.exec(statement)
        for descriptor in results:
            print(descriptor)

def main():
    select_descriptors()

if __name__ == "__main__":
    main()