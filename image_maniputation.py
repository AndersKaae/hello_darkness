from PIL import Image, ImageEnhance
import cv2
from joblib import Parallel, delayed
import multiprocessing

def ImageManipulation(images_list, imageObject):
    images_list_modified = []
    test = multiprocessing.cpu_count()
    #Parallel(n_jobs=multiprocessing.cpu_count())(delayed(rgb_to_gray)(image, imageObject, images_list.index(image), images_list_modified, len(images_list)) for image in images_list)


    for image in images_list:
        Rgb_to_gray(image, imageObject, images_list.index(image), images_list_modified, len(images_list))
        Zoom_on_image(image, imageObject, images_list.index(image), images_list_modified)
    return images_list_modified

def Rgb_to_gray(img, imageObject, idx, images_list_modified, no_items):
    with Image.open(imageObject.tmp_folder() + img) as im:
        converter = ImageEnhance.Color(im)
        factor = 1 - (1/int(imageObject.total_images))*idx
        img2 = converter.enhance(factor)
        filename = "gray" + str(idx) + "." + imageObject.file_extension
        img2.save(imageObject.tmp_folder() + filename)
        #images_list_modified.append(filename)
    print(str(idx) + " / " + str(no_items))
    
def Zoom_on_image(image, imageObject, idx, images_list_modified):
    def Get_Image_Number(image):
        number = int(image.split(".")[0].replace("newname", ""))
        return str(number - 100)
    
    # Opening the image
    image_number = Get_Image_Number(image)
    image = cv2.imread(imageObject.tmp_folder() + "gray" + image_number + "." + imageObject.file_extension)
    # Cropping image
    height_zoom_pixels = 2
    width_zoom_pixels = int((height_zoom_pixels / 9) * 16)
    y = height_zoom_pixels * idx + 1
    x = width_zoom_pixels * idx + 1
    image_height = image.shape[0]
    image_width = image.shape[1]
    h = image_height - (height_zoom_pixels * idx * 2)
    w = image_width - width_zoom_pixels * idx * int((16/9))
    cropped_image = image[y:y+h, x:x+w]
    # rezising image back to original size
    dim = (image_width, image_height)
    resized = cv2.resize(cropped_image, dim, interpolation = cv2.INTER_AREA)
    # Saving the image
    file_name = "zoom" + image_number + "." + imageObject.file_extension
    cv2.imwrite(imageObject.tmp_folder() + file_name, resized)
    images_list_modified.append(file_name)
