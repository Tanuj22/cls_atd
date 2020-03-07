import cv2
from mtcnn import MTCNN

detector = MTCNN()

image = cv2.cvtColor(cv2.imread("1.jpg"), cv2.COLOR_BGR2RGB)
result = detector.detect_faces(image)

# Result is an array with all the bounding boxes detected.

num_of_faces = len(result)

 
for i in range(0,num_of_faces):
	bounding_box = result[i]['box']
	keypoints = result[i]['keypoints']

	tempim = image[bounding_box[1]:(bounding_box[1] + bounding_box[3]), bounding_box[0]:(bounding_box[0] + bounding_box[2])]
	cv2.imwrite("face_{}.jpg".format(i), cv2.cvtColor(tempim, cv2.COLOR_RGB2BGR))
	cv2.rectangle(image,
		      (bounding_box[0], bounding_box[1]),
		      (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
		      (255,255,0),
		      2)

	cv2.circle(image,(keypoints['left_eye']), 2, (255,255,0), 2)
	cv2.circle(image,(keypoints['right_eye']), 2, (255,255,0), 2)
	cv2.circle(image,(keypoints['nose']), 2, (255,255,0), 2)
	cv2.circle(image,(keypoints['mouth_left']), 2, (255,255,0), 2)
	cv2.circle(image,(keypoints['mouth_right']), 2, (255,255,0), 2)

	
	cv2.imwrite("1_result.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
	

print("Number of faces detected: ", num_of_faces)
