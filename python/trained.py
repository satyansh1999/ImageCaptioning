from pickle import load
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from keras.models import load_model

import sys
import json
# from PIL import Image
# from urllib import request
# from io import BytesIO

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo,sequence], verbose=0)
        yhat = argmax(yhat)
        word = word_for_id(yhat, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'endseq':
            break
    return in_text

def extract_feature(filename):
    model = VGG16()
    model.layers.pop()
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    image = load_img(filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = model.predict(image, verbose=0)
    return feature

# def extract_feature(filename):
#     model = VGG16()
#     # re-structure the model
#     model.layers.pop()
#     model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
#     url = "https://post.healthline.com/wp-content/uploads/2020/08/3180-Pug_green_grass-1200x628-FACEBOOK-1200x628.jpg"
# #     response = requests.get(url)
# #     image = Image.open(BytesIO(response.content))
#     res = request.urlopen(url).read()
#     image = Image.open(BytesIO(res)).resize((224,224))
#     image = img_to_array(image)
#     image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
#     image = preprocess_input(image)
#     feature = model.predict(image, verbose=0)
#     return feature

tokenizer = load(open('tokenizer.pkl', 'rb'))
max_length = 34
model = load_model('model.h5')
photo = extract_feature('../uploads/'+sys.argv[1])
description = generate_desc(model, tokenizer, photo, max_length)

query = description
stopwords = ['startseq','endseq']
querywords = query.split()
resultwords  = [word for word in querywords if word.lower() not in stopwords]
result = ' '.join(resultwords)

resp = {"desc" : result}
print(json.dumps(resp))
# print(result)
sys.stdout.flush()