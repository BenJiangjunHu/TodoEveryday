// DOM Elements
const searchAddInput = document.getElementById('search-add-input');
const searchDropdown = document.getElementById('search-dropdown');
const tasksList = document.getElementById('tasks-list');
const taskModal = document.getElementById('task-modal');
const closeModal = document.querySelector('.close-modal');
const taskForm = document.getElementById('task-form');
const taskNameInput = document.getElementById('task-name');
const taskStatusSelect = document.getElementById('task-status');
const taskDeadlineInput = document.getElementById('task-deadline');
const taskFinishedInput = document.getElementById('task-finished');
const taskDescriptionInput = document.getElementById('task-description');
const taskCreatedDate = document.getElementById('task-created-date');
const taskUpdatedDate = document.getElementById('task-updated-date');
const saveTaskBtn = document.getElementById('save-task');
const deleteTaskBtn = document.getElementById('delete-task');
const copyTaskBtn = document.getElementById('copy-task');
const filterBtns = document.querySelectorAll('.filter-btn');

// App State
let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
let currentFilter = 'all';
let editingTaskId = null;

// Initialize App
function init() {
    renderTasks();
    addEventListeners();
}

// Event Listeners
function addEventListeners() {
    // Search/Add input
    searchAddInput.addEventListener('keyup', (e) => {
        const query = searchAddInput.value.trim();
        
        if (e.key === 'Enter' && query !== '') {
            handleEnterKeyInSearch();
        } else {
            updateSearchDropdown(query);
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
            hideDropdown();
        }
    });
    
    // Focus on search input
    searchAddInput.addEventListener('focus', () => {
        const query = searchAddInput.value.trim();
        if (query) {
            updateSearchDropdown(query);
        }
    });

    // Close modal
    closeModal.addEventListener('click', closeTaskModal);
    window.addEventListener('click', (e) => {
        if (e.target === taskModal) {
            closeTaskModal();
        }
    });

    // Task form submission
    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        saveTask();
    });

    // Delete task
    deleteTaskBtn.addEventListener('click', deleteTask);

    // Copy task
    copyTaskBtn.addEventListener('click', copyTask);

    // Task status change
    taskStatusSelect.addEventListener('change', () => {
        if (taskStatusSelect.value === 'completed') {
            taskFinishedInput.value = formatDate(new Date());
            taskFinishedInput.disabled = false;
        } else {
            taskFinishedInput.value = '';
            taskFinishedInput.disabled = true;
        }
    });

    // Filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderTasks();
        });
    });
}

// Handle dropdown functionality
function updateSearchDropdown(query) {
    if (!query) {
        hideDropdown();
        return;
    }
    
    // Find matching tasks
    const matchingTasks = tasks.filter(task => 
        task.name.toLowerCase().includes(query.toLowerCase()) || 
        (task.description && task.description.toLowerCase().includes(query.toLowerCase()))
    ).slice(0, 5); // Limit to 5 results
    
    // Clear previous dropdown content
    searchDropdown.innerHTML = '';
    
    // Add matching tasks to dropdown
    matchingTasks.forEach(task => {
        const item = document.createElement('div');
        item.className = 'dropdown-item';
        item.dataset.id = task.id;
        
        const deadlineText = task.deadline ? 
            `Deadline: ${formatDateDisplay(task.deadline)}` : 'No deadline';
        const createdText = `Created: ${formatDateDisplay(new Date(task.createdAt))}`;
        
        item.innerHTML = `
            <div class="task-match-name">${highlightMatch(task.name, query)}</div>
            <div class="task-match-info">${deadlineText} • Status: ${task.status}</div>
            <div class="task-match-date">${createdText}</div>
        `;
        
        item.addEventListener('click', () => {
            openEditTaskModal(task.id);
            hideDropdown();
        });
        
        searchDropdown.appendChild(item);
    });
    
    // Add "Create new task" option if no exact match
    const exactMatch = matchingTasks.some(t => t.name.toLowerCase() === query.toLowerCase());
    if (!exactMatch) {
        const createItem = document.createElement('div');
        createItem.className = 'dropdown-item create-new';
        createItem.innerHTML = `<i>Create new task: "${query}"</i>`;
        
        createItem.addEventListener('click', () => {
            openNewTaskModal(query);
            hideDropdown();
        });
        
        searchDropdown.appendChild(createItem);
    }
    
    // Show dropdown if there are items
    if (searchDropdown.children.length > 0) {
        showDropdown();
    } else {
        hideDropdown();
    }
}

