import easygui as eg
import cv2 as cv
from os import walk
from os.path import splitext
from random import randint


def file_extentions(directory):
	fileExts = set()
	_, _, filenames = next(walk(directory))

	for f in filenames:
		_, ext = splitext(f)
		fileExts.add(ext)

	if '' in fileExts:  # deleting directory extension if exists
		fileExts.remove('')

	return fileExts


def photo_iterator(img_path, fileExt):
	_, _, filenames = next(walk(img_path))

	for f in filenames:
		_, ext = splitext(f)
		if ext in fileExt:
			filepath = img_path + '/' + f
			yield cv.imread(filepath)


img_path = eg.diropenbox(default='.')
video_path = eg.fileopenbox(default='.')
fileExtList = list(file_extentions(img_path))

if len(fileExtList) == 0:
	raise "There are no file here!"
if len(fileExtList) == 1:
	fileExtList.append('')  # Dummy item, because multchoicebox need at least 2 item
fileExt = eg.multchoicebox(msg="Select file extentions that you want to process data augmentation on those",
                           title="Select file extentions",
                           choices=fileExtList)

cap = cv.VideoCapture(video_path)

videosize = cap.read()[1].shape[:2][::-1]
out = cv.VideoWriter('perfuse.avi', cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, videosize)

p_iter = photo_iterator(img_path, fileExt)
count = 0
while cap.isOpened():
	ret, frame = cap.read()
	if ret:
		count += 1
		try:
			if count == 2:
				obj = next(p_iter)
				count = 0

			# cv.imshow('obj', obj)
			width, height, _ = frame.shape
			x1 = randint(0, width - obj.shape[0])
			y1 = randint(0, height - obj.shape[1])

			frame[x1:x1 + obj.shape[0], y1:y1 + obj.shape[1], :] = obj[:, :, :]
		except:
			pass
		# cv.imshow('frame', frame)
		out.write(frame)
		if cv.waitKey(25) & 0xFF == ord('q'):
			break
	else:
		break
