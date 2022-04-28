from sqlalchemy import create_engine
import urllib
from sqlalchemy.orm import sessionmaker, Session
from dtos import PersonalInfoDto
from models import PersonalInfo


def get_azure_sql_session_maker(connection_string):
    engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(connection_string)}",
        connect_args={"check_same_thread": False, "autocommit": True},
    )
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


class PersonalInfoData:
    def __init__(self, database_session: Session):
        self.session = database_session

    async def get_all_personal_data(self, country):
        if country:
            return (
                self.session.query(PersonalInfoDto)
                .where(PersonalInfoDto.country == country.lower())
                .all()
            )
        else:
            return self.session.query(PersonalInfoDto).all()

    async def get_personal_data(self, person_id):
        return (
            self.session.query(PersonalInfoDto)
            .where(PersonalInfoDto.id == person_id)
            .first()
        )

    async def insert_personal_data(self, personal_info: PersonalInfo):
        self.session.add(
            PersonalInfoDto(
                first_name=personal_info.first_name.lower(),
                last_name=personal_info.last_name.lower(),
                age=personal_info.age,
                gender=personal_info.gender.lower(),
                city=personal_info.city.lower(),
                country=personal_info.country.lower(),
            )
        )
        self.session.commit()

    async def delete_personal_data(self, person_id):
        personal_data = await self.get_personal_data(person_id)
        if personal_data:
            self.session.delete(personal_data)
            self.session.commit()
