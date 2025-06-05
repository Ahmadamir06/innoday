import React, { useState, useEffect } from 'react';
import { Trash2, Plus, Check } from 'lucide-react';

// Minor code smell: global variable
let globalCounter = 0;

const TodoApp = () => {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [filter, setFilter] = useState('all');
  const [user, setUser] = useState(null);

  // Simulated user fetch (slightly overengineered for demo)
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await new Promise((resolve, reject) => {
          setTimeout(() => {
            if (Math.random() > 0.9) {
              reject('API Error');
            } else {
              resolve({ name: 'Demo User', id: 123 });
            }
          }, 500);
        });
        setUser(userData);
      } catch (error) {
        console.log('Error fetching user:', error);
        setUser({ name: 'Guest User', id: 0 });
      }
    };
    fetchUser();
  }, []);

  const addTodo = () => {
    globalCounter++; // Using global variable (minor code smell)
    
    if (inputValue.trim() === '') return;
    
    const newTodo = {
      id: Date.now(), // Using timestamp as ID (potential collision)
      text: inputValue,
      completed: false,
      createdAt: new Date(),
      priority: Math.random() > 0.5 ? 'high' : 'low', // Random priority
      count: globalCounter
    };
    
    setTodos([...todos, newTodo]);
    setInputValue('');
    
    // Side effect in component (minor code smell)
    document.title = `Todo App (${todos.length + 1} items)`;
  };

  // Slightly verbose filtering logic
  const getFilteredTodos = () => {
    let filtered = todos;
    if (filter === 'completed') {
      filtered = todos.filter(todo => todo.completed === true);
    } else if (filter === 'active') {
      filtered = todos.filter(todo => todo.completed !== true);
    } else if (filter === 'all') {
      filtered = todos;
    }
    return filtered;
  };

  const toggleTodo = (id) => {
    setTodos(todos.map(todo => {
      if (todo.id === id) {
        return { ...todo, completed: !todo.completed, lastModified: new Date() };
      } else {
        return todo;
      }
    }));
  };

  // Inefficient delete function (using loop instead of filter)
  const deleteTodo = (id) => {
    const newTodos = [];
    for (let i = 0; i < todos.length; i++) {
      if (todos[i].id !== id) {
        newTodos.push(todos[i]);
      }
    }
    setTodos(newTodos);
  };

  const filteredTodos = getFilteredTodos();

  return (
    <div className="container">
      <h1 className="header">
        {user ? `${user.name}'s` : 'Loading...'} Todo App
      </h1>
      <h2 className="header">
        DO innovation day
      </h2>
      
      <div className="input-section">
        <div className="input-group">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                addTodo();
              }
            }}
            placeholder="Add a new todo..."
            className="todo-input"
          />
          <button onClick={addTodo} className="add-btn">
            <Plus size={20} />
          </button>
        </div>

        <div className="filter-buttons">
          <button
            onClick={() => setFilter('all')}
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          >
            All ({todos.length})
          </button>
          <button
            onClick={() => setFilter('active')}
            className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
          >
            Active ({todos.filter(t => !t.completed).length})
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
          >
            Completed ({todos.filter(t => t.completed).length})
          </button>
        </div>
      </div>

      <div className="todos-list">
        {filteredTodos.length === 0 ? (
          <div className="empty-state">
            {filter === 'all' ? 'No todos yet!' : `No ${filter} todos!`}
          </div>
        ) : (
          filteredTodos.map((todo, index) => (
            <div
              key={todo.id}
              className={`todo-item ${todo.completed ? 'completed' : ''}`}
            >
              <div
                onClick={() => toggleTodo(todo.id)}
                className={`todo-checkbox ${todo.completed ? 'completed' : ''}`}
              >
                {todo.completed && <Check size={14} />}
              </div>
              
              <div style={{ flex: 1 }}>
                <span className={`todo-text ${todo.completed ? 'completed' : ''}`}>
                  {todo.text}
                </span>
                {/* Extra info display (slightly unnecessary) */}
                <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
                  #{todo.count} | Priority: {todo.priority} | 
                  Created: {todo.createdAt.toLocaleTimeString()}
                </div>
              </div>
              
              <button
                onClick={() => deleteTodo(todo.id)}
                className="delete-btn"
              >
                <Trash2 size={16} />
              </button>
            </div>
          ))
        )}
      </div>

      {/* Debug info (minor code smell - should be removed in production) */}
      <div style={{ 
        marginTop: '20px', 
        padding: '15px', 
        backgroundColor: '#fff3cd', 
        border: '1px solid #ffeaa7',
        borderRadius: '4px',
        fontSize: '14px'
      }}>
        <strong>Debug Info:</strong><br />
        Global Counter: {globalCounter}<br />
        Total Todos: {todos.length}<br />
        Filtered Todos: {filteredTodos.length}<br />
        Current Filter: {filter}
      </div>
    </div>
  );
};

export default TodoApp;