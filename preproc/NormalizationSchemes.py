from os import listdir
from img_viz.medical import MedicalImageVisualizer
from img_viz.constants import SliceMode
import SimpleITK as sitk
import time
from os.path import join
import os


def n4itk(img_itk, shrink_factor=2):
    """
    Computes n4ITK bias correction using SimpleItk
    :param img_itk:
    :param viz_result:
    :return:
    """
    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    corrector.SetNumberOfThreads(8)
    # Obtains a simple mask with data from the image (need to validate this)
    # img_itk, insideValue, outsideValue, #histograms, MaskOutput, Mask value
    img_mask = sitk.OtsuThreshold(img_itk, 0, 1, 200)

    # ********* Shrink image (to make it take less time) *************
    # Casting both, the image and the mask to the same factor
    sm_img = sitk.Shrink(img_itk, [int(shrink_factor)]*img_itk.GetDimension())
    sm_mask = sitk.Shrink(img_mask, [int(shrink_factor)]*img_itk.GetDimension())
    sm_img = sitk.Cast(sm_img, sitk.sitkFloat32)  # N4 needs floats

    corrector.SetConvergenceThreshold(.0065)  # Lower is better and slower (around .006)
    img_norm = corrector.Execute(sm_img, sm_mask)
    return img_norm


# ================= Only for testing =====================
if __name__ == '__main__':
    from os.path import join

    file_name = join('..','imagevisualizer', 'test_data', 'input','Case-0001', 'img_tra.nrrd')
    print('Reading image....')
    img_itk = sitk.ReadImage(file_name)

    print('Performing normalization ....')
    img_norm = n4itk(img_itk, shrink_factor=4)

    print('Plotting results....')
    viz_obj = MedicalImageVisualizer(disp_images=True)
    viz_obj.plot_img_and_ctrs_itk(img_itk, itk_ctrs=[], slices=SliceMode.MIDDLE, file_name_prefix='Original')
    viz_obj.plot_img_and_ctrs_itk(img_norm, itk_ctrs=[], slices=SliceMode.MIDDLE, file_name_prefix='Normalized')
