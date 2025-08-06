# TodoEveryday Backend - Java Spring Boot

A complete Java Spring Boot backend implementation of the TodoEveryday application, migrated from the original Python FastAPI backend while maintaining 100% API compatibility.

## 🚀 Features

- **Complete API Migration**: All original FastAPI endpoints migrated to Spring Boot
- **RESTful API**: Full CRUD operations for todo management
- **Advanced Filtering**: Filter todos by status (all, completed, pending)
- **Pagination**: Built-in pagination support for large todo lists
- **Batch Operations**: Delete completed, delete all, or complete all todos
- **Statistics**: Get comprehensive todo statistics including overdue items
- **Data Validation**: Comprehensive input validation using Bean Validation
- **Error Handling**: Global exception handling with detailed error responses
- **API Documentation**: Interactive Swagger UI documentation
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Database**: H2 in-memory database for development (easily configurable for production)

## 🛠️ Technology Stack

- **Java 17**: Modern Java features and performance
- **Spring Boot 3.2.0**: Latest Spring Boot framework
- **Spring Data JPA**: Database abstraction and ORM
- **H2 Database**: In-memory database for development
- **Bean Validation**: Input validation and constraints
- **SpringDoc OpenAPI**: API documentation generation
- **Maven**: Dependency management and build tool

## 📋 API Endpoints

All endpoints maintain the same structure as the original Python backend:

### Todo Operations
- `GET /api/v1/todos` - Get todos with filtering and pagination
- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a specific todo
- `PATCH /api/v1/todos/{id}/toggle` - Toggle todo completion status
- `DELETE /api/v1/todos/{id}` - Delete a specific todo

### Batch Operations
- `POST /api/v1/todos/batch` - Perform batch operations (delete completed, delete all, complete all)

### Statistics
- `GET /api/v1/todos/stats` - Get todo statistics (total, completed, pending, overdue)

### Query Parameters
- `status`: Filter by status (`all`, `completed`, `pending`)
- `page`: Page number (starts from 1)
- `limit`: Number of items per page (1-100)

## 🏃‍♂️ Quick Start

### Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

### Installation & Running

1. **Clone and Navigate**
   ```bash
   cd backend-java
   ```

2. **Build the Project**
   ```bash
   # Windows
   build.bat
   
   # Linux/Mac
   chmod +x build.sh
   ./build.sh
   
   # Or manually
   mvn clean install
   ```

3. **Run the Application**
   ```bash
   # Windows
   run.bat
   
   # Linux/Mac
   chmod +x run.sh
   ./run.sh
   
   # Or manually
   mvn spring-boot:run
   
   # Or run the JAR
   java -jar target/todo-backend-1.0.0.jar
   ```

4. **Access the Application**
   - API Base URL: `http://localhost:8080/api/v1/todos`
   - Swagger UI: `http://localhost:8080/swagger-ui.html`
   - H2 Console: `http://localhost:8080/h2-console` (JDBC URL: `jdbc:h2:mem:todoeveryday`)

## 📚 API Examples

### Create a Todo
```bash
curl -X POST http://localhost:8080/api/v1/todos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Spring Boot",
    "description": "Complete the migration from FastAPI to Spring Boot",
    "priority": 3,
    "dueDate": "2025-08-10T23:59:59"
  }'
```

### Get All Todos
```bash
curl "http://localhost:8080/api/v1/todos?status=all&page=1&limit=10"
```

### Update a Todo
```bash
curl -X PUT http://localhost:8080/api/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "isCompleted": true
  }'
```

### Get Statistics
```bash
curl http://localhost:8080/api/v1/todos/stats
```

## 🏗️ Project Structure

```
backend-java/
├── src/
│   ├── main/
│   │   ├── java/com/todoeveryday/
│   │   │   ├── TodoEveryDayApplication.java    # Main application class
│   │   │   ├── config/                         # Configuration classes
│   │   │   │   ├── OpenApiConfig.java         # OpenAPI/Swagger config
│   │   │   │   └── WebConfig.java             # CORS and web config
│   │   │   ├── controller/                    # REST controllers
│   │   │   │   └── TodoController.java        # Todo REST endpoints
│   │   │   ├── dto/                           # Data Transfer Objects
│   │   │   │   ├── TodoCreateRequest.java     # Create todo request
│   │   │   │   ├── TodoUpdateRequest.java     # Update todo request
│   │   │   │   ├── TodoResponse.java          # Todo response
│   │   │   │   ├── TodoListResponse.java      # Paginated list response
│   │   │   │   ├── BaseResponse.java          # Generic response wrapper
│   │   │   │   ├── StatsResponse.java         # Statistics response
│   │   │   │   ├── BatchRequest.java          # Batch operation request
│   │   │   │   ├── FilterStatus.java          # Status filter enum
│   │   │   │   └── BatchAction.java           # Batch action enum
│   │   │   ├── exception/                     # Exception handling
│   │   │   │   └── GlobalExceptionHandler.java # Global exception handler
│   │   │   ├── model/                         # JPA entities
│   │   │   │   └── Todo.java                  # Todo entity
│   │   │   ├── repository/                    # Data access layer
│   │   │   │   └── TodoRepository.java        # Todo JPA repository
│   │   │   └── service/                       # Business logic layer
│   │   │       └── TodoService.java          # Todo business logic
│   │   └── resources/
│   │       └── application.properties         # Application configuration
│   └── test/
│       └── java/com/todoeveryday/
│           └── TodoEveryDayApplicationTests.java # Basic tests
├── pom.xml                                    # Maven dependencies
├── build.bat / build.sh                      # Build scripts
├── run.bat / run.sh                          # Run scripts
└── README.md                                 # This file
```

