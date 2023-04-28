# Load libraries
import flask
import pandas as pd
import tensorflow as tf
import keras
import json
from flask import request
from keras.models import load_model

# instantiate flask 
app = flask.Flask(__name__)

# we need to redefine our metric function in order 
# to use it when loading the model 
# def auc(y_true, y_pred):
#     auc = tf.metrics.auc(y_true, y_pred)[1]
#     keras.backend.get_session().run(tf.local_variables_initializer())
#     return auc


# # load the model, and pass in the custom metric function
# global graph
# graph = tf.get_default_graph()
path = request.json["recognizer"]
model = load_model('model.h5')

# define a predict function as an endpoint 
@app.route("/predict", methods=["GET","POST"])
def predict():
    data = {"success": False}
    price = []

    params = True
    if (params == None):
        params = flask.request.args

    # if parameters are found, return a prediction
    if (params != None):
        img = tf.keras.preprocessing.image.load_img(path, target_size=(256, 256))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) 
        predictions = model.predict(img_array)
        classes = ['Aluminium', 'Carton', 'Glass', 'Organic Waste', 'Other Plastics', 'Paper and Cardboard', 'Plastic', 'Textiles', 'Wood', 'alluminium+ cardboard', 'Newspaper', 'Books', 'Magazines', 'White Papers'
                   'Grey Board', 'PlainPapers', 'Copy', 'Fibre']
        for index,i in enumerate(predictions[0]):
            if i >0.20:
                print("Prediction: ", classes[index])  #, f"{i*100}%")
                if classes[index]=="Aluminium":
                    print("Price of Alumminium per kg:",70)
                    price.append("Price of Alumminium per kg: 70")
                elif classes[index]=="Carton":
                    print("Price of carton per kg:",9.5)
                    price.append("Price of carton per kg:9.5")
                elif classes[index]=="Glass":
                    print("Price of glass in kg:",5)
                    price.append("Price of glass in kg:5")
                elif classes[index]=="Other Plastics":
                    print("Price of other plastics per kg:",4)
                    price.append("Price of other plastics per kg:4")
                elif classes[index]=="Paper and Cardboard":
                    print("Price of newspapers per kg:",15)
                    print("Price of cardboard per kg:",7.5) 
                    price.append("Price of cardboard per kg:7.5")
                    price.append("Price of newspapers per kg:15")
                elif classes[index]=="Plastic":
                    print("Price of plastic per kg:",6)
                    price.append("Price of plastic per kg:6")
                elif classes[index]=="Textiles":
                    print("Price of textiles per kg:",10)
                    price.append("Price of textiles per kg:10")
                elif classes[index]=="Wood":
                    print("Price of wood per kg:",80) 
                    price.append("Price of wood per kg:80")
                elif classes[index]=="alluminium+cardboard":
                    print("Price of cardboard per kg:",7.5)
                    print("Price of Alumminium per kg:",100)  
                    price.append("Price of cardboard per kg:7.5")
                    price.append("Price of aluminium per kg:100")   
                else:
                    print("SORRY THIS DOES NOT COMES UNDER DRY WASTE CATEOGRY")  
                    price = "SORRY THIS DOES NOT COMES UNDER DRY WASTE CATEOGRY"

    # return a response in json format 
    return flask.jsonify({"price": price})    

# start the flask app, allow remote connections 
if __name__ == '__main__':
    app.run(port=7000)