# Hydroponic System Management API

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [API Documentation](#api-documentation)
    - [Authorization](#authorization)
    - [Hydroponic Systems](#hydroponic-systems)
    - [Measurements](#measurements)
    - [Example Usage](#example-usage)
    
## Introduction
This readme is a documentation of API service created to manage hydroponic systems.

Project version: `v1`

## Features
- JWT authorization
- Hydroponic Systems CRUD
- Creating / Displaying measurements from sensors of hydroponic systems

## Tech stack
Technologies used in project. Checkout requiremets.txt for more packages:
- Python
- Django
- Django Rest Framework
- Docker
- Poetry
- PostgreSQL

## Installation
1. Clone project
```
git clone https://github.com/RadekKusiak71/hydrophonic-app.git
```

2. **Configure `.env` (In case of reqruitment process .env is excluded from .gitignore to skip process of creating .env)**.

3. Run docker and navigate to project folder and execute
```bash
docker compose up
```

## API DOCUMENTATION

**Documentation of endpoints is gonna be covered in document but is also available at `/api/swagger/`**

Possible structures of endpoints:
```
1. /api/{objects}/?[filters]&[sorting]
2. /api/{objects}/{id}/
```
1. Api is prefixed with /api/

2. `{objects}`is the name of object(s) you want to return for Ex. `/api/systems/`

3. `{id}` is a id of object mostly for returning data related to object

4. `[filters]` are filtering options which are gonna be coverd later in docs

5. `[sorting]` are sorting options which are gonna be coverd later in docs

### Authorization:

JWT is implemented with refreshing and blacklisting
- User is obtaining access token and refresh token
- Access token lifetime is 15 minutes
- Refresh token lifetime is 24 hours

| Method  | Endpoint | Purpouse | Result |
| ------------- | ------------- |------------- |------------- |
| `POST`  | `/api/register/`  | Creating user | Returns user instance |
| `POST`  | `/api/token/`  | Obtaining a jwtoken | Returns access and refresh token |
| `POST`  | `/api/token/refresh/` | Refreshing jwtoken | Return new access and refresh token |

### Hydroponic Systems
Systems allows user to get systems that are signed to his account

- Systems can be filtered by name (Filter returns a objects that name contains queried parameter)

- In case user tries to access other user system server will return status code 403

- Endpoints are only available for authorized users otherwise server return status code 401

- Endpoint `/api/systems/` is paginated (look for example usage at the end of docs)

| Method  | Endpoint | Purpouse | Result |
| ------------- | ------------- |------------- |------------- |
| `GET`  | `/api/systems/`  | Fetching systems that are signed for user | Returns paginated list of hydroponic systems |
| `POST`  |`/api/systems/`  | Creating a system | Returns hydroponic system |
| `GET`  | `/api/systems/{id}` | Retrieving system | Return hydroponic system with provided id |
| `PUT`  | `/api/systems/{id}` | Updating whole system with provided id | Returns updated instance |
| `PATCH`  | `/api/systems/{id}` | Updating fields of system with provided id | Return updated system |
| `DELETE`  | `/api/systems/{id}` | Deleting system | Returns message |

### Measurements
- Endpoint is only for authorized users and for their systems

- There are a lot of options you can filter measurements by which are available at `/api/swagger/` and the end of the documentation

- In case of trying to fetch data from not owned system, server will return 403


- Endpoints are only available for authorized users otherwise server return status code 401

- `{id}` is a system id which is gonna return measurements for system with provided id

| Method  | Endpoint | Purpouse | Result |
| ------------- | ------------- |------------- |------------- |
| `POST`  | `/api/measurements/`  | Creating measurements | Returns measurements |
| `POST`  | `/api/measurements/system/{id}`  | Fetching measurements for a system | Returns measurements for system with provided id |
| `POST`  | `/api/measurements/system/{id}/latest` | Get 10 last measurements created | Return new access and refresh token |


## Example Usage

To use pagination add queries

```
    /api/systems?page=1 -> returns 10 results
```


Checkout swagger at endpoint:
-   `/api/swagger/`
-   `/api/redoc/`

For endpoints only for authorized users remember to add headers
```
Authorization: "Bearer <your_jwt_token>"
```

### Measurements filters / sorting available

1. Filtering Options
-   Less Than (water_temperature__lt)
-   Greater Than (water_temperature__gt)
-   Less Than (water_ph__lt)
-   Greater Than (water_ph__gt)
-   Total Dissolved Solids (TDS)
-   Less Than (tds__lt)
-   Greater Than (tds__gt)
-   Less Than (timestamp__lt)
-   Greater Than (timestamp__gt)
-   Specific Timestamp (timestamp)
2.  Sorting Options
Ordering
-   Water Temperature (Ascending: water_temperature, Descending: -water_temperature)
-   Water pH (Ascending: water_ph, Descending: -water_ph)
-   TDS (Ascending: tds, Descending: -tds)
-   Timestamp (Ascending: timestamp, Descending: -timestamp)
3.  Pagination Parameters
-   Page: Integer representing the page number within the paginated result set.
-   Page Size: Number of results to return per page.