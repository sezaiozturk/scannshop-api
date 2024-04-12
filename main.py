from flask import Flask,request,jsonify,send_from_directory,render_template
import os
app=Flask(__name__)

@app.route("/")
def home():
    return "Home"


@app.route('/get_image/<filename>')
def get_image(filename):
    # Dosya adına göre resmin yolunu oluşturun
    image_path = f'uploads/{filename}'
    # Resmi doğrudan okuyun ve istemciye gönderin
    return send_from_directory('.', image_path)
    #return send_from_directory('uploads', filename)

@app.route('/list')
def list_images():
    # uploads klasöründeki tüm dosyaları al
    image_files = os.listdir('uploads')
    # dosya adlarını bir JSON yanıtı olarak geri döndür
    return jsonify(image_files)

@app.route('/view')
def view_images():
    # uploads klasöründeki tüm dosyaları al
    image_files = os.listdir('uploads')
    # resimlerin tam yollarını oluştur
    image_paths = [f'uploads/{filename}' for filename in image_files]
    # HTML şablonunu render et
    return render_template('view_images.html', image_paths=image_paths)

if __name__=="__main__":
    app.run(debug=True)