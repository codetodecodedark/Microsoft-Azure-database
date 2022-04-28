from fastapi import FastAPI, Depends
from typing import Optional, List
from database import get_azure_sql_session_maker
import json
from database import PersonalInfoData
from models import PersonalInfoModel, PersonalInfo

app = FastAPI()

connection_string = None
with open("local.settings.json") as fp:
    connection_string = json.loads(fp.read())


def get_personal_info_logic_session():
    Session = get_azure_sql_session_maker(
        connection_string["AzureSQLConnectionString"])
    session = Session()
    try:
        yield PersonalInfoData(session)
    finally:
        session.close()


@app.get("/")
def index():
    return {"status": "welcome to personal info api"}


@app.get("/all-personal-info", response_model=List[PersonalInfoModel])
async def get_all_personal_info(
    country: Optional[str] = None,
    personal_info_logic_session: PersonalInfoData = Depends(
        get_personal_info_logic_session
    ),
) -> List[PersonalInfoModel]:
    return await personal_info_logic_session.get_all_personal_data(country)


@app.get("/personal-info/{person_id}", response_model=PersonalInfoModel)
async def get_personal_info(
    person_id: int,
    personal_info_logic_session: PersonalInfoData = Depends(
        get_personal_info_logic_session
    ),
) -> PersonalInfoModel:
    return await personal_info_logic_session.get_personal_data(person_id)


@app.post("/personal-info")
async def insert_personal_info(
    personal_info: PersonalInfo,
    personal_info_logic_session: PersonalInfoData = Depends(
        get_personal_info_logic_session
    ),
) -> None:
    await personal_info_logic_session.insert_personal_data(personal_info)


@app.put("/personal-info")
def update_personal_info():
    pass


@app.delete("/personal-info/{person_id}")
async def delete_personal_info(
    person_id: int,
    personal_info_logic_session: PersonalInfoData = Depends(
        get_personal_info_logic_session
    ),
) -> None:
    await personal_info_logic_session.delete_personal_data(person_id)
