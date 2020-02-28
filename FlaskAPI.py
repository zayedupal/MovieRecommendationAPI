from flask import Flask, jsonify, request
from MovieLens_reco_content import RecoContent

app = Flask(__name__)
recoContent = RecoContent()

@app.route("/",methods=['GET'])
def get_movie_list():
    return jsonify(recoContent.get_movies().values.tolist())

@app.route("/predict", methods=['POST'])
def do_prediction_content():
    print("request fetched: ", request)
    json = request.get_json()
    print('json:',json)
    df = recoContent.json_to_df(json)

    prediction = recoContent.predict(df)
    print('prediction: ',prediction.values.tolist())
    return jsonify(prediction.values.tolist())
    # return prediction.to_json()
@app.route("/upload", methods=['POST'])
def do_image_upload():
    f = request.files['file']
    print('file:',f.filename)
    return jsonify(f.filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)