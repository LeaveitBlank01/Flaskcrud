# People API with Basic Authentication

## Overview

This is a RESTful API built with Flask that allows you to manage information about people. The API provides endpoints to:

* Retrieve a list of people.
* Retrieve details of a specific person by ID.
* Create new person entries.
* Update existing person entries.
* Delete person entries.
* Search for people based on name or city.

The API uses Basic Authentication to secure endpoints from unauthorized access.

## Requirements

* Python 3.x
* Flask
* Flask-MySQLdb (or a similar library for database interaction)
* MySQL (or a compatible database)
* Flask-HTTPAuth (for Basic Authentication)
* Marshmallow (for input validation)
* dicttoxml (for XML formatting) (Optional)

## Installation

1. Clone the Repository:

   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
