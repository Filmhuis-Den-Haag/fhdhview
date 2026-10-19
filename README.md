# FDH View

## Description

Filmhuis Den Haag schedule viewer using FastAPI and SQLModel.

Ingests a ScreenWriter XML file with theater screening schedule.

Backend has an API with a main ticketing booth overview and theater hall specific endpoints.

The endpoint serves the 10 upcoming screenings for the day. The frontend automatically refreshes to update its view with the current information.

## Run

For development run the application locally:

```sh
poetry run uvicorn fdhview.main:app --reload
```

## Endpoints

* GET `/admin` - upload form protected with Basic Auth.
* POST `/admin/upload` - upload endpoint protected with Basic Auth
* GET `/info` - serves desk info endpoint
* GET `/api/screenings` - serves JSON with upcoming 10 films for today
* GET `/api/screenings/prices` - serves JSON with pricing data

## Docker

Run the container with docker-compose:

```sh
docker compose -f docker/docker-compose.yml up
```

## License

The code for this repository is available under the `GNU Affero General Public License v3.0 or later`.

Figtree fonts in `fdhview/static/fonts/` are under the `SIL Open Font License, Version 1.1`.

The logo in `fdhview/static/Logo.svg` is copyright of `Filmhuis Den Haag` and must be replaced.
