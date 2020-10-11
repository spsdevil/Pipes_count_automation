
# A very simple Flask Hello World app for you to get started with...

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import random

# path = os.getcwd()
UPLOAD_FOLDER = './static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)

		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(filepath)
		src = cv2.imread(filepath, cv2.IMREAD_COLOR)

	# camera_port = 0  # Assigns which webcame to detect if user has more than one webcam
	# camera = cv2.VideoCapture(camera_port)
	# first_frame = None

	# while True:
	# 	status = 0
	# 	check, frame = camera.read()

		
		gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
		gray_blurred = cv2.blur(gray, (3, 3))

#
#     	# Apply Hough transform on the blurred image.
		rows = gray.shape[0]
		detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, rows/80, param1 = 50, param2 = 25, minRadius = 6,maxRadius = 15)

		# Draw circles that are detected.
		if detected_circles is not None:

			# Convert the circle parameters a, b and r to integers.
			detected_circles = np.uint16(np.around(detected_circles))

			for pt in detected_circles[0, :]:
				a, b, r = pt[0], pt[1], pt[2]

				# Draw the circumference of the circle.
				cv2.circle(src, (a, b), r, (0, 255, 0), 2)

				# Draw a small circle (of radius 1) to show the center.
				# cv2.circle(src, (a, b), 1, (0, 0, 255), 3)
		img_num = random.randint(0,100)
		cv2.imwrite(os.path.join(UPLOAD_FOLDER + str(img_num) + '.jpg'), src)
		cvt_img = str(img_num) + ".jpg"
		count = detected_circles.shape
# 		#print('upload_image filename: ' + filename)
		flash('pipes_count:'+str(count[1]))
		return render_template('upload.html', filename=cvt_img)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)