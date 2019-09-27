from preproc.PreprocDCE import preprocDCE
from preproc.Preprocess import *
from preproc.constants import PreprocMode, PreprocParams
from config.MainConfig import getPreprocessingConfig
from utils.strutils import get_id_number_from_cases

from os.path import join


def main():
    preproc_options = getPreprocessingConfig()

    preproc_mode = preproc_options[PreprocParams.mode]
    input_folder = preproc_options[PreprocParams.input_folder]
    output_folder = preproc_options[PreprocParams.output_folder]
    cases = preproc_options[PreprocParams.cases_to_process]
    print(preproc_options)

    if preproc_mode == PreprocMode.PX:
        px(preproc_options, input_folder, output_folder, cases)
    if preproc_mode == PreprocMode.GE:
        px(preproc_options, input_folder, output_folder, cases)
    if preproc_mode == PreprocMode.RADIOMICS:
        radiomics(preproc_options, input_folder, output_folder, cases)
    if preproc_mode == PreprocMode.RP:
        rp(preproc_options, input_folder, output_folder, cases)
    if preproc_mode == PreprocMode.MASKRCNN:
        preproc_maskrcnn(preproc_options, input_folder, output_folder, cases)
    if preproc_mode == PreprocMode.CERVIX:
        cervix(preproc_options, input_folder, output_folder, cases)
    if preproc_mode == PreprocMode.PANCREAS:
        pancreas(preproc_options, input_folder, output_folder, cases)


def preproc_maskrcnn(preproc_options, input_folder, output_folder, cases):
    """
    Preprocess the folder (from DICOM to nrrd), only contours and T2
    :param preproc_options: A dictionary with all the preprocessing options
    :param input_folder:  Input folder, where the folders for each case are stored
    :param output_folder: Where the preprocessed files will be stored
    :param cases: An array of integers with the cases that need to be proccessed. If can be 'all'
    :return:
    """

    output_folder = output_folder

    resampling = [0.5, 0.5, 0.5]

    # First 3 images MUST be tra, cor y sag
    img_names = ['T2_TRANSVERSAL']
    out_img_names = ['tra']
    normalize_img = [True]
    bias_correction = [True]
    fix_adc = [False]

    ctr_folder_names = ['CONTOURS']
    ctr_names = ['prostate', 'Muscle', 'Femur|Fumor', 'Bladder', 'GM']
    match_whole_w_ctr = [True, True, False, True, True]
    out_ctr_names = ['pro', 'Muscle', 'Femur', 'Bladder', 'GM']

    common_iteration(preproc_options, input_folder, output_folder, cases, resampling, img_names, out_img_names,
                     normalize_img, bias_correction, fix_adc, ctr_folder_names, ctr_names, match_whole_w_ctr,
                     out_ctr_names)


def pancreas(preproc_options, input_folder, output_folder, cases):
    """
    Preprocess the folder (from DICOM to nrrd), only contours and T2
    :param preproc_options: A dictionary with all the preprocessing options
    :param input_folder:  Input folder, where the folders for each case are stored
    :param output_folder: Where the preprocessed files will be stored
    :param cases: An array of integers with the cases that need to be proccessed. If can be 'all'
    :return:
    """

    output_folder = output_folder
    resampling = [0.5, 0.5, 0.5]

    # First 3 images MUST be tra, cor y sag
    img_names = ['T2_TRANSVERSAL']
    out_img_names = ['tra']
    normalize_img = [True]
    bias_correction = [True]
    fix_adc = [False]

    ctr_folder_names = ['CONTOURS']
    ctr_names = ['GTVp', 'Liver', 'Stomach', 'Bowel', 'Duodenum', 'Skin', 'Pancreas', 'SpinalCord', 'KidneyBilat']
    match_whole_w_ctr = [True for x in ctr_names]
    out_ctr_names = ['GTVp', 'Liver', 'Stomach', 'Bowel', 'Duodenum', 'Skin', 'Pancreas', 'SpinalCord', 'KidneyBilat']

    common_iteration(preproc_options, input_folder, output_folder, cases, resampling, img_names, out_img_names,
                     normalize_img, bias_correction, fix_adc, ctr_folder_names, ctr_names, match_whole_w_ctr,
                     out_ctr_names)


