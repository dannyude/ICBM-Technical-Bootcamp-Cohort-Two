from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# pydantic is always used to validate data coming from the request body.
class AnimalRequest(BaseModel):
    animal: str

@app.post("/classify")
# 2. FastAPI sees a Pydantic model type, so it looks in the request body
def classify(payload: AnimalRequest):
    # note that in fastapi, the type hint is always on the right side of the parameter. 
    # in this case payload is the parameter, and its type is AnimalRequest, which is a Pydantic model.
    # 3. Access the data using object dot notation
    chosen_animal = payload.animal.lower()
    
    if chosen_animal == "dog":
        return {"message": "This is a dog."}
    elif chosen_animal == "cat":
        return {"message": "This is a cat."}
    else:
        return {"message": "Unknown animal."}