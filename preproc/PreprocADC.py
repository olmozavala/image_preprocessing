from img_viz.medical import MedicalImageVisualizer
from img_viz.constants import SliceMode

import SimpleITK as sitk
import numpy as np
from preproc.UtilsItk import copyItkImage


def correct_adc_np(img, low_threshold=1, max_value=4500, fix_value='mean'):
    """
    Corrects the adc values (zero patches) with another value
    :param img:
    :param low_threshold:
    :param max_value:
    :param fix_value:
    :return:
    """
    img_mod = img.copy()
    # Get index of voxels below the threshold
    below_th_idx = img < low_threshold
    others_idx = img >= low_threshold

    if fix_value == 'mean':
        mid_val = np.mean(img[others_idx])
        img_mod[below_th_idx] = mid_val
        img_mod = img_mod/max_value
        # print(F'{np.amin(img_mod)},{np.amax(img_mod)}')

    return img_mod


def correct_adc_itk(img_itk, low_threshold=1, max_value=4500, fix_value='mean'):
    """
    This function receives and outputs an itk image.
    :param img_itk:
    :param low_threshold:
    :param max_value:
    :param fix_value:
    :return:
    """
    img_np = sitk.GetArrayFromImage(img_itk)
    img_np_norm = correct_adc_np(img_np, low_threshold, max_value, fix_value)
    return copyItkImage(img_itk,img_np_norm)


# ================= Only for testing =====================
if __name__ == '__main__':
    from os.path import join

    file_name = join('..','imagevisualizer', 'test_data', 'input','Case-0001', 'img_adc.nrrd')
    print('Reading image....')
    img_itk = sitk.ReadImage(file_name)

    img_corrected_itk = correct_adc_itk(img_itk, low_threshold=1, max_value=4500, fix_value='mean')
    print('Plotting results....')
    viz_obj = MedicalImageVisualizer(disp_images=True)
    viz_obj.plot_img_and_ctrs_itk(img_itk, itk_ctrs=[], slices=SliceMode.MIDDLE,
                                  file_name_prefix='Original')
    viz_obj.plot_img_and_ctrs_itk(img_corrected_itk, itk_ctrs=[], slices=SliceMode.MIDDLE,
                                  file_name_prefix='Corrected')


