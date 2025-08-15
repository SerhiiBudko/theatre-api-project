# Theatre API

DRF API for theatre with ticket booking functionality.

## Project Description

This project is a REST API for a theatre that allows:
- Viewing information about theatre halls, genres, actors, plays, and performances
- Booking tickets for performances
- Viewing available and occupied seats
- Managing user reservations

## Technologies

- Django 4.2.23
- Django REST Framework 3.16.1
- JWT authentication (djangorestframework-simplejwt)
- Swagger documentation (drf-spectacular)
- SQLite database

## Installation and Setup

### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd theatre-api-project
```

2. Run with Docker Compose:
```bash
./docker-run.sh
```

Or manually:
```bash
docker-compose up --build
```

The API will be available at http://localhost:8000/api/

### Option 2: Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd theatre-api-project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
# or
venv\Scripts\activate  # for Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Create sample data:
```bash
python manage.py create_sample_data
```

7. Start the server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/user/register/` - Register new user
- `POST /api/user/token/` - Get JWT token
- `POST /api/user/token/refresh/` - Refresh JWT token
- `GET /api/user/me/` - Current user information

### Theatre Halls
- `GET /api/halls/` - List all halls
- `POST /api/halls/` - Create new hall (admin only)
- `GET /api/halls/{id}/` - Hall details
- `PUT /api/halls/{id}/` - Update hall (admin only)
- `DELETE /api/halls/{id}/` - Delete hall (admin only)

### Genres
- `GET /api/genres/` - List all genres
- `POST /api/genres/` - Create new genre (admin only)
- `GET /api/genres/{id}/` - Genre details
- `PUT /api/genres/{id}/` - Update genre (admin only)
- `DELETE /api/genres/{id}/` - Delete genre (admin only)

### Actors
- `GET /api/actors/` - List all actors
- `POST /api/actors/` - Create new actor (admin only)
- `GET /api/actors/{id}/` - Actor details
- `PUT /api/actors/{id}/` - Update actor (admin only)
- `DELETE /api/actors/{id}/` - Delete actor (admin only)

### Plays
- `GET /api/plays/` - List all plays
- `POST /api/plays/` - Create new play (admin only)
- `GET /api/plays/{id}/` - Play details
- `PUT /api/plays/{id}/` - Update play (admin only)
- `DELETE /api/plays/{id}/` - Delete play (admin only)

### Performances
- `GET /api/performances/` - List all performances
- `POST /api/performances/` - Create new performance (admin only)
- `GET /api/performances/{id}/` - Performance details
- `PUT /api/performances/{id}/` - Update performance (admin only)
- `DELETE /api/performances/{id}/` - Delete performance (admin only)
- `GET /api/performances/{id}/seats/` - View available and occupied seats

### Reservations
- `GET /api/reservations/` - List reservations (authenticated users only)
- `POST /api/reservations/` - Create new reservation (authenticated users only)
- `GET /api/reservations/my/` - My reservations (authenticated users only)

## API Documentation

Swagger documentation is available at: http://localhost:8000/api/docs/

## Usage Examples

### User Registration
```bash
curl -X POST http://localhost:8000/api/user/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "first_name": "John", "last_name": "Doe"}'
```

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/user/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### View Plays
```bash
curl http://localhost:8000/api/plays/
```

### View Available Seats
```bash
curl http://localhost:8000/api/performances/1/seats/
```

### Create Reservation
```bash
curl -X POST http://localhost:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"performance_id": 1, "seats": [{"row": 1, "seat": 1}, {"row": 1, "seat": 2}]}'
```

### View My Reservations
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/reservations/my/
```

## Data Models

### TheatreHall
- `name` - Hall name
- `rows` - Number of rows
- `seats_in_row` - Number of seats per row

### Genre
- `name` - Genre name

### Actor
- `first_name` - Actor's first name
- `last_name` - Actor's last name

### Play
- `title` - Play title
- `description` - Play description
- `genres` - Genres (ManyToMany with Genre)
- `actors` - Actors (ManyToMany with Actor)

### Performance
- `play` - Play (ForeignKey to Play)
- `theatre_hall` - Theatre hall (ForeignKey to TheatreHall)
- `show_time` - Performance time

### Reservation
- `created_at` - Reservation creation time
- `user` - User (ForeignKey to User)

### Ticket
- `row` - Row number
- `seat` - Seat number
- `performance` - Performance (ForeignKey to Performance)
- `reservation` - Reservation (ForeignKey to Reservation)

## Features

- JWT authentication with access and refresh tokens
- Automatic seat validation during booking
- Duplicate seat prevention
- Request rate limiting
- Swagger API documentation
- Different access levels for users and administrators

## Docker

### Quick Start with Docker

The easiest way to run the project is using Docker:

```bash
# Clone the repository
git clone <repository-url>
cd theatre-api-project

# Run with Docker Compose
./docker-run.sh
```

### Docker Commands

```bash
# Build and start services
docker-compose up --build

# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build --force-recreate
```

### Docker Services

- **Web**: Django application (port 8000)
- **Database**: PostgreSQL (port 5432)

## Testing

For API testing you can use:
- Swagger UI: http://localhost:8000/api/docs/
- curl commands
- Postman or other API testing tools

## Demo Script

Run the demo script to see the API in action:
```bash
python demo_api.py
```

This script demonstrates:
- User registration and authentication
- Viewing plays and performances
- Creating reservations
- Seat validation
- Error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

If you have any questions or issues, please create an issue in the GitHub repository. 