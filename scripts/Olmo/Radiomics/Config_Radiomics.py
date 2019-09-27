from preproc.constants import *

_cur_config_folder = 'RADIOMICS_and_MRI_Normalization'
_root_folder = '/media/osz1/DATA_Old/ALL/'

def getReorderFolderConfig():

    cur_config = {ReorderParams.mode: ReorderFolders.RADIOMICS,
                  ReorderParams.start_idx:1,   # Integer to start the numbering of the cases
                  ReorderParams.input_folder: F'{_root_folder}{_cur_config_folder}/MIM_ORIGINAL', # Root folder where the patients are
                  ReorderParams.output_folder: F'{_root_folder}{_cur_config_folder}/MIM_ORGANIZED_NO_DATE' # Root folder where the patients are
                  }
    return cur_config

def getPreprocessingConfig():
    '''These method creates configuration parameters for the preprocessing code.'''
    cur_config = {
        PreprocParams.input_folder: F'{_root_folder}{_cur_config_folder}/MIM_ORGANIZED_NO_DATE',
        PreprocParams.output_folder: F'{_root_folder}{_cur_config_folder}/Preproc',
        PreprocParams.mode: PreprocMode.RADIOMICS, #'RADIOMICS', 'PX', 'RP', 'GE', 'MASK_RCNN'
        PreprocParams.bias_correction: False, # Computes and saves using N4ITK bias correction
        PreprocParams.resample: False, # Computes and saves resampling the images to .5 .5 .5 mm
        PreprocParams.compute_roi_from_intersection: False, # Computes and saves the ROI obtained by the intersection of coronal, sag, ax
        'normalize': False, # The images are normalized from 0 to 1
        PreprocParams.smooth_ctrs: False, # Images are smoothed using a spheric mask and binary closing morphological operation
        PreprocParams.optical_flow_ctr_interpolation: False, # Interpolates contours using optical flow (only used if roi = True)
        PreprocParams.cases_to_process: [13]
    }

    return cur_config
