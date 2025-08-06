#!/bin/bash
echo "Building TodoEveryday Spring Boot Backend..."

# Clean and build the project
mvn clean install

if [ $? -eq 0 ]; then
    echo "Build completed successfully!"
    echo "You can now run the application with: mvn spring-boot:run"
    echo "Or run: java -jar target/todo-backend-1.0.0.jar"
else
    echo "Build failed!"
    exit 1
fi
