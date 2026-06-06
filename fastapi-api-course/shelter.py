# --- Rules on importing packages in Python ---
# Convention: standard-library imports go first, then third-party packages.
# "from <package> import <name>" pulls one specific name out of a package so
# you can use it directly, without writing the package prefix every time.

from fastapi import FastAPI          # FastAPI: the third-party web framework class
from typing import Optional          # typing: standard library; Optional marks a value that may be None
from pydantic import BaseModel, ConfigDict   # pydantic: third-party data-validation package

# Create the application instance. Every route below is attached to this object.
app = FastAPI()


# ============================================================================
# APPROACH 1 -- buy_animal_1: WITHOUT Pydantic
# The values come from the URL itself: a path parameter + optional query parameters.
# ============================================================================

# Old one without Pydantic
@app.post("/shelter/{animal}") # path parameter
def buy_animal_1(animal: str, color: Optional[str] = None, animal_type: Optional[str] = None):  # query parameters
    if color and animal_type:
        return {"message": f"You bought a {color} {animal_type} {animal}."}
    if color:
        return {"message": f"You bought a {color} {animal}."}
    if animal_type:
        return {"message": f"You bought a {animal_type} {animal}."}
    return {"message": f"You bought a {animal}."}

    # Example only (would need "from pydantic import Field" to work):
    # name: str = Field(min_length=1, max_length=50)


# ============================================================================
# APPROACH 2 -- buy_animal_2: WITH Pydantic
# The values come from the JSON request body, described by a Pydantic model.
# ============================================================================

# --- Pydantic model ---
# A Pydantic model is a class that inherits from BaseModel. It describes the
# shape of the data we expect, and Pydantic validates that incoming data for us.
class AnimalPurchase(BaseModel):
    # ConfigDict(extra='forbid') tells Pydantic to reject any extra field that
    # is not declared below, instead of silently ignoring it.
    model_config = ConfigDict(extra='forbid')

    # --- Basic data types (type hints) ---
    # Each field is written as "name: type" so Pydantic knows what to expect.
    id: int                          # int -> whole number
    name : str                       # str -> text
    amount : int                     # int -> whole number
    # --- typing ---
    # Optional[str] = None means "a string OR None"; None is the default value,
    # so these two fields are not required.
    color: Optional[str] = None
    type: Optional[str] = None


# --- HTTP method ---
# @app.post(...) registers this function to handle POST requests.
# POST is the method used to send/create data through the request body.
@app.post("/shelter")
# Because the parameter is typed with a Pydantic model (Animal_purchase),
# FastAPI reads the incoming values from the JSON request body.
def buy_animal_2(purchase: AnimalPurchase):
    if name := purchase.name:
        if purchase.color and purchase.type:
            return {"message": f"the name of the animal purchased is {name} and it is a {purchase.color} {purchase.type}."}
        if purchase.color:
            return {"message": f"the name of the animal purchased is {name} and it is a {purchase.color}."}
        if purchase.type:
            return {"message": f"the name of the animal purchased is {name} and it is a {purchase.type}."}
        return {"message": f"the name of the animal purchased is {name}."}


# --- Path parameters ---
# A path parameter is a variable written inside curly braces in the URL,
# e.g. "/shelter/{animal_id}". Its value is taken straight from the URL path.
# method delete
@app.delete("/shelter/{animal_id}")  # dynamic routing
def delete_animal(animal_id: int):
    if animal_id == 1:
        return {"message": f"You deleted the dog with id {animal_id}."}
    if animal_id == 2:
        return {"message": f"You deleted the cat with id {animal_id}."}
    return {"message": f"you cannot delete this record with id {animal_id}."}


# ============================================================================
# EXTRA EXAMPLE (commented out for beginners)
# A simple POST route with its own Pydantic model.
# Remove the leading "# " on each line below to turn it on.
# ============================================================================
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    content: str
    published: bool

@app.post("/blog/new")
def create_blog(request_body: Blog):
    return {"message": "A new blog post has been created.", "blog": request_body}
