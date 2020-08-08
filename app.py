#necessary imports
import os
from flask import Flask,jsonify,request
from models import Base, Session, engine, Product
from werkzeug.utils import secure_filename
from PIL import Image 



app = Flask(__name__)
Base.metadata.create_all(engine)
session = Session()
#defining the folder to upload the images
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENTIONS = {'png','jpg','jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#sample end point to check
@app.route('/')
def index():
    return jsonify({'message':'welcome dennis'})

#end point to add products i.e with an image and a title
@app.route('/addproduct', methods = ['POST'])
def addproduct():

    #from postman the file is read by using the form-data
    data = request.form['title']
    image = request.files['file']
    filename = secure_filename(image.filename)

    if 'file' not in request.files:
     return jsonify({'message': 'image not found'})

    #checks weather a valid file name is present or the image do already exist.
    if image.filename == '' or session.query(Product).filter_by(image_name=filename).first():
        return jsonify({'message': ' image already exists or a valid one is missing'})


    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    product = Product(title = data, image_name = filename )
    session.add(product)
    session.commit()
    
    #opening the image to be resized
    imageview = Image.open('images/' + filename)
    print(imageview.size)
    resizedimage1 = imageview.resize((250, 250)) #resized image with 250 * 250
    resizedimage2 = imageview.resize((300, 300)) #resized image with 300 * 300
    resizedimage3 = imageview.resize((700, 700)) #resized image with 700 * 700
    resizedimage4 = imageview.resize((1000, 1000)) #resized image with 1000 * 1000
    print(resizedimage1.size)

    response = {'product_id': product.id, 'image_name': filename, 'resizedimage1': resizedimage1.size,
     'resizedimage2': resizedimage2.size, 'resizedimage3': resizedimage3.size,
     'resizedimage4': resizedimage4.size}
    return (
        jsonify(message=f"product added successfully.", data=response), 200
    )


if __name__ == '__main__':
    app.run(debug=True)