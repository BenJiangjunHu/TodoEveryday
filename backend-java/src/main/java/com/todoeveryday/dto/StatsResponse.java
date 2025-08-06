package com.todoeveryday.dto;

public class StatsResponse {
    
    private Integer total;
    private Integer completed;
    private Integer pending;
    private Integer overdue;
    
    // Constructors
    public StatsResponse() {}
    
    public StatsResponse(Integer total, Integer completed, Integer pending, Integer overdue) {
        this.total = total;
        this.completed = completed;
        this.pending = pending;
        this.overdue = overdue;
    }
    
    // Getters and Setters
    public Integer getTotal() {
        return total;
    }
    
    public void setTotal(Integer total) {
        this.total = total;
    }
    
    public Integer getCompleted() {
        return completed;
    }
    
    public void setCompleted(Integer completed) {
        this.completed = completed;
    }
    
    public Integer getPending() {
        return pending;
    }
    
    public void setPending(Integer pending) {
        this.pending = pending;
    }
    
    public Integer getOverdue() {
        return overdue;
    }
    
    public void setOverdue(Integer overdue) {
        this.overdue = overdue;
    }
}