def cervix(preproc_options, input_folder, output_folder, cases):
    """
    Preprocess the folder (from DICOM to nrrd), only contours and T2
    :param preproc_options: A dictionary with all the preprocessing options
    :param input_folder:  Input folder, where the folders for each case are stored
    :param output_folder: Where the preprocessed files will be stored
    :param cases: An array of integers with the cases that need to be proccessed. If can be 'all'
    :return:
    """

    output_folder = output_folder

    resampling = [0.5, 0.5, 0.5]

    # First 3 images MUST be tra, cor y sag
    img_names = ['T2_TRANSVERSAL']
    out_img_names = ['tra']
    normalize_img = [True]
    bias_correction = [True]
    fix_adc = [False]

    ctr_folder_names = ['CONTOURS']
    ctr_names = ['GTV', 'Uterus', 'Sigmoid', 'Bone', 'Bladder', 'Rectum', 'Parametrium', 'Vagina', 'Meso', 'Femur']
    match_whole_w_ctr = [False, True, True, False, True, True, True, True, False, True]
    out_ctr_names = ['GTV', 'Uterus', 'Sigmoid', 'Bone_Marrow', 'Bladder', 'Rectum', 'Parametrium', 'Vagina',
                     'Mesorectum', 'Femur']

    common_iteration(preproc_options, input_folder, output_folder, cases, resampling, img_names, out_img_names,
                     normalize_img, bias_correction, fix_adc, ctr_folder_names, ctr_names, match_whole_w_ctr,
                     out_ctr_names)


def px(preproc_options, input_folder, output_folder, cases):
    """
    Preprocess the GE folder (from DICOM to nrrd)
    :param preproc_options: A dictionary with all the preprocessing options
    :param input_folder:  Input folder, where the folders for each case are stored
    :param output_folder: Where the preprocessed files will be stored
    :param cases: An array of integers with the cases that need to be proccessed. If can be 'all'
    :return:
    """

    output_folder = output_folder

    resampling = [0.5, 0.5, 0.5]

    # First 3 images MUST be tra, cor y sag
    img_names = ['T2_TRANSVERSAL', 'T2_CORONAL', 'T2_SAGITTAL', 'ADC_TRANSVERSAL', 'BVAL_TRANSVERSAL']
    out_img_names = ['tra', 'cor', 'sag', 'adc', 'bval']
    normalize_img = [True, True, True, False, False]
    bias_correction = [True, True, True, False, False]
    fix_adc = [False, False, False, True, False]

    ctr_folder_names = ['CONTOURS']
    ctr_names = [r'prostate', 'PZ',
                 r'^ROI[.]*[-_]+\d+[-_]+1_*',
                 r'^ROI[.]*[-_]+\d+[-_]+2_*',
                 r'^ROI[.]*[-_]+\d+[-_]+3_*',
                 r'^ROI[.]*[-_]+\d+[-_]+4_*',
                 r'^ROI[.]*[-_]+\d+[-_]+5_*',
                 r'^ROI[.]*[-_]+\d+[-_]+F_\S*',
                 r'^ROI[.]*[-_]+\d+[-_]+T_\S*',
                 ]
    # re.search('^ROI[.]*[-_]+\d+_3_*', 'ROI_3_4_PZ'
    match_whole_w_ctr = [True, True, False, False, False, False, False, False, False]
    out_ctr_names = ['pro', 'pz', 'lesion_1', 'lesion_2', 'lesion_3', 'lesion_4', 'lesion_5',
                     'lesion_F', 'lesion_T']

    common_iteration(preproc_options, input_folder, output_folder, cases, resampling, img_names, out_img_names,
                     normalize_img, bias_correction, fix_adc, ctr_folder_names, ctr_names, match_whole_w_ctr,
                     out_ctr_names)


