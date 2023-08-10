# import dependencies
from ultralytics import YOLO
import cv2
import numpy as np
import os

# Load the segmentation model
segmentation_model = YOLO(os.path.join('..', 'src', 'YOLO_models', 'yolov8n-seg.pt'))
    
def get_segmented_image(imgpath):
    # perform the segmentation on the image
    results = segmentation_model.predict(imgpath, retina_masks=True, verbose=False)

    # get only the segmentation-highlighted objects from the image using the obtained masks
    # from https://github.com/ultralytics/ultralytics/issues/1411
    segmented_img = None
    for result in results:
        mask = result.masks.cpu().numpy()
        masks = mask.data.astype(bool)
        ori_img = result.orig_img
        for m in masks:
            # initialise new segmented image as numpy array
            segmented_img = np.zeros_like(ori_img, dtype=np.uint8)
            # overlay mask on original image to get segmented image,
            # save this as segmented_img
            segmented_img[m] = ori_img[m]
   
    return segmented_img


# function that performs the segmentation of the car
def save_segmented_image(imgpath_orig, segm_folder, rescale=False):
    # get img filename and folder from imgpath
    orig_folder, imgfilename = os.path.split(imgpath_orig)
    # get image name and extension from the filename
    imgname, fileextension = ''.join(imgfilename.split('.')[:-1]), imgfilename.split('.')[-1]
    # generate relevant filepaths
    imgpath_orig = os.path.join(orig_folder, '.'.join((imgname, fileextension)))
    imgpath_segm = os.path.join(segm_folder, '.'.join((imgname + '_segm', fileextension)))
    
    # perform segmentation
    segmented_img = get_segmented_image(imgpath_orig)

    # save segmented image
    # first check if we even have a segmented image.
    if not isinstance(segmented_img, type(None)):
        if rescale:
            segmented_img = cv2.resize(segmented_img, (256, 256))
        cv2.imwrite(imgpath_segm, segmented_img)
    else:
        print('Image could not be segmented.')