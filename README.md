# Project Description
The goal of this project is to create a REST API for storing and managing contacts. The API is built using the FastAPI infrastructure and uses SQLAlchemy for database management.

Contacts are stored in the database and contain the following information:

- **Name**
- **E-mail address**
- **Phone number**
- **Birthday**

The API has the ability to perform the following actions:

- *Create a new contact*
- *Get a list of all contacts*
- *Get one contact per ID*
- *Update an existing contact*
- *Delete contact*

In addition to the basic CRUD functionality, the API also has the following features:

- *Contacts are available for search by name, surname or e-mail address (Query).*
- *The API is able to retrieve a list of contacts with birthdays for the next 7 days.*

# General Information

- **Using the FastAPI framework to create APIs**
- **Using ORM SQLAlchemy to work with the database**
- **PostgreSQL is used as a database**
- **Support for CRUD operations for contacts**
- **Support for storing a contact's date of birth**
- **Provide API documentation**
- **Using the Pydantic data validation module**
- **Implemented an authentication mechanism in the application**
- **An authorization mechanism has been implemented using JWT tokens so that all operations with contacts are performed only by registered users**
- **The user has access only to his transactions with contacts**
- **A mechanism for verifying the registered user's e-mail has been implemented**
- **A limited number of requests to your contact routes. Limited speed - creating contacts for the user**
- **CORS enabled for REST API**
- **The ability to update the user's avatar has been implemented. Cloudinary service is used**
- **Documentation for this project was created using Sphinx**
- **Covered repository modules with unit tests using the Unittest framework**
- **Functional tests covered the auth route using the pytest framework**