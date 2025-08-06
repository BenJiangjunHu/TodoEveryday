package com.todoeveryday.repository;

import com.todoeveryday.model.Todo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface TodoRepository extends JpaRepository<Todo, Long> {
    
    // Find todos by completion status
    Page<Todo> findByIsCompletedOrderByCreatedAtDesc(Boolean isCompleted, Pageable pageable);
    
    // Find all todos ordered by creation date
    Page<Todo> findAllByOrderByCreatedAtDesc(Pageable pageable);
    
    // Count todos by completion status
    Long countByIsCompleted(Boolean isCompleted);
    
    // Find overdue todos
    @Query("SELECT COUNT(t) FROM Todo t WHERE t.isCompleted = false AND t.dueDate < :now")
    Long countOverdue(@Param("now") LocalDateTime now);
    
    // Batch operations
    @Modifying
    @Query("DELETE FROM Todo t WHERE t.isCompleted = true")
    int deleteAllCompleted();
    
    @Modifying
    @Query("UPDATE Todo t SET t.isCompleted = true, t.completedAt = :now WHERE t.isCompleted = false")
    int completeAll(@Param("now") LocalDateTime now);
    
    // Find by IDs
    List<Todo> findByIdIn(List<Long> ids);
}
