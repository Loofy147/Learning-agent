# Question & Answer API

This is a simple FastAPI application for managing a database of questions and answers.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

### Create a new question

* **Endpoint:** `POST /questions/`
* **Request Body:**
  ```json
  {
    "question": "string",
    "answer": "string",
    "topic": "string",
    "difficulty": "string"
  }
  ```
* **Response:**
  ```json
  {
    "id": "integer",
    "question": "string",
    "answer": "string",
    "topic": "string",
    "difficulty": "string"
  }
  ```

### Get a specific question

* **Endpoint:** `GET /questions/{question_id}`
* **Response:**
  ```json
  {
    "id": "integer",
    "question": "string",
    "answer": "string",
    "topic": "string",
    "difficulty": "string"
  }
  ```

### Get all questions

* **Endpoint:** `GET /questions/`
* **Query Parameters:**
  - `skip` (integer, optional): Number of questions to skip.
  - `limit` (integer, optional): Maximum number of questions to return.
* **Response:** A list of question objects.

### Update a question

* **Endpoint:** `PUT /questions/{question_id}`
* **Request Body:**
  ```json
  {
    "question": "string",
    "answer": "string",
    "topic": "string",
    "difficulty": "string"
  }
  ```
* **Response:** The updated question object.

### Delete a question

* **Endpoint:** `DELETE /questions/{question_id}`
* **Response:** `204 No Content`

### Get a random question

* **Endpoint:** `GET /questions/random/`
* **Response:** A random question object.

### Search questions by topic

* **Endpoint:** `GET /questions/search/`
* **Query Parameters:**
  - `topic` (string, required): The topic to search for.
  - `skip` (integer, optional): Number of questions to skip.
  - `limit` (integer, optional): Maximum number of questions to return.
* **Response:** A list of question objects matching the topic.

## Roadmap

### Advanced Features

* **Pagination for all listings:** Ensure all endpoints that return a list of items are paginated.

### Potential Integrations

* **User authentication:** Integrate an authentication system to manage access to the API.
* **Caching:** Implement a caching layer to improve the performance of frequently requested data.
* **Full-text search:** Use a more advanced search engine like Elasticsearch for more powerful search capabilities.