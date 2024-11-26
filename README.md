# Chatters

**Chaters** is a real-time chat application built with Django Channels, Vue.js, and Redis for high-performance asynchronous messaging. PostgreSQL serves as the relational database, and B2 (Backblaze) is used for storage.

## Features

- **Real-time Communication**: Leverages Django Channels and WebSockets for instant messaging.
- **Modern Frontend**: Built with Vue.js for a dynamic and user-friendly interface.
- **Asynchronous Backend**: Supports scalable and efficient real-time operations.
- **Persistent Storage**: Utilizes PostgreSQL for structured data and B2 for media files.
- **Caching and Pub/Sub**: Redis powers session management, caching, and Pub/Sub messaging.

## Tech Stack

- **Backend**: Django Channels (WebSocket support)
- **Frontend**: Vue.js (SPA)
- **Database**: PostgreSQL
- **Cache/Message Queue**: Redis
- **Storage**: Backblaze B2

## Installation

### Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL
- Redis
- Backblaze B2 credentials

### Backend Setup

1. Clone the repository:
   git clone https://github.com/QusaiAlbonni/chatters.git
   cd chatapp

2. Install dependencies:
   pip install -r requirements.txt

3. Apply migrations:
   python manage.py migrate

4. Configure environment variables:
   - Database: `DATABASE_URL`
   - Redis: `CACHE_URL`
   - Secret Key: `SECRET_KEY`
   - B2: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_ENDPOINT_URL`, `AWS_S3_REGION_NAME`

   you can also skip B2 with DEBUG=on for local development

5. Run the server:
```sh
   python manage.py runserver
```
### Frontend Setup

1. Navigate to the `frontend` directory:
```sh
   cd frontend
```

2. Install dependencies:
```sh
   npm install
```

3. Setup Env with:
- `VITE_API_HOST` for the backend api
- `VITE_WS_HOST` for websockets

4. Start the development server:
```sh
   npm run dev
```
- you may also build the project:
```sh
   npm run build
```

## Deployment

For production, consider using:
- **Gunicorn/Daphne** with ASGI for Django Channels.
- **NGINX** for serving static files and acting as a reverse proxy.
- **Docker** for containerization.

## Contributing

We welcome contributions! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
*/
