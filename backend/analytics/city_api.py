from fastapi import FastAPI

app=FastAPI()

@app.get("/health")

def health():

    return {

        "status":"running"

    }


@app.get("/city")

def city():

    return {

        "city":"Vijayawada",

        "status":"Healthy"

    }