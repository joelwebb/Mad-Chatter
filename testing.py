import boto3
import cv2
import os

def image_to_thumbs(img_path):
	"""Create thumbs from image"""
	try:
		print("reading image")
		img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
		# resize image
		resized = cv2.resize(img, (200, 200), interpolation = cv2.INTER_AREA)
		print("resized successfully")
		#write it out
		cv2.imwrite(img_path, resized)
		return True
	except Exception as e:
		print(e)
		print("couldn't resize image")
		raise e
	
	
def grab_second_frame(video_path: str, output_path:str):
	"""grabs second frame"""
	print("grabbing second frame")
	try:
		cam = cv2.VideoCapture(video_path)
		# frame
		current_frame = 0
		
		while(True):
			# reading from frame
			ret, frame = cam.read()
			#skip first frame
			if current_frame == 0:
				current_frame += 1
				continue
			else:
				pass
			if ret:
				# if video is still left continue creating images
				print('Creating thumbnail...')
				# writing the extracted images
				cv2.imwrite(output_path, frame)
				break
		#close the video sourcee
		cam.release()
		return True
	except Exception as e:
		print(e)
		print('Error processing thumbnail')
		raise e

def parse_input(input_bucket, input_key):
	"""makes a thumbnail from s3 video and uploads to s3"""
	try:
		#create s3 client
		s3Client = boto3.client('s3')
		#download local location

		#download it from s3
		url = s3Client.generate_presigned_url(ClientMethod='get_object', Params={ 'Bucket': input_bucket, 'Key': input_key } )
		#get file prefix and make it png
		thumbnail_output = str(os.path.splitext(input_key)[0]) + "_thumbnail.png"
		
		#grab the frame to tmp/thumbnail_{}
		grab_second_frame(url, thumbnail_output) 
		#rezise it to 200 X 200 for thumbnail
		image_to_thumbs(thumbnail_output)

		s3Client.upload_file(thumbnail_output, input_bucket, thumbnail_output)

		return "success"

	except Exception as e:
		print(e)
		print('Error uploading file to output bucket')
		return "Error uploading file to output bucket"


if __name__ == "__main__":
	parse_input(input_bucket, input_key)