## 🔧 Configuration

### Database Configuration

**Development (H2 In-Memory)**
```properties
spring.datasource.url=jdbc:h2:mem:todoeveryday
spring.datasource.driver-class-name=org.h2.Driver
spring.jpa.hibernate.ddl-auto=create-drop
```

**Production (MySQL Example)**
```properties
spring.datasource.url=jdbc:mysql://localhost:3306/todoeveryday
spring.datasource.username=todo_user
spring.datasource.password=todo_password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.jpa.hibernate.ddl-auto=validate
```

### Server Configuration
```properties
server.port=8080
server.servlet.context-path=/
```

### CORS Configuration
```properties
spring.web.cors.allowed-origins=*
spring.web.cors.allowed-methods=GET,POST,PUT,PATCH,DELETE,OPTIONS
```

## 🧪 Testing

### Run Tests
```bash
mvn test
```

### API Testing with Swagger UI
1. Start the application
2. Open `http://localhost:8080/swagger-ui.html`
3. Use the interactive interface to test all endpoints

## 📊 Migration Details

### Maintained Compatibility
- **Same API Endpoints**: All FastAPI routes preserved
- **Same Request/Response Format**: JSON structure unchanged
- **Same Query Parameters**: Filtering and pagination identical
- **Same Status Codes**: HTTP response codes maintained
- **Same Error Format**: Error response structure preserved

### Enhancements
- **Better Performance**: Spring Boot optimizations and JPA query optimization
- **Better Documentation**: Enhanced Swagger documentation with examples
- **Better Validation**: Comprehensive Bean Validation annotations
- **Better Error Handling**: Detailed validation error messages
- **Better Configuration**: Externalized configuration with profiles

### Key Differences
- **Database**: H2 instead of SQLite (easily configurable)
- **ORM**: JPA/Hibernate instead of SQLAlchemy
- **Validation**: Bean Validation instead of Pydantic
- **Documentation**: SpringDoc OpenAPI instead of FastAPI auto-docs

## 🚀 Deployment

### JAR Deployment
```bash
mvn clean package
java -jar target/todo-backend-1.0.0.jar
```

### Docker Deployment
```dockerfile
FROM openjdk:17-jre-slim
COPY target/todo-backend-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

## 🤝 Frontend Integration

The Java backend is 100% compatible with the existing React frontend. Simply:

1. Update the frontend API base URL to `http://localhost:8080/api/v1/todos`
2. No other changes required - all endpoints and data formats are identical

## 📝 Next Steps

1. **Database Migration**: Configure production database (PostgreSQL/MySQL)
2. **Security**: Add Spring Security for authentication/authorization
3. **Caching**: Implement Redis caching for better performance
4. **Monitoring**: Add Actuator endpoints for health checks and metrics
5. **Testing**: Expand unit and integration test coverage
6. **CI/CD**: Set up automated deployment pipeline

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8080 | xargs kill -9
```

**Build Fails**
```bash
# Clean Maven cache
mvn clean
rm -rf ~/.m2/repository/com/todoeveryday
mvn install
```

**H2 Console Access Issues**
- Ensure `spring.h2.console.enabled=true` in application.properties
- Use JDBC URL: `jdbc:h2:mem:todoeveryday`
- Username: `sa`, Password: (empty)

## 📞 Support

For issues or questions:
1. Check the application logs
2. Verify the API documentation at `/swagger-ui.html`
3. Test endpoints using the H2 console for database issues
4. Compare request/response format with the original Python backend

---

**Migration Complete! 🎉**

This Java Spring Boot backend provides identical functionality to the original Python FastAPI backend while offering improved performance, better tooling, and enterprise-grade features.
