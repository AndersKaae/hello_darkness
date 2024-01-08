const maxImageWidth = 640;
const maxImageHeight = 640;

var imageObject = new Object();

imgInp.onchange = (evt) => {
  const [file] = imgInp.files;
  if (file) {
    let imageBox = document.getElementById("imageBox");
    imageBox.classList.remove("hide");
    document.getElementById("imageCropper").classList.remove("hide");
    document.getElementById("generateMeme").classList.remove("hide");
    document.getElementById("uploadForm").classList.add("hide");
    uploadedImage.src = URL.createObjectURL(file);
    //Initiate the JavaScript Image object.
    uploadedImage.onload = function () {
      imageObject = GetOriginalSize(imageObject, this);
      imageObject = GetAndSetReducedImageSize(imageObject); // Gets the size of the image as displayed
      imageObject = OptimalCropWidth(this, imageObject);
      imageObject = StoreImageBoxLocation(imageObject);
      let imageCropper = document.getElementById("imageCropper");
      imageCropper.style.width = imageObject.widthCrop + "px";
      imageCropper.style.height = imageObject.heightCrop + "px";
      imageCropper.style.left = imageObject.imageBoxX + "px";
      imageCropper.style.top = imageObject.imageBoxY + "px";
    };
  }
};

function GetOriginalSize(imageObject, image){
  imageObject.heightOrginal = image.height;
  imageObject.widthOrginal = image.width;
  return imageObject;
}

function GetAndSetReducedImageSize(imageObject) {
  if (imageObject.heightOrginal > imageObject.widthOrginal){
    if (imageObject.heightOrginal > 640){
      imageObject.heightReduced = 640;
      imageObject.widthReduced = (640 / imageObject.heightOrginal) * imageObject.widthOrginal;
    }
  }
  let uploadedImageElement = document.getElementById("uploadedImage");
  //imageObject.heightReduced = uploadedImageElement.clientHeight;
  //imageObject.widthReduced = uploadedImageElement.clientWidth;
  uploadedImageElement.style.width = imageObject.widthReduced + "px"
  uploadedImageElement.style.height = imageObject.heightReduced + "px"
  return imageObject;
}

function OptimalCropWidth(image, imageObject) {
  const apectWidth = 16;
  const aspectHeight = 9;
  // Check if we can run full width
  if (
    imageObject.heightOrginal >
    (imageObject.widthOrginal / apectWidth) * aspectHeight
  ) {
    imageObject.widthCrop = imageObject.widthReduced;
    imageObject.heightCrop =
      (imageObject.widthReduced / apectWidth) * aspectHeight;
  } else {
    // MISSING LOGIN FOR WHEN THE IMAGE WIDTH IS LARGER THAN HEIGHT
  }
  return imageObject;
}

var m = document.getElementById("imageCropper");
m.addEventListener("mousedown", mouseDown, false);
window.addEventListener("mouseup", mouseUp, false);

function mouseUp() {
  window.removeEventListener("mousemove", move, true);
}

function mouseDown(e) {
  window.addEventListener("mousemove", move, true);
  let colisionStatus = cropColisionDectected();
  unColideElements(colisionStatus);
}

function move(e) {
  let colisionStatus = cropColisionDectected();
  if (colisionStatus == "noColision") {
    m.style.top = e.clientY - imageObject.heightCrop / 2 + "px";
    m.style.left = e.clientX - imageObject.widthCrop / 2 + "px";
    imageObject.cropX = parseInt(m.style.left.replace('px', ''))
    imageObject.cropY = parseInt(m.style.top.replace('px', ''))
    console.log(imageObject)
  } else {
    unColideElements(colisionStatus);
  }
}

function cropColisionDectected() {
  let colision = "noColision";
  let cropElement = document.getElementById("imageCropper");
  // Handling colision with left side of image
  if (cropElement.getBoundingClientRect().x < imageObject.imageBoxX) {
    colision = "leftColision";
  }
  // Handling colision with right side of image
  if (
    cropElement.getBoundingClientRect().x + imageObject.widthCrop >
    imageObject.imageBoxX + imageObject.widthReduced
  ) {
    colision = "rightColision";
  }
  // Handling colision with top side of image
  if (cropElement.getBoundingClientRect().y < imageObject.imageBoxY) {
    colision = "topColision";
  }
  // Handling colision with bottom side of image
  if (
    cropElement.getBoundingClientRect().y + imageObject.heightCrop >
    imageObject.imageBoxY + imageObject.heightReduced
  ) {
    colision = "bottomColision";
  }
  return colision;
}

function unColideElements(colisionStatus) {
  if (colisionStatus == "leftColision") {
    m.style.left = imageObject.imageBoxX + "px";
  } else if (colisionStatus == "rightColision") {
    m.style.left =
      imageObject.imageBoxX +
      imageObject.widthReduced -
      imageObject.widthCrop +
      "px";
  } else if (colisionStatus == "topColision") {
    m.style.top = imageObject.imageBoxY + "px";
  } else if (colisionStatus == "bottomColision") {
    m.style.top =
      imageObject.imageBoxY +
      imageObject.heightReduced -
      imageObject.heightCrop +
      "px";
  }
}

function StoreImageBoxLocation(imageObject) {
  let imageBox = document.getElementById("imageBox");
  var rect = imageBox.getBoundingClientRect();
  imageObject.imageBoxX = rect.x;
  imageObject.imageBoxY = rect.y;
  return imageObject;
}

document
  .getElementById("generateMeme")
  .addEventListener("click", saveToLocalStorage);

function saveToLocalStorage() {
  //sessionStorage.setItem('imageObject', JSON.stringify(imageObject));
  document.cookie = "imageObject =" + JSON.stringify(imageObject);
}
