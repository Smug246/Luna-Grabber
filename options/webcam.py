import cv2
import os

def capture_images(num_images=1):
	num_cameras = 0
	cameras = []
	os.makedirs(os.path.join(temp_path, "Webcam"), exist_ok=True)

	while True:
		cap = cv2.VideoCapture(num_cameras)
		if not cap.isOpened():
			break
		cameras.append(cap)
		num_cameras += 1

	if num_cameras == 0:
		return

	for _ in range(num_images):
		for i, cap in enumerate(cameras):
			ret, frame = cap.read()
			if ret:
				cv2.imwrite(os.path.join(temp_path, "Webcam", f"image_from_camera_{i}.jpg"), frame)

	for cap in cameras:
		cap.release()