import cv2
import os


count=1

def extract_frames(video_path, frames_dir, overwrite=False, start=-1, end=-1, every=1):



    video_path = os.path.normpath(video_path)  # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)  # make the paths OS (Windows) compatible

    # print(video_path+'\n'+frames_dir)

    video_dir, video_filename = os.path.split(video_path)  # get the video path and filename from the path

    assert os.path.exists(video_path)  # assert the video file exists

    capture = cv2.VideoCapture(video_path)  # open the video using OpenCV

    if start < 0:  # if start isn't specified lets assume 0
        start = 0
    if end < 0:  # if end isn't specified assume the end of the video
        end = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    every = end//34
        # capture.get(cv2.CAP_PROP_Length)
    # print('Total Frames = ' + str(end))

    capture.set(1, start)  # set the starting frame of the capture
    frame = start  # keep track of which frame we are up to, starting from start
    while_safety = 0  # a safety counter to ensure we don't enter an infinite while loop (hopefully we won't need it)
    saved_count = 0  # a count of how many frames we have saved




    while frame < every * 34:  # lets loop through the frames until the end

        _, image = capture.read()  # read an image from the capture

        if while_safety > 500:  # break the while if our safety maxs out at 500
            break

        # sometimes OpenCV reads None's during a video, in which case we want to just skip
        if image is None:  # if we get a bad return flag or the image we read is None, lets not save
            while_safety += 1  # add 1 to our while safety, since we skip before incrementing our frame variable
            continue  # skip

        if frame % every == 0:  # if this is a frame we want to write out based on the 'every' argument
            while_safety = 0  # reset the safety count

            save_path = os.path.join(frames_dir, str(count), "{:05d}.jpg".format(frame))  # create the save path

            print(save_path)
            if not os.path.exists(save_path) or overwrite:  # if it doesn't exist or we want to overwrite anyways
                cv2.imwrite(save_path, image)  # save the extracted image
                saved_count += 1  # increment our counter by one

        frame += 1  # increment our frame count

    capture.release()  # after the while has finished close the capture

    return saved_count  # and return the count of the images we saved



# # # for i in north[:5]:
# extract_frames('dataset/north/%s'%'north1605902720941.mp4','./data',every=2)


folders = os.listdir('dataset')
folders = ['north','south']


for folder in folders:
	print('\n' + folder + '\n')
	if os.path.isdir('./data/'+folder):
		pass
	else:
		os.mkdir('./data/'+folder)
	for video in os.listdir('dataset/'+folder):
		os.mkdir('./data/'+folder+'/'+str(count))
		files = extract_frames('dataset/'+folder+'/'+video,'data/'+folder,True)
		
		count+=1


minimum = 300

folders = os.listdir('dataset')

for folder in folders:
	print('\n' + folder + '\n')
	for video in os.listdir('dataset/'+folder):
		capture = cv2.VideoCapture('dataset/'+folder+'/'+video)

		frame = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
		print("Frame = " + str(frame))
		if(frame<minimum):
			minimum = frame
		capture.release()

print('Minimum Frame Count = '+ str(minimum))


"""
   Extract frames from a video using OpenCVs VideoCapture
   :param video_path: path of the video
   :param frames_dir: the directory to save the frames
   :param overwrite: to overwrite frames that already exist?
   :param start: start frame
   :param end: end frame
   :param every: frame spacing
   :return: count of images saved
   """