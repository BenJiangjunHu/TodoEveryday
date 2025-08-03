import React from 'react';

const TodoFilter = ({ currentFilter, onFilterChange, stats }) => {
  const filters = [
    { key: 'all', label: '全部', count: stats?.total || 0 },
    { key: 'pending', label: '未完成', count: stats?.pending || 0 },
    { key: 'completed', label: '已完成', count: stats?.completed || 0 }
  ];

  return (
    <div className="card">
      <h3 className="mb-3">筛选任务</h3>
      <div className="filter-buttons">
        {filters.map((filter) => (
          <button
            key={filter.key}
            className={`btn btn-outline ${currentFilter === filter.key ? 'active' : ''}`}
            onClick={() => onFilterChange(filter.key)}
          >
            {filter.label}
            <span className="count-badge">
              {filter.count}
            </span>
          </button>
        ))}
      </div>
      
      {stats && (
        <div className="stats-summary mt-3">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">{stats.total}</div>
              <div className="stat-label">总任务</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{stats.completed}</div>
              <div className="stat-label">已完成</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{stats.pending}</div>
              <div className="stat-label">待完成</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{stats.overdue}</div>
              <div className="stat-label">已过期</div>
            </div>
          </div>
          
          {stats.total > 0 && (
            <div className="progress-bar mt-3">
              <div className="progress-label">
                完成进度: {Math.round((stats.completed / stats.total) * 100)}%
              </div>
              <div className="progress-track">
                <div 
                  className="progress-fill"
                  style={{ width: `${(stats.completed / stats.total) * 100}%` }}
                ></div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TodoFilter;
