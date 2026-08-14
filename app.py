
from flask import Flask, render_template, request, jsonify
import sqlite3
# CHAT GPT used to confirm 
import ast
import operator
from datetime import datetime

app = Flask(__name__)

DATABASE = "calculator.db"


# Abstract Syntax Tree , dictionary that tells the calculator which mathematical operations are allowed and which Python function to use for each one.
# These are the maths operations my calculator allows
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}


# Connect to the database
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# Create the database table
def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Work out the calculation from the AST
def evaluate_node(node):

    # This is the main Abstract Syntax Tree section Check if the value is a number , very difficult CHAT GPT used to debug
    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value

        raise ValueError("Invalid number")

    # Check if the calculation has two parts evaluate_node() goes through the expression piece by piece,
    #  checks that the numbers and mathematical operators are allowed, 
    # handles positive and negative numbers, and then performs the calculation using the approved operator.
    if isinstance(node, ast.BinOp):

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Operator not allowed")

        left = evaluate_node(node.left)
        right = evaluate_node(node.right)

        return operation(left, right)

    # Handle positive and negative numbers The function uses recursion because a mathematical expression can contain smaller expressions inside it. node.left represents the left side and node.right represents the right side. The function calls itself on both sides to work out their values. It keeps doing this until it reaches individual numbers, then works its way back up and combines the results using the correct operator.s
    if isinstance(node, ast.UnaryOp):

        if isinstance(node.op, ast.USub):
            return -evaluate_node(node.operand)

        if isinstance(node.op, ast.UAdd):
            return evaluate_node(node.operand)

    raise ValueError("Invalid expression")


# Calculate the expression without using eval()
def safe_calculate(expression):

    if len(expression) > 100:
        raise ValueError("Expression is too long")

    try:
        tree = ast.parse(expression, mode="eval")

        return evaluate_node(tree.body)

    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")

    except (SyntaxError, TypeError, ValueError):
        raise ValueError("Invalid expression")


# Home page
@app.route("/")
def index():

    connection = get_db_connection()

    history = connection.execute("""
        SELECT id, expression, result, created_at
        FROM calculations
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template("index.html", history=history)


# Calculate a number and save it to the database
@app.route("/calculate", methods=["POST"])
def calculate():

    expression = request.form.get("expression", "").strip()

    # Check that something was entered
    if not expression:
        return jsonify({"error": "Please enter a calculation."}), 400

    try:

        # Calculate the expression
        result = safe_calculate(expression)

        # Change 5.0 into 5
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        result = str(result)

        # Connect to database
        connection = get_db_connection()

        # Save the calculation
        connection.execute("""
            INSERT INTO calculations
            (expression, result, created_at)
            VALUES (?, ?, ?)
        """, (
            expression,
            result,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        connection.commit()
        connection.close()

        # Send the result back to JavaScript
        return jsonify({
            "result": result,
            "expression": expression
        })

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 400


# Get the calculation history
@app.route("/history", methods=["GET"])
def history():

    connection = get_db_connection()

    calculations = connection.execute("""
        SELECT id, expression, result, created_at
        FROM calculations
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    # Turn the database results into JSON
    return jsonify([
        {
            "id": calculation["id"],
            "expression": calculation["expression"],
            "result": calculation["result"],
            "created_at": calculation["created_at"]
        }
        for calculation in calculations
    ])


# Delete all the calculation history
@app.route("/clear-history", methods=["POST"])
def clear_history():

    connection = get_db_connection()

    connection.execute("DELETE FROM calculations")

    connection.commit()
    connection.close()

    return jsonify({"success": True})


# Start the application
if __name__ == "__main__":

    initialize_database()

    app.run(debug=True)