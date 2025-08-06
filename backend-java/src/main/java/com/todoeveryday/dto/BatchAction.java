package com.todoeveryday.dto;

public enum BatchAction {
    DELETE_COMPLETED("delete_completed"),
    DELETE_ALL("delete_all"),
    COMPLETE_ALL("complete_all");
    
    private final String value;
    
    BatchAction(String value) {
        this.value = value;
    }
    
    public String getValue() {
        return value;
    }
    
    public static BatchAction fromString(String value) {
        for (BatchAction action : BatchAction.values()) {
            if (action.value.equalsIgnoreCase(value)) {
                return action;
            }
        }
        throw new IllegalArgumentException("Invalid batch action: " + value);
    }
}
