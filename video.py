import cv2
import os
import shutil
from image_maniputation import ImageManipulation

def MainVideo(imageObject ,cropped_image_url):
    video_length_seconds = 9
    fps = 20
    imageObject.total_images = video_length_seconds * fps

    def CreateCopies(source_image, index, dir_path):
        shutil.copy2(source_image, dir_path + '/newname' + str(index+100) +'.png')


    dir_path = imageObject.tmp_folder()
    output_file = 'static/user_uploads/' + imageObject.file_name + '.mp4'

    # Create copies of images
    current_dir = os.getcwd()
    os.mkdir(current_dir + "/" + dir_path)
    for n in range(imageObject.total_images):
        CreateCopies(cropped_image_url, n, dir_path)

    # Load images to list
    images = []
    for f in os.listdir(dir_path):
        images.append(f)
    images.sort()

    # Manipulate images
    images = ImageManipulation(images, imageObject)

    # Determine the width and height from the first image
    image_path = os.path.join(dir_path, images[0])
    frame = cv2.imread(image_path)
    height, width, channels = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'AVC1') # Be sure to use lower case
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (width, height))

    for image in images:
        image_path = os.path.join(dir_path, image)
        frame = cv2.imread(image_path)
        out.write(frame) # Write out frame to video

    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()
    return output_file

def AddAudio(video_location, imageObject):
    current_dir = os.getcwd()
    full_video_location = current_dir + "/" + video_location
    full_audio_location = current_dir + "/static/hello_darkness.mp3"
    tmp_video_location = current_dir + "/static/user_uploads/tmp_" + imageObject.file_name + ".mp4"
    os.system("ffmpeg -i " + full_video_location + " -i " + full_audio_location + " -c copy -map 0:v:0 -map 1:a:0 " + tmp_video_location)
    #os.remove(full_video_location)
    os.rename(tmp_video_location, full_video_location)


