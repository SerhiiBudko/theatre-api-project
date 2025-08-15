#!/bin/bash

echo "🎭 Theatre API Docker Setup"
echo "=========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "🐳 Building and starting Theatre API with Docker Compose..."
echo ""

# Build and start the services
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Theatre API is running successfully!"
    echo ""
    echo "🌐 API Documentation: http://localhost:8000/api/docs/"
    echo "🎫 API Base URL: http://localhost:8000/api/"
    echo ""
    echo "📊 Service Status:"
    docker-compose ps
    echo ""
    echo "📝 To view logs: docker-compose logs -f"
    echo "🛑 To stop services: docker-compose down"
    echo ""
    echo "🎉 Happy testing!"
else
    echo "❌ Failed to start services. Check logs with: docker-compose logs"
    exit 1
fi 