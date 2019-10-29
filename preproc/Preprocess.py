from img_viz.medical import MedicalImageVisualizer
from img_viz.constants import SliceMode

from preproc.constants import *

from preproc.NormalizationSchemes import n4itk
from preproc.PreprocADC import correct_adc_itk
from preproc.UtilsPreproc import *
from preproc.contour_smoothing import smoothContours

from inout.io_common import create_folder, write_itk_imgs
from inout.readData import read_dicom_mri_series, read_rtstruct_mri_series
import SimpleITK as sitk
import numpy as np
from os.path import join, exists


def preprocess_imgs_and_ctrs(input_folder, output_folder, resampling, img_names, ctr_names_orig, out_img_names, out_ctr_names_orig,
                    match_whole_w_ctr, normalize_imgs, ctr_folder_names, bias_corrections, fix_adc, options):
    """
    Generates nrrd files from dicom files. It does it for contours and series
    :param input_folder: Path to the DICOM files
    :param output_folder: Path to output nrrd files
    :param resampling: Array with 3 values indicating each resolution x,y,z
    :param img_names: Array Names of the images we want to transform
    :param ctr_names: Array Name of the contours we want to read
    :param out_img_names: Output img names
    :param out_ctr_names: Output ctr names
    :param match_whole_w_ctr: Bool array Indicate if we need to match the name of the contours exactly or as a RegEx
    :param normalize_imgs: Bool array Indicates if we need to perform percentile normalization to the images
    :param ctr_folder_names: Str Array With the name of the 'folder' names to search for contours
    :return:
    """
    viz_obj = MedicalImageVisualizer()

    ctr_names = ctr_names_orig.copy() # Patch to avoid problems with global variable
    out_ctr_names = out_ctr_names_orig.copy() # Patch to avoid problems with global variable

    create_folder(output_folder)

    # ******************** READS DATA *******************
    print('\tReading data....')

    [orig_imgs, final_img_names] = read_dicom_mri_series(input_folder, img_names, out_img_names)

    [orig_ctrs, final_ctr_names] = read_rtstruct_mri_series(input_folder,
                                                            ctr_folder_names=ctr_folder_names,
                                                            in_ctr_names=ctr_names,
                                                            out_ctr_names=out_ctr_names,
                                                            ref_img_itk=orig_imgs[0],
                                                            match_whole_word=match_whole_w_ctr)

    # Saves original images without bias correction
    write_itk_imgs(output_folder, 'img', orig_imgs, final_img_names)
    write_itk_imgs(output_folder, 'ctr', orig_ctrs, final_ctr_names)

    # ************** Correcting ADC intensities  *************
    for idx_fix_adc, c_fix_adc in enumerate(fix_adc):
        if c_fix_adc:
            print('\tFixing ADC, changing "black" values on original images ....')
            orig_imgs[idx_fix_adc] = correct_adc_itk(orig_imgs[idx_fix_adc])

    # ************** Normalize images (N4K bias correction) *************
    if options[PreprocParams.bias_correction]:
        print("\tBias correction.....")
        pretxt = 'img_n4k'
        for ii in range(len(orig_imgs)):
            if bias_corrections[ii]:
                # First try to read an existing file, if not, compute it
                file_name = join(output_folder,'{}_{}.nrrd'.format(pretxt, final_img_names[ii]))
                if exists(file_name):
                    print('\t\tReading previous n4k file...')
                    orig_imgs[ii] = sitk.ReadImage(file_name)
                else:
                    orig_imgs[ii] = n4itk(orig_imgs[ii])
        # Saving bias corrected images
        write_itk_imgs(output_folder, pretxt, orig_imgs, final_img_names)

    norm_perc = options[PreprocParams.normalize_percentiles]
    for idx_img in range(len(orig_imgs)):
        if normalize_imgs[idx_img]:
            print(F'\tNormalizing intensities ... {img_names[idx_img]}')
            orig_imgs[idx_img] = normalize_to_percentiles([orig_imgs[idx_img]], norm_perc[0], norm_perc[1])[0]

    # *********** Resample to [.5,.5,.5] and interpolate with optical flow ******************
    if options[PreprocParams.resample]:
        print("\tResampling .....")
        # viz_obj.plot_img_and_ctrs_itk(orig_imgs[0], orig_ctrs, slices=SliceMode.MIDDLE, title='Befor resampling')
        resampled_imgs, resampled_ctrs = reample_imgs_and_ctrs(orig_imgs, orig_ctrs, resampling)
        # viz_obj.plot_img_and_ctrs_itk(resampled_imgs[0], resampled_ctrs, slices=SliceMode.MIDDLE,title='RESAMPLED')
        if options[PreprocParams.optical_flow_ctr_interpolation]:
            print('\t\tOptical flow ....')
            resampled_ctrs = optical_flow_interpolation(resampled_ctrs)
        write_itk_imgs(output_folder, 'hr', resampled_imgs, final_img_names)
        write_itk_imgs(output_folder, 'hr_ctr', resampled_ctrs, final_ctr_names)

    # *********** Crop and normalize to 0 and 1 ************
    if options[PreprocParams.compute_roi_from_intersection]:
        print("\tCropping.....")
        roi_imgs, roi_ctrs, startROI_final, sizeROI_final = getCroppedIsotropicImgsOZ(resampled_imgs, resampled_ctrs)

        if options[PreprocParams.smooth_ctrs]:
            print("\t\tSmoothing ctrs.....")
            # viz_obj.plot_img_and_ctrs_itk(roi_ctrs[0], slices=SliceMode.MIDDLE,title='Before smoothing')
            roi_ctrs = smoothContours(roi_ctrs)
            # viz_obj.plot_img_and_ctrs_itk(roi_ctrs[0], slices=SliceMode.MIDDLE,title='After smoothing')

        # Saves the size and start position of the ROI, used when running the model
        np.savetxt(join(output_folder,'start_ROI.csv'),startROI_final)
        np.savetxt(join(output_folder,'size_ROI.csv'),sizeROI_final)
        # Save the roi images
        write_itk_imgs(output_folder, 'roi', roi_imgs, final_img_names)
        write_itk_imgs(output_folder, 'roi_ctr', roi_ctrs, final_ctr_names)

    # viz_obj.plot_imgs_and_ctrs_itk(roi_imgs, roi_ctrs, slices=SliceMode.MIDDLE, title='Final ROIs')
    print("DONE!!!!...")


