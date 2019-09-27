import os
from os.path import join
import SimpleITK as sitk
from inout.io_common import create_folder


# Contains some utility functions for saving and basic image manipulation with itk


def castImage(img, type):
    """
    Cast an itk image to an specific type
    :param img:
    :param type:
    :return:
    """
    castFilter = sitk.CastImageFilter()
    castFilter.SetOutputPixelType(type) #sitk.sitkUInt8
    out = castFilter.Execute(img)
    return out

def getMaximumValue(img):
    """
    Gets the maximum value from an itk image
    :param img:
    :return:
    """
    maxFilter = sitk.StatisticsImageFilter()
    maxFilter.Execute(img)
    maxValue = maxFilter.GetMaximum()
    return maxValue

def copyItkImage(itk_src, np_arr):
    """
    Copies the 'most' important parameters from an itk image into a np array
    :param itk_src:
    :param np_arr:
    :return:
    """
    out_itk = sitk.GetImageFromArray(np_arr)
    out_itk.SetOrigin(itk_src.GetOrigin())
    out_itk.SetDirection(itk_src.GetDirection())
    out_itk.SetSpacing(itk_src.GetSpacing())
    return out_itk
