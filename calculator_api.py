from flask import Flask, request, jsonify
from calc_logic.converter.postfix_var_expression_converter import PostfixExpressionConverter
from calc_logic.calculator.postfix_var_expression_calculator import ExpressionTree
from flask_cors import CORS
from calc_logic.service.calculator_service import CalculatorService

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

calc_service = CalculatorService()
    
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    print("request received...\n")
    try:
        expression = data['expression']
        result = calc_service.calculate_expression(expression)

        # Return the result as JSON
        return jsonify({'result': result})
    except Exception as e:
        # If there's an error, return it as JSON
        return jsonify({'error': str(e)})

@app.route('/graph', methods=['POST'])
def graph():
    try:
        # extract data from the request
        data = request.get_json()
        # validate input data
        if not all(key in data for key in ['funcExpression', 'rangeStart', 'rangeEnd', 'steps']):
            raise ValueError("Invalid input data")

        func_expression = data['funcExpression']
        range_start = data['rangeStart']
        range_end = data['rangeEnd']
        steps = data['steps']

        # validate steps
        if not isinstance(steps, int):
            raise ValueError("Steps must be an integer.")
        
        # call calculate_graph function
        data_pairs = calc_service.calculate_graph(func_expression, range_start, range_end, steps)
        return jsonify(data_pairs)
    
    except ValueError as ve:  # Catch ValueError for invalid input data
        print(f"Invalid input data: {str(ve)}")  # log the error
        return jsonify({"error": str(ve)}), 400  # return an error response with status code 400
    except Exception as e:  # Catch all other exceptions
        print(f"Error calculating graph: {str(e)}")  # log the error
        return jsonify({"error": "An error occurred during processing"}), 500  # return an error response with status code 500

# main thread
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Or whichever port you prefer
