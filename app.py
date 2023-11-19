from flask import Flask, request, jsonify, render_template
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
        return jsonify({'result': result})
    except Exception as e:
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

        print(f"expr: {func_expression}, range_start: {range_start}, range_end: {range_end}, steps: {steps}")

        data_pairs = calc_service.calculate_graph(
            func_expression, range_start, range_end, steps)

        return jsonify(data_pairs)

    except ValueError as ve:
        print(f"Invalid input data: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error calculating graph: {str(e)}")
        return jsonify({"error": "An error occurred during processing"}), 500


@app.route('/graphpage')
def graph_page():
    return render_template('graph.html')


@app.route('/')
def index():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
