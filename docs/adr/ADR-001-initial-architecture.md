# ADR-001 Initial Architecture

Date: 2026-10-13

## Context

Filmhuis Den Haag (FDH) has a display above the ticket counter that shows ticket pricing information and upcoming screenings with ticket sales. Currently it's running a proprietary system that is leased from a third party. Since FDH already has all feature and ticket information available, as part of a weekly ScreenWriter XML, the desire is to have their own solution to replace the proprietary system.

It needs to display both ticket pricing info and upcoming features with information like the start and end times, KijkWijzer ratings, theater room, and other useful data.

## Decision

A FastAPI backend will be able to ingest the ScreenWriter XML and collect all feature information into a simple database. Subsequently for ticketing info a JSON endpoint will serve the next 10 upcoming features. A simple frontend page can automatically refresh every couple minutes in order to display the latest valid information.

When a new XML is uploaded it replaces all information in the database with the new data. This way the backend only holds currently relevant information.

The upload endpoints will be secured using a basic auth password.

For each screening at least the following information is stored:

* unique session id - int, as reference
* screen - which screen/room is it being displayed
* start time - timestamp
* end time - timestamp
* duration - in seconds
* title - str
* rating - int
* seats_total - int, called seats_avaialble in XML
* seats_sold - int
* en_subs - bool, if the feature has english subtitles
* intro - bool, if there is an introductory talk
* outro - bool, if there is an after talk
* kijkwijzer - list of kijkwijzer ids
* tags - any additional tags that may be useful

## MVP Definition

An authenticated user needs to be able to log into the upload page and provide an XML with data. Any (parsing) errors will be displayed to the user if there are issues.

A simple browser client connected to a display can then open a html page that will automatically refresh every couple minutes with updated/current information.

## Future Improvements

* add display endpoints for each of the theater rooms with current and upcoming feature information
* be able to synchronize with a ticketing backend without the user having to upload an XML
