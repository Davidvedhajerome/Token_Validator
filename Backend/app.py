from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/tokenDB'
mongo = PyMongo(app)
CORS(app)

# Define the collection
token_collection = mongo.db.tokens

@app.route('/add-token', methods=['POST'])
def add_token():
    data = request.json
    token_number = data.get('tokenNumber')

    if not token_number:
        return jsonify({"message": "Token number is required"}), 400

    if '-' in token_number:
        try:
            start, end = map(int, token_number.replace(" ", "").split('-'))
            if start > end:
                return jsonify({"message": "Invalid range: start cannot be greater than end"}), 400

            tokens_to_add = [{'tokenNumber': str(i)} for i in range(start, end + 1)]
            existing_tokens = token_collection.find({"tokenNumber": {"$in": [str(i) for i in range(start, end + 1)]}})
            existing_tokens_list = [token['tokenNumber'] for token in existing_tokens]
            new_tokens = [token for token in tokens_to_add if token['tokenNumber'] not in existing_tokens_list]
            if new_tokens:
                token_collection.insert_many(new_tokens)
                return jsonify({"message": f"{len(new_tokens)} tokens added successfully"}), 201
            else:
                return jsonify({"message": "All tokens in range already exist"}), 400
        except ValueError:
            return jsonify({"message": "Invalid range format"}), 400
    else:
        if token_collection.find_one({'tokenNumber': token_number}):
            return jsonify({"message": "Token already exists"}), 400
        token_collection.insert_one({'tokenNumber': token_number})
        return jsonify({"message": "Token added successfully"}), 201

# Updated route to validate a token or a range of tokens
@app.route('/validate-token', methods=['POST'])
def validate_token():
    data = request.json
    token_number = data.get('tokenNumber')

    if not token_number:
        return jsonify({"message": "Token number is required for validation"}), 400

    valid_tokens = []
    invalid_tokens = []

    if '-' in token_number:
        try:
            start, end = map(int, token_number.replace(" ", "").split('-'))
            if start > end:
                return jsonify({"message": "Invalid range: start cannot be greater than end"}), 400

            for i in range(start, end + 1):
                token = str(i)
                if token_collection.find_one({"tokenNumber": token}):
                    valid_tokens.append(token)
                else:
                    invalid_tokens.append(token)

            return jsonify({
                "message": "Validation complete",
                "valid_tokens": valid_tokens,
                "invalid_tokens": invalid_tokens
            }), 200

        except ValueError:
            return jsonify({"message": "Invalid range format"}), 400
    else:
        if token_collection.find_one({"tokenNumber": token_number}):
            return jsonify({"message": "Token is valid"}), 200
        else:
            return jsonify({"message": "Token is invalid"}), 404

if __name__ == '__main__':
    app.run(debug=True)

