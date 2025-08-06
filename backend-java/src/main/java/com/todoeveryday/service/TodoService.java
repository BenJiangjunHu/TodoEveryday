package com.todoeveryday.service;

import com.todoeveryday.dto.*;
import com.todoeveryday.model.Todo;
import com.todoeveryday.repository.TodoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Transactional
public class TodoService {
    
    @Autowired
    private TodoRepository todoRepository;
    
    // Get todos with filtering and pagination
    @Transactional(readOnly = true)
    public Page<TodoResponse> getTodos(FilterStatus status, int page, int limit) {
        Pageable pageable = PageRequest.of(page - 1, limit);
        Page<Todo> todoPage;
        
        switch (status) {
            case COMPLETED:
                todoPage = todoRepository.findByIsCompletedOrderByCreatedAtDesc(true, pageable);
                break;
            case PENDING:
                todoPage = todoRepository.findByIsCompletedOrderByCreatedAtDesc(false, pageable);
                break;
            default:
                todoPage = todoRepository.findAllByOrderByCreatedAtDesc(pageable);
                break;
        }
        
        return todoPage.map(this::convertToResponse);
    }
    
    // Create new todo
    public TodoResponse createTodo(TodoCreateRequest request) {
        Todo todo = new Todo();
        todo.setTitle(request.getTitle());
        todo.setDescription(request.getDescription());
        todo.setPriority(request.getPriority() != null ? request.getPriority() : 1);
        todo.setDueDate(request.getDueDate());
        
        Todo savedTodo = todoRepository.save(todo);
        return convertToResponse(savedTodo);
    }
    
    // Get single todo by ID
    @Transactional(readOnly = true)
    public Optional<TodoResponse> getTodoById(Long id) {
        return todoRepository.findById(id)
                .map(this::convertToResponse);
    }
    
    // Update todo
    public Optional<TodoResponse> updateTodo(Long id, TodoUpdateRequest request) {
        return todoRepository.findById(id)
                .map(todo -> {
                    if (request.getTitle() != null) {
                        todo.setTitle(request.getTitle());
                    }
                    if (request.getDescription() != null) {
                        todo.setDescription(request.getDescription());
                    }
                    if (request.getIsCompleted() != null) {
                        todo.setIsCompleted(request.getIsCompleted());
                    }
                    if (request.getPriority() != null) {
                        todo.setPriority(request.getPriority());
                    }
                    if (request.getDueDate() != null) {
                        todo.setDueDate(request.getDueDate());
                    }
                    
                    Todo updatedTodo = todoRepository.save(todo);
                    return convertToResponse(updatedTodo);
                });
    }
    
    // Toggle todo completion status
    public Optional<TodoResponse> toggleTodo(Long id) {
        return todoRepository.findById(id)
                .map(todo -> {
                    todo.setIsCompleted(!todo.getIsCompleted());
                    Todo updatedTodo = todoRepository.save(todo);
                    return convertToResponse(updatedTodo);
                });
    }
    
    // Delete todo
    public boolean deleteTodo(Long id) {
        if (todoRepository.existsById(id)) {
            todoRepository.deleteById(id);
            return true;
        }
        return false;
    }
    
    // Batch operations
    public int batchDeleteCompleted() {
        return todoRepository.deleteAllCompleted();
    }
    
    public int batchDeleteAll() {
        int count = (int) todoRepository.count();
        todoRepository.deleteAll();
        return count;
    }
    
    public int batchCompleteAll() {
        return todoRepository.completeAll(LocalDateTime.now());
    }
    
    // Get statistics
    @Transactional(readOnly = true)
    public StatsResponse getStats() {
        Long total = todoRepository.count();
        Long completed = todoRepository.countByIsCompleted(true);
        Long pending = total - completed;
        Long overdue = todoRepository.countOverdue(LocalDateTime.now());
        
        return new StatsResponse(
                total.intValue(),
                completed.intValue(),
                pending.intValue(),
                overdue.intValue()
        );
    }
    
    // Convert entity to response DTO
    private TodoResponse convertToResponse(Todo todo) {
        return new TodoResponse(
                todo.getId(),
                todo.getTitle(),
                todo.getDescription(),
                todo.getIsCompleted(),
                todo.getPriority(),
                todo.getCreatedAt(),
                todo.getUpdatedAt(),
                todo.getCompletedAt(),
                todo.getDueDate()
        );
    }
}
