package com.todoeveryday.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

/**
 * Root controller for basic application endpoints.
 * Equivalent to the Python FastAPI root endpoints.
 */
@RestController
@CrossOrigin(origins = {"http://localhost:3000", "http://127.0.0.1:3000"})
@Tag(name = "Application", description = "Basic application endpoints")
public class RootController {

    /**
     * Root endpoint
     * Equivalent to Python GET /
     */
    @GetMapping("/")
    @Operation(
        summary = "Application info",
        description = "Get basic application information"
    )
    @ApiResponse(responseCode = "200", description = "Application information")
    public ResponseEntity<Map<String, Object>> root() {
        Map<String, Object> response = new HashMap<>();
        response.put("message", "TodoEveryday API");
        response.put("version", "1.0.0");
        response.put("docs", "/swagger-ui.html");
        return ResponseEntity.ok(response);
    }

    /**
     * Health check endpoint
     * Equivalent to Python GET /health
     */
    @GetMapping("/health")
    @Operation(
        summary = "Health check",
        description = "Check if the application is running"
    )
    @ApiResponse(responseCode = "200", description = "Application is healthy")
    public ResponseEntity<Map<String, String>> healthCheck() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "healthy");
        return ResponseEntity.ok(response);
    }
}
