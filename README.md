# Chatbot with React + TypeScript + Python + FastAPI

This repository contains a full-stack chatbot application built using React, TypeScript, Python, and FastAPI. The chatbot interacts with users through a simple web interface, utilizing the Groq API to generate responses based on user input.

## Project Structure:

* `frontend/`: Contains the React application code
    * `App.tsx`: The main component for the chatbot interface
    * `ChatService.ts`: Has all the API requests to the backend API
* `backend/`: Represents the FastAPI application
    * `main.py`: Main file executed in the server
    * `routers/`: Defines API routers
    * `db/`: All code related to the database (settings, models, schemas, and actions)
    * `groq_adapter`: An adapter used to interact with the Groq API
    * `.env`: Stores environment variables for API keys and configurations (use `.env.sample` as the model to create it)

## Prerequisites:

* Python 3.10+ and npm (or yarn) installed
* A Groq API key (create one at [https://console.groq.com/keys](https://console.groq.com/keys))

## Setup and Usage:

1. Clone this repository:
    ```bash
    git clone [https://github.com/your-username/fullstack-chatbot.git]
    ```
2. Create a `.env` file in the backend directory with the following variables:
    ```
    GROQ_API_KEY=YOUR_GROQ_API_KEY
    DATABASE_NAME=your_database_name (if you don't define it, the default name will be test)
    ```
3. Install dependencies in both `frontend` and `backend` directories:
    * `frontend`: `cd front/chatbot-client && npm install` (or `yarn`)
    * `backend`: `cd back && pip install -r requirements.txt` (or `yarn`)
4. Start the backend server at `http://localhost:8000`:
    ```bash
    cd api/ && uvicorn main:app --reload
    ```
5. Start the frontend client in your browser at `http://localhost:3000`.
    ```bash
    npm start
    ```