def preprocess_imgs(input_folder, output_folder, resampling, img_names, out_img_names,
                    normalize_imgs, bias_corrections, fix_adc, options, save_imgs: bool):
    """
    Generates preprocessesd images only, this can be used when making classifications of the test
    dataset of the NN.
    :param input_folder: Path to the DICOM files
    :param output_folder: Path to output nrrd files
    :param resampling: Array with 3 values indicating each resolution x,y,z
    :param img_names: Array Names of the images we want to transform
    :param out_img_names: Output img names
    :param normalize_imgs: Bool array Indicates if we need to perform percentile normalization to the images
    :param save_imgs: Bool indicates if we need to save or not the output images
    :return:
    """
    viz_ob = MedicalImageVisualizer()
    create_folder(output_folder)

    # ******************** READS DATA *******************
    print('\tReading data....')

    [orig_imgs, final_img_names] = read_dicom_mri_series(input_folder, img_names, out_img_names)

    # Saves original images without bias correction
    if save_imgs:
        write_itk_imgs(output_folder, 'img', orig_imgs, final_img_names)

    if len(fix_adc) == len(orig_imgs):
        for idx_fix_adc, c_fix_adc in enumerate(fix_adc):
            if c_fix_adc:
                print('\tFixing ADC, changing "black" values on original images ....')
                orig_imgs[idx_fix_adc] = correct_adc_itk(orig_imgs[idx_fix_adc])
    else:
        print('\tNone ADC img is being fixed')

    # ************** Normalize images (N4K bias correction) *************
    if options[PreprocParams.bias_correction]:
        print("\tBias correction.....")
        pretxt = 'img_n4k'
        for ii in range(len(orig_imgs)):
            if bias_corrections[ii]:
                # First try to read an existing file, if not, compute it
                orig_imgs[ii] = n4itk(orig_imgs[ii])
        # Saving bias corrected images
        if save_imgs:
            write_itk_imgs(output_folder, pretxt, orig_imgs, final_img_names)

    norm_perc = options[PreprocParams.normalize_percentiles]
    for idx_img in range(len(orig_imgs)):
        if normalize_imgs[idx_img]:
            print(F'\tNormalizing intensities ... {img_names[idx_img]}')
            orig_imgs[idx_img] = normalize_to_percentiles([orig_imgs[idx_img]], norm_perc[0], norm_perc[1])[0]

    # *********** Resample to [.5,.5,.5] and interpolate with optical flow ******************
    if options[PreprocParams.resample]:
        print("\tResampling .....")
        # viz_obj.plot_img_and_ctrs_itk(orig_imgs[0], slices=SliceMode.MIDDLE,title='Befor resampling')
        resampled_imgs, _= reample_imgs_and_ctrs(orig_imgs, [], resampling)
        # viz_obj.plot_img_and_ctrs_itk(resampled_imgs[0], slices=SliceMode.MIDDLE,title='RESAMPLED')
        if save_imgs:
            write_itk_imgs(output_folder, 'hr', resampled_imgs, final_img_names)

    # *********** Crop and normalize to 0 and 1 ************
    if options[PreprocParams.compute_roi_from_intersection]:
        print("\tCropping.....")
        roi_imgs, _, startROI_final, sizeROI_final = getCroppedIsotropicImgsOZ(resampled_imgs, [])

        # Saves the size and start position of the ROI, used when running the model
        np.savetxt(join(output_folder,'start_ROI.csv'),startROI_final)
        np.savetxt(join(output_folder,'size_ROI.csv'),sizeROI_final)
        # Save the roi images
        if save_imgs:
            write_itk_imgs(output_folder, 'roi', roi_imgs, final_img_names)

    return orig_imgs, resampled_imgs, roi_imgs