def radiomics(preproc_options, input_folder, output_folder, cases):
    """
    Preprocess the Radiomics folder folder (from DICOM to nrrd)
    :param preproc_options: A dictionary with all the preprocessing options
    :param input_folder:  Input folder, where the folders for each case are stored
    :param output_folder: Where the preprocessed files will be stored
    :param cases: An array of integers with the cases that need to be proccessed. If can be 'all'
    :return:
    """

    output_folder = output_folder

    img_names = ['T2_TRANSVERSAL', 'ADC_TRANSVERSAL', 'BVAL_TRANSVERSAL']
    out_img_names = ['t2_tra', 'adc', 'bval']
    normalize_img = [False, False, False]
    bias_correction = [False, False, False]
    fix_adc = [False, False, False]
    resampling = [0.5, 0.5, 0.5]

    ctr_folder_names = ['CONTOURS']
    ctr_names = ['GM', 'Muscle', r'^M0\S+', r'^GM\S+', r'^GB\S+', 'Prostate', 'PZ', 'NAPZ', 'NATZ']
    match_whole_w_ctr = [True, True, False, False, False, False, True, True, True]
    out_ctr_names = ['GM', 'GM', PreprocParams.keep_ctr_name, PreprocParams.keep_ctr_name, PreprocParams.keep_ctr_name, 'pro', 'pz', 'NAPZ',
                     'NATZ']  # Using FROMCTR should copy the original name

    common_iteration(preproc_options, input_folder, output_folder, cases, resampling, img_names, out_img_names,
                     normalize_img, bias_correction, fix_adc, ctr_folder_names, ctr_names, match_whole_w_ctr,
                     out_ctr_names)


def rp(preproc_options, input_folder, output_folder, cases):
    """
    Preprocess the Radiomics folder folder (from DICOM to nrrd)
    :param preproc_options: A dictionary with all the preprocessing options
    :param input_folder:  Input folder, where the folders for each case are stored
    :param output_folder: Where the preprocessed files will be stored
    :param cases: An array of integers with the cases that need to be proccessed. If can be 'all'
    all the files
    :return
    """

    output_folder = output_folder

    resampling = [0.5, 0.5, 0.5]

    # READ: First 3 images MUST be tra, cor y sag
    img_names = ['T2_TRANSVERSAL', 'T2_CORONAL', 'T2_SAGITTAL', 'ADC_TRANSVERSAL', 'BVAL_TRANSVERSAL']
    out_img_names = ['tra', 'cor', 'sag', 'adc', 'bval']
    fix_adc = [False, False, False, False, False]
    normalize_img = [True, True, True, False, True]

    ctr_folder_names = ['CONTOURS']
    ctr_names = ['Prostate', 'PZ']
    max_num_roi = 15  # How many ROI do we want to search for
    ctr_names.extend(['^ROI-{}'.format(i) for i in range(max_num_roi)])  # For all ROI
    print(ctr_names)
    match_whole_w_ctr = [False, False]
    match_whole_w_ctr.extend([False for i in range(max_num_roi)])
    out_ctr_names = ['pro', 'pz']
    out_ctr_names.extend(['lesion_{}'.format(i) for i in range(max_num_roi)])

    # These are dependent on previous selection
    bias_correction = [True, True, True, False, False]

    common_iteration(preproc_options, input_folder, output_folder, cases, resampling, img_names, out_img_names,
                     normalize_img, bias_correction, fix_adc, ctr_folder_names, ctr_names, match_whole_w_ctr,
                     out_ctr_names)


def common_iteration(preproc_options, input_folder, output_folder, cases, resampling, img_names, out_img_names,
                     normalize_img, bias_correction, fix_adc, ctr_folder_names, ctr_names, match_whole_w_ctr,
                     out_ctr_names):

    assert len(ctr_names) == len(match_whole_w_ctr), 'Different number of contour names and boolean matching variables'
    assert len(ctr_names) == len(out_ctr_names), 'Different number of contour names and out names'

    if isinstance(cases, str):
        if cases == 'all':
            cases = get_id_number_from_cases(input_folder)

    print("============ PREPROCESSING ===============")
    print(F'From {input_folder} to {output_folder}')
    for pat_num in cases:
        try:
            dir_pat = 'Case-{num:04d}'.format(num=pat_num)
            input_path = join(input_folder, dir_pat)
            output_path = join(output_folder, dir_pat)
            print(F"********Case {pat_num:04d} ********")
            preprocess_imgs_and_ctrs(input_path, output_path, resampling, img_names,
                                     ctr_names, out_img_names, out_ctr_names,
                                     match_whole_w_ctr, normalize_img, ctr_folder_names,
                                     bias_correction, fix_adc, preproc_options)
        except Exception as e:
            print(F"!!!!!!! Failed for patient {pat_num:04d} Error: {e} !!!!!!!!!!!!")


if __name__ == '__main__':
    main()
