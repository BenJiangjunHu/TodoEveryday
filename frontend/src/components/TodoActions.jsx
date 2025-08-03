import React from 'react';

const TodoActions = ({ onClearCompleted, onClearAll, stats, loading }) => {
  const hasCompleted = stats?.completed > 0;
  const hasAny = stats?.total > 0;

  const handleClearCompleted = async () => {
    if (!hasCompleted) return;
    
    if (window.confirm(`确定要清除所有已完成的任务吗？（共${stats.completed}个）`)) {
      try {
        await onClearCompleted();
      } catch (error) {
        console.error('清除已完成任务失败:', error);
        alert('操作失败，请重试');
      }
    }
  };

  const handleClearAll = async () => {
    if (!hasAny) return;
    
    if (window.confirm(`确定要清除所有任务吗？（共${stats.total}个）\n此操作不可恢复！`)) {
      try {
        await onClearAll();
      } catch (error) {
        console.error('清除所有任务失败:', error);
        alert('操作失败，请重试');
      }
    }
  };

  return (
    <div className="card">
      <h3 className="mb-3">批量操作</h3>
      <div className="action-buttons">
        <button
          className="btn btn-danger"
          onClick={handleClearCompleted}
          disabled={!hasCompleted || loading}
          title={hasCompleted ? `清除${stats.completed}个已完成任务` : '没有已完成的任务'}
        >
          {loading ? (
            <>
              <span className="spinner" style={{ width: '16px', height: '16px', marginRight: '8px' }}></span>
              清除中...
            </>
          ) : (
            <>
              🗑️ 清除已完成 {hasCompleted ? `(${stats.completed})` : ''}
            </>
          )}
        </button>
        
        <button
          className="btn btn-danger"
          onClick={handleClearAll}
          disabled={!hasAny || loading}
          title={hasAny ? `清除所有${stats.total}个任务` : '没有任务'}
        >
          {loading ? (
            <>
              <span className="spinner" style={{ width: '16px', height: '16px', marginRight: '8px' }}></span>
              清除中...
            </>
          ) : (
            <>
              💥 清除全部 {hasAny ? `(${stats.total})` : ''}
            </>
          )}
        </button>
      </div>
      
      {hasAny && (
        <div className="action-info mt-3">
          <p className="text-muted">
            💡 提示：清除操作将永久删除任务，请谨慎操作
          </p>
        </div>
      )}
    </div>
  );
};

export default TodoActions;
