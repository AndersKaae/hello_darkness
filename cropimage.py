import os
import cv2
import uuid


def CropMain(url, imageObject):
    def GenerateFileName(url):
        modified_url = url.replace("./","")
        modified_url = modified_url.split(".")
        modified_url = modified_url[0] + "_cropped." + modified_url[1]
        return modified_url

    image = cv2.imread(url)
    sizeDifferenceFactor = imageObject.reduced_to_original_factor()
    x = int(imageObject.crop_pos["x"] * sizeDifferenceFactor)
    y = int(imageObject.crop_pos["y"] * sizeDifferenceFactor)
    h = int(imageObject.crop_dimensions["height"] * sizeDifferenceFactor)
    w = int(imageObject.crop_dimensions["width"] * sizeDifferenceFactor)
    cropped_image = image[y:y+h, x:x+w]

    image_url = GenerateFileName(url)
    cv2.imwrite(image_url, cropped_image)
    return image_url

def SaveImage(file, folder, imageObject):
    def GetFileType(filename):
        extension = filename.split(".")[-1]
        return extension

    imageObject.file_extension = GetFileType(file.filename)
    imageObject.file_name = str(uuid.uuid4())
    file.save(os.path.join(folder, imageObject.full_file_name()))
    url = "./" + folder + "/" + imageObject.full_file_name()
    return url, imageObject

def ConstructObjectFromJson(imageObject, imageJson):
    imageObject.crop_pos["x"] = imageJson['cropX'] - imageJson['imageBoxX']
    imageObject.crop_pos["y"] = imageJson['cropY'] - imageJson['imageBoxY']
    imageObject.crop_dimensions["height"] = imageJson["heightCrop"]
    imageObject.crop_dimensions["width"] = imageJson["widthCrop"]
    imageObject.original_image_dimenions["height"] = imageJson["heightOrginal"]
    imageObject.original_image_dimenions["width"] = imageJson["widthOrginal"]
    imageObject.reduced_image_dimensions["height"] = imageJson["heightReduced"]
    imageObject.reduced_image_dimensions["width"] = imageJson["widthReduced"]
    return imageObject