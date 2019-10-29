from enum import Enum

class PreprocMode(Enum):
    """ Enum to select the different types of slices"""
    PX = 'PX'
    GE = 'GE'
    RADIOMICS = 'RADIOMICS' # Radiomics and MRI normalization
    RP = 'RP'
    MASKRCNN = 'Mask-RCNN'
    PANCREAS = 'Pancreas'
    CERVIX = 'Cervix'


class ReorderFolders(Enum):
    """ Enum to select the different types folders configuration to choose """
    PX = 1  # PX project (sequential cases and standard names)
    GE = 2  # GE project (sequential cases and standard names)
    RADIOMICS = 3  # Radiomics and MRI normalization
    RP = 4  #
    MASKRCNN = 5
    PANCREAS = 6
    RAD_PLANS = 7
    MOVE_ALL = 8  # Use this mode if you want to move EVERY single folder inside MIM dates folder as a new
    # case. not normally used
    PATCH_MASKRCNN = 9  # TODO what is this doing


class ReorderParams(Enum):
    """Contains the possible parameters to reorder a folder"""
    mode = 1
    start_idx = 2
    input_folder = 3
    output_folder = 4


class PreprocParams(Enum):
    """Contains the possible parameters to preprocess a folder"""
    input_folder = 1
    output_folder = 2
    mode = 3  # The database configuration we will use (is different for PX, GE, RP, etc.)
    # Indicate if we will perform bias correction on the images. If False, then no bias correction is performed,
    # if True, then each configuration contains to which images are we performing bias correction
    bias_correction = 4
    resample = 5  # If we are resampling the images and to which resolutions
    normalize_percentiles = 6  # The percentiles to perform normalization normal [1,99]
    smooth_ctrs = 7  # If we are going to smooth contours (boolean). They are smoothed with a sphere of radius 5
    optical_flow_ctr_interpolation = 8  # Optical flow interpolation when resampling contours between every two slices
    cases_to_process = 9  # An np array with the cases to process
    compute_roi_from_intersection = 10  # IN this case a ROI is obtained by intersecting the first 3 images
    keep_ctr_name = 11  # Its used to keep the name of the ctr from its original rt structure name

class NormParams(Enum):
    """Contains the parameters for a 1D normalization"""
    min_max =1
