# Slightly Messy Todo App

A React todo application with some subtle code issues for demonstration purposes. This app contains a few minor code smells and inefficiencies that are commonly found in real-world projects.

## Setup Instructions

1. **Create a new directory** for your project:
   ```bash
   mkdir messy-todo-app
   cd messy-todo-app
   ```

2. **Copy all the provided files** into the appropriate directories:
   ```
   messy-todo-app/
   ├── package.json
   ├── README.md
   ├── public/
   │   └── index.html
   └── src/
       ├── index.js
       ├── index.css
       ├── App.js
       ├── App.css
       └── TodoApp.js
   ```

3. **Install dependencies**:
   ```bash
   npm install
   ```

4. **Start the development server**:
   ```bash
   npm start
   ```

5. **Open your browser** to `http://localhost:3000`

## Minor Code Issues Present

This app contains subtle issues for educational purposes:

### Minor Code Smells
- Using `Date.now()` for IDs (potential collision risk)
- Verbose delete function using manual loop instead of `filter()`
- Slightly redundant filtering logic
- Some repetitive filter count calculations

### Potential Improvements
- Could use `crypto.randomUUID()` for better ID generation
- Delete function could be simplified with `filter()`
- Filter logic could be more concise
- Could memoize filtered todos for better performance

## Purpose

This codebase is perfect for:
- Learning to identify minor code improvements
- Practice with simple refactoring
- Understanding the difference between working code and optimal code
- Teaching clean code principles without overwhelming complexity

## Notes

The app is fully functional and reasonably well-written, with just a few minor areas for improvement that represent common scenarios in real codebases.

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (not recommended)