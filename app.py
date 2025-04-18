from flask import Flask, request, jsonify
from itertools import permutations

app = Flask(__name__)

# Product data with weight and source
product_data = {
    'A': {'weight': 3, 'center': 'C1'},
    'B': {'weight': 2, 'center': 'C1'},
    'C': {'weight': 8, 'center': 'C2'},
    'D': {'weight': 12, 'center': 'C2'},
    'E': {'weight': 25, 'center': 'C2'},
    'F': {'weight': 1.5, 'center': 'C3'},
    'G': {'weight': 0.5, 'center': 'C3'},
    'H': {'weight': 1, 'center': 'C3'},
    'I': {'weight': 2, 'center': 'C3'}
}

# Distance between centers and L1
distances = {
    ('C1', 'L1'): 4,
    ('C2', 'L1'): 2.5,
    ('C3', 'L1'): 3,
    ('C1', 'C2'): 3,
    ('C2', 'C3'): 2,
    ('C3', 'C1'): 2,
}

def calculate_cost(path, total_weight):
    total_distance = 0
    for i in range(len(path) - 1):
        d = distances.get((path[i], path[i+1]), distances.get((path[i+1], path[i]), 0))
        total_distance += d

    if total_weight <= 5:
        cost_per_km = 10
    else:
        cost_per_km = (5 * 10 + (total_weight - 5) * 8) / total_weight

    return round(total_weight * cost_per_km * total_distance / total_weight)

@app.route('/api/calculate-cost', methods=['POST'])
def calculate_delivery_cost():
    order = request.json
    centers_needed = set()
    total_weight = 0

    for product, quantity in order.items():
        if product in product_data:
            info = product_data[product]
            centers_needed.add(info['center'])
            total_weight += info['weight'] * quantity

    center_list = list(centers_needed)
    min_cost = float('inf')

    for perm in permutations(center_list):
        path = list(perm) + ['L1']
        cost = calculate_cost(path, total_weight)
        if cost < min_cost:
            min_cost = cost

    return jsonify({'minimum_cost': round(min_cost)})

if __name__ == '__main__':
    app.run(debug=True)
