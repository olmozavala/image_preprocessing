import inout.io_common
from img_viz.medical import MedicalImageVisualizer
from img_viz.constants import SliceMode

from os.path import join, isdir
import numpy as np
import inout.io_rt as io_rt
import SimpleITK as sitk
from preproc.constants import PreprocParams

viz_obj = MedicalImageVisualizer()

def validateFolders(folders_to_read, dicom_path, img_names, ctr_names):

    final_folders = []

    print("Validating folders.... be patient")
    folder_names = [join(dicom_path, 'Patient-{num:04d}'.format(num=f)) for f in folders_to_read]

    for idx, folder in enumerate(folder_names):
        try:
            for ctr in ctr_names:
                t = sitk.ReadImage(join(dicom_path,folder,ctr))

            for img in img_names:
                t = sitk.ReadImage(join(dicom_path,folder,img))

            final_folders.append(folders_to_read[idx])
        except Exception as e:
            print("Folder {} do not contains all the required images: {}".format(folder, e))

    return np.array(final_folders)


def read_rtstruct_mri_series(input_folder, ctr_folder_names, in_ctr_names, out_ctr_names, ref_img_itk, match_whole_word: list):
    """
    Reads MRI series and RT Dicom contours into sitk images
    :param input_folder: Path where to search the DICOM folder for contours
    :param ctr_folder_names: Name of the folders to look for
    :param in_ctr_names: Array Name of the contours we want to read (prostate, pz, gene, ...)
    :param out_ctr_names: List Output Name of the contours we want to read (prostate, pz, gene, ...)
    :param ref_img_itk:  Reference ITK image
    :param out_ctr_names: Str Array With the name of the contours used for saving (output)
    :param match_whole_word: Array that indicates if we should look for the whole contour name or as a regex
    :return:
    """
    tot_ctrs = len(out_ctr_names)

    orig_ctrs = []
    final_ctr_names = []

    for ctr_idx in range(tot_ctrs):
        try:
            all_ctrs, tmp_ctr_names = io_rt.getCtrAsItk(input_folder, ctr_folder_names, np.array([in_ctr_names[ctr_idx]]),
                                                        ref_img_itk, whole_word=match_whole_word[ctr_idx])
            for ii, c_ctr in enumerate(all_ctrs):
                orig_ctrs.append(c_ctr)
                # Here we decide if we use the original ctr name or the one inside the RT structure
                if out_ctr_names[ctr_idx] == PreprocParams.keep_ctr_name:
                    final_ctr_names.append(tmp_ctr_names[ii])
                else:
                    final_ctr_names.append(out_ctr_names[ctr_idx])

        except Exception as e:
            print("\t\t!!!!!WARNING for contour {ctr} {e} !!!!!!!!!!!!!!!!!!!".format(ctr=out_ctr_names[ctr_idx], e=e))

    return [orig_ctrs, final_ctr_names]


def read_dicom_mri_series(input_folder, mri_series_folder_name, out_mri_series_folder_name=[]):
    """
    Reads MRI series and RT Dicom contours into sitk images
    :param input_folder: Path to the DICOM folders files
    :param mri_series_folder_name: Array Names of the image folders we want to read
    :param out_mri_series_folder_name: Name of the images to output (only used when reading from preprocessing)
    :return:
    """

    tot_imgs = len(mri_series_folder_name)
    orig_imgs = []
    obt_mri_series_folder_name = []

    for img_idx in range(tot_imgs):
        try:
            final_folder = inout.io_common.get_earliest_mri_from_folder(mri_series_folder_name[img_idx], input_folder)
            f_names = sitk.ImageSeriesReader_GetGDCMSeriesFileNames(join(input_folder,final_folder))
            orig_imgs.append(sitk.ReadImage(f_names))
            if len(out_mri_series_folder_name) > 0:
                obt_mri_series_folder_name.append(out_mri_series_folder_name[img_idx])
        except Exception as e:
            print("\t\t!!!!!WARNING for img {}: {} !!!!!!!!!!!!!!!!!!!".format(mri_series_folder_name[img_idx],e))

    return [orig_imgs, obt_mri_series_folder_name]
