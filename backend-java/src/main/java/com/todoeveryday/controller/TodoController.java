package com.todoeveryday.controller;

import com.todoeveryday.dto.*;
import com.todoeveryday.service.TodoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/v1/todos")
@Tag(name = "Todo Management", description = "API for managing todo items")
public class TodoController {
    
    @Autowired
    private TodoService todoService;
    
    @GetMapping
    @Operation(summary = "Get todos", description = "Retrieve todos with filtering and pagination")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Successfully retrieved todos")
    })
    public ResponseEntity<TodoListResponse> getTodos(
            @Parameter(description = "Filter by status (all, completed, pending)")
            @RequestParam(defaultValue = "all") String status,
            @Parameter(description = "Page number (starts from 1)")
            @RequestParam(defaultValue = "1") int page,
            @Parameter(description = "Number of items per page")
            @RequestParam(defaultValue = "10") int limit) {
        
        FilterStatus filterStatus = FilterStatus.fromString(status);
        Page<TodoResponse> todoPage = todoService.getTodos(filterStatus, page, limit);
        
        TodoListResponse response = new TodoListResponse(
            true,
            todoPage.getContent(),
            (int) todoPage.getTotalElements(),
            page,
            limit
        );
        
        return ResponseEntity.ok(response);
    }
    
    @PostMapping
    @Operation(summary = "Create todo", description = "Create a new todo item")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "Todo created successfully"),
        @ApiResponse(responseCode = "400", description = "Invalid input")
    })
    public ResponseEntity<BaseResponse<TodoResponse>> createTodo(
            @Valid @RequestBody TodoCreateRequest request) {
        
        TodoResponse todo = todoService.createTodo(request);
        BaseResponse<TodoResponse> response = BaseResponse.success(todo);
        
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get todo", description = "Get a specific todo by ID")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Todo found"),
        @ApiResponse(responseCode = "404", description = "Todo not found")
    })
    public ResponseEntity<BaseResponse<TodoResponse>> getTodo(
            @Parameter(description = "Todo ID")
            @PathVariable Long id) {
        
        Optional<TodoResponse> todo = todoService.getTodoById(id);
        
        if (todo.isPresent()) {
            BaseResponse<TodoResponse> response = BaseResponse.success(todo.get());
            return ResponseEntity.ok(response);
        } else {
            BaseResponse<TodoResponse> response = BaseResponse.error("Todo not found");
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
        }
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "Update todo", description = "Update a specific todo")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Todo updated successfully"),
        @ApiResponse(responseCode = "404", description = "Todo not found"),
        @ApiResponse(responseCode = "400", description = "Invalid input")
    })
    public ResponseEntity<BaseResponse<TodoResponse>> updateTodo(
            @Parameter(description = "Todo ID")
            @PathVariable Long id,
            @Valid @RequestBody TodoUpdateRequest request) {
        
        Optional<TodoResponse> updatedTodo = todoService.updateTodo(id, request);
        
        if (updatedTodo.isPresent()) {
            BaseResponse<TodoResponse> response = BaseResponse.success(updatedTodo.get());
            return ResponseEntity.ok(response);
        } else {
            BaseResponse<TodoResponse> response = BaseResponse.error("Todo not found");
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
        }
    }
    
    @PatchMapping("/{id}/toggle")
    @Operation(summary = "Toggle todo", description = "Toggle completion status of a todo")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Todo toggled successfully"),
        @ApiResponse(responseCode = "404", description = "Todo not found")
    })
    public ResponseEntity<BaseResponse<TodoResponse>> toggleTodo(
            @Parameter(description = "Todo ID")
            @PathVariable Long id) {
        
        Optional<TodoResponse> toggledTodo = todoService.toggleTodo(id);
        
        if (toggledTodo.isPresent()) {
            BaseResponse<TodoResponse> response = BaseResponse.success(toggledTodo.get());
            return ResponseEntity.ok(response);
        } else {
            BaseResponse<TodoResponse> response = BaseResponse.error("Todo not found");
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
        }
    }
    
    @DeleteMapping("/{id}")
    @Operation(summary = "Delete todo", description = "Delete a specific todo")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Todo deleted successfully"),
        @ApiResponse(responseCode = "404", description = "Todo not found")
    })
    public ResponseEntity<BaseResponse<Void>> deleteTodo(
            @Parameter(description = "Todo ID")
            @PathVariable Long id) {
        
        boolean deleted = todoService.deleteTodo(id);
        
        if (deleted) {
            BaseResponse<Void> response = BaseResponse.success("Todo deleted successfully");
            return ResponseEntity.ok(response);
        } else {
            BaseResponse<Void> response = BaseResponse.error("Todo not found");
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
        }
    }
    
    @PostMapping("/batch")
    @Operation(summary = "Batch operations", description = "Perform batch operations on todos")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Batch operation completed"),
        @ApiResponse(responseCode = "400", description = "Invalid action")
    })
    public ResponseEntity<BaseResponse<Void>> batchOperation(
            @Valid @RequestBody BatchRequest request) {
        
        int count = 0;
        String message = "";
        
        try {
            switch (request.getAction()) {
                case DELETE_COMPLETED:
                    count = todoService.batchDeleteCompleted();
                    message = "Deleted " + count + " completed todos";
                    break;
                case DELETE_ALL:
                    count = todoService.batchDeleteAll();
                    message = "Deleted " + count + " todos";
                    break;
                case COMPLETE_ALL:
                    count = todoService.batchCompleteAll();
                    message = "Completed " + count + " todos";
                    break;
                default:
                    BaseResponse<Void> errorResponse = BaseResponse.error("Invalid action");
                    return ResponseEntity.badRequest().body(errorResponse);
            }
            
            BaseResponse<Void> response = BaseResponse.success(message);
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            BaseResponse<Void> errorResponse = BaseResponse.error("Error performing batch operation");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(errorResponse);
        }
    }
    
    @GetMapping("/stats")
    @Operation(summary = "Get statistics", description = "Get todo statistics")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Statistics retrieved successfully")
    })
    public ResponseEntity<BaseResponse<StatsResponse>> getStats() {
        StatsResponse stats = todoService.getStats();
        BaseResponse<StatsResponse> response = BaseResponse.success(stats);
        return ResponseEntity.ok(response);
    }
}
