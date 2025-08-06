package com.todoeveryday.dto;

import java.util.List;

public class BatchRequest {
    
    private BatchAction action;
    private List<Long> todoIds;
    
    // Constructors
    public BatchRequest() {}
    
    public BatchRequest(BatchAction action, List<Long> todoIds) {
        this.action = action;
        this.todoIds = todoIds;
    }
    
    // Getters and Setters
    public BatchAction getAction() {
        return action;
    }
    
    public void setAction(BatchAction action) {
        this.action = action;
    }
    
    public List<Long> getTodoIds() {
        return todoIds;
    }
    
    public void setTodoIds(List<Long> todoIds) {
        this.todoIds = todoIds;
    }
}
