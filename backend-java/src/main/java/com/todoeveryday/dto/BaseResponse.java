package com.todoeveryday.dto;

// Base response class
public class BaseResponse<T> {
    
    private Boolean success;
    private String message;
    private T data;
    
    // Constructors
    public BaseResponse() {}
    
    public BaseResponse(Boolean success) {
        this.success = success;
    }
    
    public BaseResponse(Boolean success, String message) {
        this.success = success;
        this.message = message;
    }
    
    public BaseResponse(Boolean success, T data) {
        this.success = success;
        this.data = data;
    }
    
    public BaseResponse(Boolean success, String message, T data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }
    
    // Static factory methods for common responses
    public static <T> BaseResponse<T> success(T data) {
        return new BaseResponse<>(true, data);
    }
    
    public static BaseResponse<Void> success(String message) {
        return new BaseResponse<>(true, message);
    }
    
    public static <T> BaseResponse<T> error(String message) {
        return new BaseResponse<>(false, message);
    }
    
    // Getters and Setters
    public Boolean getSuccess() {
        return success;
    }
    
    public void setSuccess(Boolean success) {
        this.success = success;
    }
    
    public String getMessage() {
        return message;
    }
    
    public void setMessage(String message) {
        this.message = message;
    }
    
    public T getData() {
        return data;
    }
    
    public void setData(T data) {
        this.data = data;
    }
}
