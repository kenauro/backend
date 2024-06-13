from flask import Flask, jsonify, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the model from the local file
with open("newprop_model2.pkl", "rb") as file:
    model = pickle.load(file)

with open("model_knn.pkl", "rb") as file2:
    model_knn = pickle.load(file2)

with open("model_adaboost.pkl", "rb") as file3:
    model_adaboost = pickle.load(file3)

with open("model_bagging.pkl", "rb") as file4:
    model_bagging = pickle.load(file4)

with open("model_dt.pkl", "rb") as file5:
    model_dt = pickle.load(file5)
    
with open("model_hgb.pkl", "rb") as file6:
    model_hgb = pickle.load(file6)

with open("meta_model.pkl", "rb") as file7:
    meta_model = pickle.load(file7)





@app.route("/")
def hello_world():
    return jsonify(
        {"status": True, "code": 200, "message": "OK", "data": "Hello, World!"}
    )

@app.route("/predict2",methods=["POST"])
def predict2():


    
    data_baru = [
    'booking_currency',
    'length_of_stay',
    'bedroom',
    'bathroom',
    'beds',
    'capacity',
    'wifi',
    'tv',
    'cable_tv',
    'ac',
    'workspace',
    'pool',
    'parking',
    'gym',
    'kitchen',
    'area_name',
    'area_distance_to_airport',
    'airport_pickup_price_idr',
    'booking_check_in_date',
    'booking_check_in_month',
    'booking_check_in_year',
    'booking_check_out_date',
    'booking_check_out_month',
    'booking_check_out_year'
    ]

    
    data1 = request.get_json()
    print(data1)


    # Konversi dictionary ke DataFrame
    df_baru = pd.DataFrame(data1)

    # Prediksi dengan setiap model dasar
    preds_baru_knn = model_knn.predict(df_baru.values)
    preds_baru_hgb = model_hgb.predict(df_baru.values)
    preds_baru_dt = model_dt.predict(df_baru.values)
    preds_baru_bagging = model_bagging.predict(df_baru.values)
    preds_baru_adaboost = model_adaboost.predict(df_baru.values)

    # Stack prediksi sebagai fitur baru untuk meta model
    stacked_features_baru = np.column_stack((preds_baru_knn, preds_baru_hgb, preds_baru_dt, preds_baru_bagging, preds_baru_adaboost))

    # Prediksi dengan meta model
    prediksi_final = meta_model.predict(stacked_features_baru)


    return jsonify(
            {
                "status": True,
                "code": 200,
                "message": "OK",
                "data": {"booking_in_idr": prediksi_final[0]}
            }
        )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Define the input fields
        input_fields = [
            "booking_currency",
            "listing_id",
            "length_of_stay",
            "unit_id",
            "bedroom",
            "bathroom",
            "beds",
            "capacity",
            "property_id",
            "wifi",
            "tv",
            "cable_tv",
            "ac",
            "workspace",
            "pool",
            "parking",
            "gym",
            "kitchen",
            "area_id",
            "area_name",
            "area_distance_to_airport",
            "airport_pickup_price_idr",
            "booking_check_in_date",
            "booking_check_in_month",
            "booking_check_in_year",
            "booking_check_out_date",
            "booking_check_out_month",
            "booking_check_out_year"
        ]

        # Get the JSON data from the request
        data = request.get_json()

        # Create an empty list to hold the input values
        input_data = []

        # Populate the input data list with values from the JSON data
        for field in input_fields:
            input_data.append(data[field])

        # Convert the input data to a numpy array and reshape for prediction
        input_data = np.array(input_data).reshape(1, -1)

        # Make the prediction
        prediction = model.predict(input_data)

        # Return the prediction result
        return jsonify(
            {
                "status": True,
                "code": 200,
                "message": "OK",
                "data": {"prediction": prediction[0]}
            }
        )
    except Exception as e:
        return jsonify(
            {
                "status": False,
                "code": 500,
                "message": f"Internal Server Error: {str(e)}",
                "data": None
            }
        )
if name == "main":
    app.run(host="0.0.0.0", port=8080)