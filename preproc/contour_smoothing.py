import numpy as np
from scipy.ndimage.morphology import *
import SimpleITK as sitk
import cv2

from scipy.ndimage.morphology import binary_closing

def smoothContours(ctrs):
    '''
    Smooth an array of contours in 3D using an spheric mask
    and the closing morphological operator
    :param ctrs:
    :return:
    '''
    maskSize = 8
    radiusSize = 4
    sphere_mask = makeSphere(maskSize, radiusSize)
    output_ctrs = []

    for idx in range(len(ctrs)):
        cur_ctr_np = sitk.GetArrayFromImage(ctrs[idx])
        # print('Smoothing ctr: {} ...'.format(idx))
        smooth_ctr = binary_closing(cur_ctr_np, structure=sphere_mask)
        output_ctrs.append( sitk.GetImageFromArray(smooth_ctr.astype(np.uint8)))

    return output_ctrs

def makeExampleImage(simg):
    # ------ Testing smoothing
    A = np.zeros((simg, simg, simg))
    minb = int(2*simg/10)
    maxb = int(8*simg/10)

    mins = int(4*simg/10)
    maxs = int(6*simg/10)
    A[ :, mins:maxs, minb:maxb] =255
    A[ :, minb:maxb, mins:maxs] =255
    return A

def makeCircle(size, r):
    '''
    Makes a mask with the form of a circle
    :param size: Size of the mask (10,10)
    :param r: Radious of the sphere inside the image
    :return:
    '''
    corAll = np.arange(size)
    X, Y = np.meshgrid(corAll,corAll)
    center = np.floor(size/2)
    vals = np.square(X-center) + np.square(Y-center)
    A = vals < (r*r)
    return A

def makeSphere(size, r):
    '''
    Makes a mask with the form of a sphere.
    :param size: Size of the mask (10,10,10)
    :param r: Radious of the sphere inside the image
    :return:
    '''
    corAll = np.arange(size)
    X, Y, Z = np.meshgrid(corAll,corAll,corAll)
    center = np.floor(size/2)
    vals = np.square(X-center) + np.square(Y-center) + np.square(Z-center)
    A = vals < (r*r)
    return A

def getContourMinPosFrom2DMask(mask):
    image, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return contours

def getContourFromMask(mask):
    '''
    Obtains the contour of a binary mask
    :param mask:
    :return:
    '''
    s = makeSphere(4,2)
    eroded_mask = binary_erosion(mask, structure=s)
    ctr = mask - eroded_mask
    ctr[ctr>0] = 1 #Binary
    return ctr
