from fastapi import FastAPI, Path, Body
from typing import Annotated, List
from datetime import date, time,datetime

from pydantic import AfterValidator, BaseModel, field_validator

from Business_logic.Business_logic import BusinessLogic
from Business_logic.Models.Note import Note
from Storage_logic.Json_logic import JsonStorage

storage = JsonStorage()
bl = BusinessLogic(storage)

app = FastAPI()

class NoteInput(BaseModel):
    start_time: time
    end_time: time
    text: str

    @field_validator("start_time", "end_time", mode="before")
    def parse_time(cls, v):
            return datetime.strptime(v, "%H:%M").time()



@app.get("/notes/{user_date}")
async def get_notes_by_date(user_date: Annotated[str,AfterValidator(bl.validate_date) ,Path()]):
    notes = bl.chose_or_create_day(user_date)
    notes_json = [i.to_dict() for i in notes]
    return notes_json

@app.post("/notes/add-note/{user_date}")
async def create_new_note(user_date: Annotated[str,AfterValidator(bl.validate_date) ,Path()], notes: Annotated[List[NoteInput], Body()]):
    day_notes = bl.chose_or_create_day(user_date)
    added_notes = []

    for n in notes:
        try:
            parsed_start_time = n.start_time.strftime('%H:%M')
            parsed_end_time = n.end_time.strftime('%H:%M')
            insert_index = bl.find_insert_index(day_notes, f"{parsed_start_time}-{parsed_end_time}")
            bl.write_notes(insert_index, n.text, f"{parsed_start_time}-{parsed_end_time}", user_date, day_notes)
            added_notes.append({"start_time":parsed_start_time, "end_time":parsed_end_time, "text":n.text})
            day_notes = bl.chose_or_create_day(user_date)
        except Exception as e:
            return {"error": str(e)}

    return added_notes

@app.delete("/notes/delete-notes/{id}")
async def delete_note(id: Annotated[int, Path()]):


