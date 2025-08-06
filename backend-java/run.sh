#!/bin/bash
echo "Starting TodoEveryday Spring Boot Backend..."

# Start the Spring Boot application
mvn spring-boot:run

if [ $? -ne 0 ]; then
    echo "Failed to start the application!"
    echo "Make sure you have built the project first with: ./build.sh"
    exit 1
fi
