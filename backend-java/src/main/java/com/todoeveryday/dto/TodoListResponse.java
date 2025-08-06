package com.todoeveryday.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;

/**
 * Paginated response for todo lists
 */
@Data
@NoArgsConstructor
public class TodoListResponse {
    private boolean success;
    private String message;
    private List<TodoResponse> data;
    private Integer total;
    private Integer page;
    private Integer limit;
    
    public TodoListResponse(boolean success, String message, List<TodoResponse> data, Integer total, Integer page, Integer limit) {
        this.success = success;
        this.message = message;
        this.data = data;
        this.total = total;
        this.page = page;
        this.limit = limit;
    }
    
    public TodoListResponse(boolean success, List<TodoResponse> data, Integer total, Integer page, Integer limit) {
        this.success = success;
        this.data = data;
        this.total = total;
        this.page = page;
        this.limit = limit;
    }
    
    public static TodoListResponse success(List<TodoResponse> data, Integer total, Integer page, Integer limit) {
        return new TodoListResponse(true, "Success", data, total, page, limit);
    }
    
    public static TodoListResponse error(String message) {
        return new TodoListResponse(false, message, null, null, null, null);
    }
}
