from preproc.constants import *

_cur_config_folder = 'Cervix_Plan_Structures'
_root_folder = F'/media/osz1/DATA/DATA/{_cur_config_folder}/'


def getReorderFolderConfig():
    cur_config = {ReorderParams.mode: ReorderFolders.MASKRCNN, # Type of folder to reorder: 'Mask_RCNN' 'RADIOMICS', 'PX', 'RP', 'GE'
                  ReorderParams.start_idx:1,   # Integer to start the numbering of the cases
                  ReorderParams.input_folder: F'{_root_folder}/MIM_ORIGINAL',
                  ReorderParams.output_folder: F'{_root_folder}/MIM_ORGANIZED_NO_DATE'
                  }
    return cur_config


def getPreprocessingConfig():
    '''These method creates configuration parameters for the preprocessing code.'''
    cur_config = {
        PreprocParams.input_folder: F'{_root_folder}/MIM_ORGANIZED_NO_DATE',
        PreprocParams.output_folder: F'{_root_folder}/Preproc',
        PreprocParams.mode: PreprocMode.RAD_PLANS, #'RADIOMICS', 'PX', 'RP', 'GE', 'MASK_RCNN'
        PreprocParams.bias_correction: False, # Computes and saves using N4ITK bias correction
        PreprocParams.resample: False, # Computes and saves resampling the images to .5 .5 .5 mm
        PreprocParams.compute_roi_from_intersection: False, # Computes and saves the ROI obtained by the intersection of coronal, sag, ax
        PreprocParams.normalize_percentiles: [1,99], # The images are normalized from 0 to 1 using values at percentile 1 and 99
        PreprocParams.smooth_ctrs: False, # Images are smoothed using a spheric mask and binary closing morphological operation
        PreprocParams.optical_flow_ctr_interpolation: False, # Interpolates contours using optical flow (only used if roi = True)
        PreprocParams.cases_to_process: 'all'
    }

    return cur_config
