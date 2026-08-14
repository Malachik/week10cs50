# iPhone Style Calculator

#### Video Demo: https://www.youtube.com/watch?v=YOUR_VIDEO_ID

#### Description:

My final project is a web-based iPhone-style calculator built using Python, Flask, JavaScript, HTML, CSS, and SQLite.

I chose to build a calculator because I wanted to create a project that was simple enough for me to understand while still allowing me to use several of the programming concepts I learned during CS50x. I already had some experience building static websites with HTML and CSS, so I wanted to use this project to learn more about connecting a website to Python and a database.

The calculator allows users to perform basic mathematical calculations including addition, subtraction, multiplication, division, and modulo. It also includes buttons for changing the sign of a number and calculating percentages.

The main additional feature of the project is the **calculation history**. Every successful calculation is saved in a SQLite database. The history records the expression, result, and date and time of the calculation. The most recent calculations are displayed first.

The user can also clear the entire calculation history using the Clear button.

## Main Features

### Calculator

The calculator supports:

- Addition
- Subtraction
- Multiplication
- Division
- Modulo
- Positive and negative numbers
- Percentages
- Decimal numbers

The calculator interface was designed to look similar to an iPhone calculator.

### Calculation History

One of the main features of the project is calculation history.

When a calculation is completed, the expression and result are stored in a SQLite database.

For example, if the user enters:

    25 * 4

the database stores the expression and result:

    Expression: 25 * 4
    Result: 100

The history also stores the date and time when the calculation was performed.

The history is displayed on the webpage with the newest calculations appearing first.

### Clear History

The calculator includes a Clear button that allows the user to delete all saved calculations from the database.

This sends a request to the Flask backend, which deletes the records from the SQLite database.

## Files

### app.py

`app.py` contains the main Python Flask application.

It creates the Flask application and contains the routes used by the calculator.

The `/` route loads the calculator page and retrieves the calculation history from the database.

The `/calculate` route receives a calculation from the frontend, calculates the result, saves it to the database, and sends the result back to the webpage.

The `/history` route retrieves the calculation history from the database and returns it as JSON.

The `/clear-history` route deletes all calculations from the database.

`app.py` also contains the functions used to connect to SQLite and create the database table.

### templates/index.html

`index.html` contains the calculator interface and calculation history section.

JavaScript is used to create the calculator buttons and handle user interaction.

When the user presses a calculator button, JavaScript updates the display.

When the equals button is pressed, JavaScript sends the calculation to the Flask `/calculate` route using a POST request.

The result returned by Flask is then displayed on the calculator.

The page also displays the calculation history.

### static/style.css

`style.css` controls the appearance of the calculator.

It contains the CSS used for the calculator layout, display, buttons, history section, spacing, fonts, and visual effects.

I designed the interface to be inspired by the iPhone calculator while creating my own layout and styling.

### calculator.db

`calculator.db` is the SQLite database used by the application.

The database contains a `calculations` table with:

- `id`
- `expression`
- `result`
- `created_at`

The database is created automatically when the application starts.

## Flask

Flask is used as the backend framework for the application.

The frontend communicates with Flask through different routes.

For example, when the user performs a calculation, JavaScript sends the expression to:

    /calculate

Flask receives the expression, processes it, saves the calculation to SQLite, and returns the result as JSON.

JavaScript then uses the returned result to update the calculator display.

This allowed me to learn how a frontend can communicate with a Python backend.

## SQLite Database

SQLite is used to store the calculation history.

I chose SQLite because it is lightweight and does not require a separate database server.

The application creates the database table automatically if it does not already exist.

The history is retrieved using SQL:

    SELECT id, expression, result, created_at
    FROM calculations
    ORDER BY id DESC

The results are ordered by ID so that the newest calculations appear first.

## Safe Calculations

One of the design decisions I made was not to use Python's `eval()` function to calculate user input.

Although `eval()` would make the calculator easier to build, it can execute arbitrary Python code. Since the calculator accepts input from the user, I wanted to avoid allowing arbitrary code to be executed.

Instead, I used Python's `ast` module to parse the mathematical expression.

The application only allows specific mathematical operators such as:

- Addition
- Subtraction
- Multiplication
- Division
- Modulo

The `evaluate_node()` function checks the different parts of the expression and makes sure that only approved operations are performed.

This was one of the more challenging parts of the project because it introduced me to concepts that I had not previously used, such as ASTs and recursion.

## JavaScript

JavaScript is responsible for making the calculator interactive.

The calculator buttons are created dynamically using JavaScript.

When a number or operator is pressed, it is added to the display.

When the equals button is pressed, JavaScript sends the expression to Flask using a POST request.

The returned JSON result is then displayed without requiring the entire webpage to reload.

JavaScript is also used to update the calculation history and handle the Clear History button.

## Design Decisions

I decided to build the project as a web application because I already had experience with HTML and CSS and wanted to improve my understanding of Python and backend development.

I chose Flask because it allowed me to connect Python with the HTML and JavaScript frontend without making the project unnecessarily complicated.

I chose SQLite because the application only needs to store a relatively small amount of information.

I added calculation history because I wanted the project to do more than simply perform calculations. It also gave me an opportunity to use SQL and persistent data storage.

I chose an iPhone-inspired design because I wanted the calculator to look like a real application rather than a basic programming exercise.

## What I Learned

This project helped me understand how the frontend and backend of a web application communicate.

I learned more about:

- Flask routes
- GET and POST requests
- JavaScript
- JSON
- SQLite
- SQL queries
- Database connections
- HTML and CSS
- Python functions
- Error handling
- AST parsing
- Recursion

I also learned more about debugging because I had to solve problems involving Flask, JavaScript, HTML, CSS, and SQLite.

One of the most useful things I learned was that a project can start as something simple and then become more useful by adding features such as persistent data and history.

## Future Improvements

If I continued developing the project, I could add additional features such as:

- Keyboard support
- Square root
- Powers
- Brackets
- More advanced mathematical operations
- User accounts
- Separate calculation histories for different users
- A dark and light mode
- Improved mobile support

## AI Assistance

I used ChatGPT as a programming assistant while developing this project.

I used it to help explain programming concepts, troubleshoot errors, understand Flask and Python code, and understand parts of the AST implementation.

I reviewed and tested the code myself and used the explanations to help me understand how the different parts of the application work.