// Show dropdown
function showDropdown() {
    searchDropdown.classList.add('active');
}

// Hide dropdown
function hideDropdown() {
    searchDropdown.classList.remove('active');
}

// Highlight matching text
function highlightMatch(text, query) {
    if (!query) return text;
    
    const regex = new RegExp('(' + escapeRegExp(query) + ')', 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// Escape special characters for regex
function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Handle Enter key in search input
function handleEnterKeyInSearch() {
    const query = searchAddInput.value.trim();
    
    // If dropdown is visible and has items, select the first item
    if (searchDropdown.classList.contains('active') && searchDropdown.children.length > 0) {
        const firstItem = searchDropdown.children[0];
        
        if (firstItem.classList.contains('create-new')) {
            openNewTaskModal(query);
        } else {
            openEditTaskModal(firstItem.dataset.id);
        }
        
        hideDropdown();
    } else {
        // Fallback to old behavior
        openNewTaskModal(query);
    }
    
    searchAddInput.value = '';
}

// Open task modal for creating a new task
function openNewTaskModal(taskName = '') {
    editingTaskId = null;
    taskForm.reset();
    taskNameInput.value = taskName;
    taskStatusSelect.value = 'active';
    taskDeadlineInput.value = '';
    taskFinishedInput.value = '';
    taskFinishedInput.disabled = true;
    
    // Set created and updated dates to current
    const currentDate = formatDateTimeDisplay(new Date());
    taskCreatedDate.textContent = currentDate;
    taskUpdatedDate.textContent = currentDate;
    
    taskModal.style.display = 'block';
    taskNameInput.focus();
    searchAddInput.value = '';
}

// Open task modal for editing an existing task
function openEditTaskModal(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;

    editingTaskId = taskId;
    taskNameInput.value = task.name;
    taskStatusSelect.value = task.status;
    taskDeadlineInput.value = task.deadline || '';
    taskFinishedInput.value = task.finishedDate || '';
    taskFinishedInput.disabled = task.status !== 'completed';
    taskDescriptionInput.value = task.description || '';
    
    // Display created and updated dates
    taskCreatedDate.textContent = formatDateTimeDisplay(new Date(task.createdAt));
    taskUpdatedDate.textContent = formatDateTimeDisplay(new Date(task.updatedAt));
    
    taskModal.style.display = 'block';
}

// Close the task modal
function closeTaskModal() {
    taskModal.style.display = 'none';
    editingTaskId = null;
}

// Save a task (create new or update existing)
function saveTask() {
    const taskName = taskNameInput.value.trim();
    const taskStatus = taskStatusSelect.value;
    const taskDeadline = taskDeadlineInput.value;
    const taskFinished = taskFinishedInput.value;
    const taskDescription = taskDescriptionInput.value.trim();

    if (taskName === '') return;

    if (editingTaskId) {
        // Update existing task
        const taskIndex = tasks.findIndex(t => t.id === editingTaskId);
        if (taskIndex !== -1) {
            tasks[taskIndex] = {
                ...tasks[taskIndex],
                name: taskName,
                status: taskStatus,
                deadline: taskDeadline,
                finishedDate: taskStatus === 'completed' ? (taskFinished || formatDate(new Date())) : '',
                description: taskDescription,
                updatedAt: new Date().toISOString()
            };
        }
    } else {
        // Create new task
        const newTask = {
            id: generateId(),
            name: taskName,
            status: taskStatus,
            deadline: taskDeadline,
            finishedDate: taskStatus === 'completed' ? formatDate(new Date()) : '',
            description: taskDescription,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        tasks.unshift(newTask);
    }

    saveTasks();
    closeTaskModal();
    renderTasks();
}

// Delete the current task
function deleteTask() {
    if (!editingTaskId) return;
    
    tasks = tasks.filter(task => task.id !== editingTaskId);
    saveTasks();
    closeTaskModal();
    renderTasks();
}

// Copy the current task
function copyTask() {
    if (!editingTaskId) return;
    
    const originalTask = tasks.find(task => task.id === editingTaskId);
    if (!originalTask) return;
    
    const copiedTask = {
        ...originalTask,
        id: generateId(),
        name: `${originalTask.name} (Copy)`,
        status: 'active',
        deadline: '',
        finishedDate: '',
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    };
    
    tasks.unshift(copiedTask);
    saveTasks();
    closeTaskModal();
    renderTasks();
}

// Search tasks
function searchTasks(query) {
    if (!query.trim()) {
        renderTasks();
        hideDropdown();
        return;
    }
    
    const filteredTasks = tasks.filter(task => 
        task.name.toLowerCase().includes(query.toLowerCase()) || 
        (task.description && task.description.toLowerCase().includes(query.toLowerCase()))
    );
    
    renderTasksList(filteredTasks);
    
    // Also update the dropdown
    updateSearchDropdown(query);
}

// Render tasks based on current filter
function renderTasks() {
    let filteredTasks;
    
    switch (currentFilter) {
        case 'active':
            filteredTasks = tasks.filter(task => task.status === 'active');
            break;
        case 'completed':
            filteredTasks = tasks.filter(task => task.status === 'completed');
            break;
        default:
            filteredTasks = tasks;
    }
    
    renderTasksList(filteredTasks);
}

// Render the tasks list to the DOM
function renderTasksList(tasksList) {
    const tasksContainer = document.getElementById('tasks-list');
    tasksContainer.innerHTML = '';
    
    if (tasksList.length === 0) {
        tasksContainer.innerHTML = `
            <div class="empty-state">
                <p>No tasks found</p>
            </div>
        `;
        return;
    }
    
    tasksList.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.className = `task-item ${task.status === 'completed' ? 'completed' : ''}`;
        
        const deadlineText = task.deadline ? `Deadline: ${formatDateDisplay(task.deadline)}` : 'No deadline';
        const finishedText = task.finishedDate ? `Finished: ${formatDateDisplay(task.finishedDate)}` : '';
        const createdText = `Created: ${formatDateDisplay(new Date(task.createdAt))}`;
        const updatedText = `Updated: ${formatDateDisplay(new Date(task.updatedAt))}`;
        
        taskElement.innerHTML = `
            <div class="task-details" data-id="${task.id}">
                <div class="task-name">${task.name}</div>
                <div class="task-info">
                    <span>${deadlineText}</span>
                    ${finishedText ? `<span>${finishedText}</span>` : ''}
                </div>
                <div class="task-lifecycle">
                    <span>${createdText}</span>
                    <span>${updatedText}</span>
                </div>
            </div>
            <div class="task-actions">
                <button class="complete-btn" data-id="${task.id}" title="${task.status === 'completed' ? 'Mark as active' : 'Mark as completed'}">
                    ${task.status === 'completed' ? '↩' : '✓'}
                </button>
                <button class="delete-btn" data-id="${task.id}" title="Delete">🗑</button>
            </div>
        `;
        
        tasksContainer.appendChild(taskElement);
        
        // Add event listener to open task details
        taskElement.querySelector('.task-details').addEventListener('click', () => {
            openEditTaskModal(task.id);
        });
        
        // Add event listener to toggle task status
        taskElement.querySelector('.complete-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            toggleTaskStatus(task.id);
        });
        
        // Add event listener to delete task
        taskElement.querySelector('.delete-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            deleteTaskById(task.id);
        });
    });
}

// Toggle task status (active/completed)
function toggleTaskStatus(taskId) {
    const taskIndex = tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) return;
    
    const newStatus = tasks[taskIndex].status === 'completed' ? 'active' : 'completed';
    tasks[taskIndex].status = newStatus;
    
    if (newStatus === 'completed') {
        tasks[taskIndex].finishedDate = formatDate(new Date());
    } else {
        tasks[taskIndex].finishedDate = '';
    }
    
    // Update the updatedAt timestamp
    tasks[taskIndex].updatedAt = new Date().toISOString();
    
    saveTasks();
    renderTasks();
}

// Delete task by ID
function deleteTaskById(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        tasks = tasks.filter(task => task.id !== taskId);
        saveTasks();
        renderTasks();
    }
}

// Save tasks to localStorage
function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Helper function to generate a unique ID
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Format date to YYYY-MM-DD for input fields
function formatDate(date) {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Format date for display
function formatDateDisplay(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Format date and time for display
function formatDateTimeDisplay(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit', 
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleString(undefined, options);
}

// Initialize the app
init();
