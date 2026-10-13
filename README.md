# FDH View

## Description

Filmhuis Den Haag schedule viewer using FastAPI and SQLModel.

Ingests a ScreenWriter XML file with theater screening schedule.

Backend has an API with a main ticketing booth overview and theater hall specific endpoints.

The endpoint serves the 10 upcoming screenings for the day. The frontend automatically refreshes to update its view with the current information.

## Run

`poetry run uvicorn fdhview.main:app --reload`

## Endpoints

* GET `/admin` - upload form protected with Basic Auth.
* POST `/admin/upload` - upload endpoint protected with Basic Auth
* GET `/api/screenings` - serves JSON with upcoming 10 films for today
