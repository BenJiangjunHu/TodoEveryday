package com.todoeveryday.dto;

public enum FilterStatus {
    ALL("all"),
    COMPLETED("completed"),
    PENDING("pending");
    
    private final String value;
    
    FilterStatus(String value) {
        this.value = value;
    }
    
    public String getValue() {
        return value;
    }
    
    public static FilterStatus fromString(String value) {
        for (FilterStatus status : FilterStatus.values()) {
            if (status.value.equalsIgnoreCase(value)) {
                return status;
            }
        }
        return ALL;
    }
}
