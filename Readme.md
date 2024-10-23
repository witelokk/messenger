# Messenger App

A simple messenger application built using FastAPI (backend), React (frontend), and Aiogram (Telegram bot). The application allows users to register, send/receive messages in real-time, and receive notifications through a Telegram bot when they are offline.

## Features

1. **User Registration and Authentication:**
   - Users can register new accounts.
   - Authentication and authorization are handled through FastAPI for secure access to the API.

2. **Sending and Receiving Messages:**
   - Users can send and receive messages in real time via WebSocket.
   - Message delivery and retrieval occur instantly.

3. **Message History:**
   - All messages are saved in the database.
   - Users can access the history of their conversations with others.

4. **Telegram Bot Notifications:**
   - A simple Telegram bot built with Aiogram is used to notify users about new messages if they are offline.

5. **Web Interface:**
   - A basic web page created with React allows users to interact with the service.
   - The web page supports sending and receiving messages in real time.

6. **Docker Compose for Easy Setup:**
   - The project is fully containerized using Docker Compose, making it easy to run and test.

## Project Structure

```
src/
├── backend/          # FastAPI backend for handling API requests
├── frontend/         # React frontend for the web interface
└── telegram_bot/     # Aiogram-based Telegram bot for notifications
```

### Backend

The backend is built using [FastAPI](https://fastapi.tiangolo.com/) and exposes a set of APIs for user registration, authentication, sending/receiving messages, and retrieving message history.

**API Documentation:**
Once the backend is running, the full API documentation is available at `/api/docs` (Swagger UI) or `/api/redoc` (ReDoc).

### Frontend

The frontend is built using React. It provides a simple interface for registering, logging in, and sending/receiving messages.

### Telegram Bot

The Telegram bot, built using Aiogram, sends notifications to users if they are offline when new messages are received.

### Database

The application uses a PostgreSQL database to store:
- User data (registration/authentication details)
- Message history

## Running the Application

This project uses Docker Compose to orchestrate the backend, frontend, database, and Telegram bot. Ensure you have Docker and Docker Compose installed.

### Steps to Run:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/witelokk/messenger
   cd messenger
   ```

2. **Build and run the application:**
   Run the following command in the project root directory to start all services:
   ```bash
   POSTGRES_USERNAME=... POSTGRES_PASSWORD=... BOT_TOKEN=... BOT_USERNAME=... docker-compose up --build
   ```

   This command will start:
   - FastAPI backend at `http://0.0.0.0:80/api`
   - React frontend at `http://0.0.0.0:80/`
   - PostgreSQL database
   - Redis instance
   - Telegram bot

4. **Setup Telegram Bot:**
   - Create a bot on Telegram using [BotFather](https://core.telegram.org/bots#botfather) and get the API token.
   - Add the token to the `.env` file in the `src/telegram_bot` folder.
   - The bot will notify users of any new messages when they are offline.

## API Endpoints

### API Endpoints

- **Sessions**:
    - `POST /sessions/`: Login, returns a session token.

- **Users**:
    - `POST /users/`: Register a new user.
    - `GET /users/username/{username}`: Get user by username (auth required).
    - `GET /users/{user_id}`: Get user by ID (auth required).
    - `DELETE /users/{user_id}`: Delete user by ID (auth required).

- **Messages**:
    - `POST /messages/`: Send a message (auth required).
    - `GET /messages/to/{to_id}`: Get messages sent to a specific user (auth required).

- **Chats**:
    - `GET /chats/`: Get a list of chats (auth required).

- **WebSocket**:
    - `GET /websocket`: Real-time messaging via WebSocket (auth required).

- **Telegram**:
    - `POST /tg_key`: Create a Telegram integration key (auth required).

For more details, see `/api/docs`.

## Development

To run individual components outside of Docker (e.g., for development):

### Backend:
1. Navigate to the backend directory:
    ```bash
    cd src/backend
    ```
2. Install dependencies using [Poetry](https://python-poetry.org/):
    ```bash
    poetry install
    ```
3. Setup .env (see .env.example)
4. Start the FastAPI development server:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```

### Frontend:
1. Navigate to `src/frontend`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Setup .env (see .env.example)
4. Start the React app:
   ```bash
   npm start
   ```

### Telegram Bot:
1. Navigate to the bot directory:
    ```bash
    cd src/telegram_bot
    ```
2. Install dependencies using Poetry:
    ```bash
    poetry install
    ```
3. Setup .env (see .env.example)
4. Start the Telegram bot:
    ```bash
    poetry run python bot.py
    ```
