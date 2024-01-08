from flask import Flask, render_template, request
import json
from cropimage import ConstructObjectFromJson, SaveImage, CropMain
from models import ImageClass
from video import MainVideo, AddAudio

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8dsadadas2323sfsdfsdfz\n\xec]/'

UPLOAD_FOLDER = 'static/user_uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'POST':
        # Getting file from front end
        file = request.files['file']
        # Saving the file locally and producing an URL
        imageObject = ImageClass()
        imageUrl, imageObject = SaveImage(file, app.config['UPLOAD_FOLDER'], imageObject)
        # Getting the image object from the front end via cookies
        imageJson = json.loads(request.cookies.get('imageObject'))
        imageObject = ConstructObjectFromJson(imageObject, imageJson)
        cropped_image_url = CropMain(imageUrl, imageObject)
        video_url = MainVideo(imageObject, cropped_image_url)
        AddAudio(video_url, imageObject)
        return render_template('processing.html', imageUrl = cropped_image_url, videoUrl = video_url)
    return render_template('main.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'    
    app.run(host="localhost", port=5000, debug=True, threaded = True)