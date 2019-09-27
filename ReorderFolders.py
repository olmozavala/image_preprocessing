import shutil
import os
from os.path import join

from config.MainConfig import getReorderFolderConfig
from reorder.ReorderMIMFolders import ReorderMIMFolders

from preproc.constants import ReorderFolders, ReorderParams


def main():
    """
    Main function, retrieves the configuration parameters from MainConfig and fills the proper options depending
    on the type of reordering we are using.
    :return:
    """
    input_params = getReorderFolderConfig()
    root_folder = input_params[ReorderParams.input_folder]
    output_folder = input_params[ReorderParams.output_folder]
    start_idx = input_params[ReorderParams.start_idx]
    f_type = input_params[ReorderParams.mode]

    print('Params: \n root folder: {}  \n folder type: {} \n start folder: {}'.format(root_folder, f_type, start_idx))

    global_reorder_obj = ReorderMIMFolders(src_folder=root_folder, dst_folder=output_folder, start_idx=start_idx)
    if f_type == ReorderFolders.PX:
        reorder_px(global_reorder_obj)
    if f_type == ReorderFolders.GE:
        reorder_ge(global_reorder_obj)
    if f_type == ReorderFolders.RADIOMICS:
        reorder_radiomics(global_reorder_obj)
    if f_type == ReorderFolders.RP:
        reorder_rp(global_reorder_obj)
    if f_type == ReorderFolders.MASKRCNN:
        reoder_maskrcnn(global_reorder_obj)
    if f_type == ReorderFolders.RAD_PLANS:
        reorder_basic(global_reorder_obj)
    if f_type == ReorderFolders.MOVE_ALL:
        reorder_every_folder(src_folder=root_folder, output_folder=output_folder, start_idx=start_idx)
    if f_type == ReorderFolders.PATCH_MASKRCNN:
        reorder_add_folder_per_image(src_folder=root_folder, output_folder=output_folder, start_idx=start_idx)


def reorder_rp(reorder_obj):
    """
    What this code does is separate the patients in their own folders, save a 'corresponding' LUT and
    removes the names from the folders.
    """
    reorder_obj.orig_folder_names = [['T2.AX.SFOV', '_AX.T2'], ['T2.COR.SFOV', '_COR.T2'],
                                     ['Sag.T2', '_SAG.T2', 'T2.SAG.SFOV', 'Sag.T2..RTr.PROPELLER'],
                                     ['Apparent', 'ADC'], ['BVAL'],
                                     ['olmo'],
                                     ['LAVA']]

    reorder_obj.new_folder_names = ['T2_TRANSVERSAL', 'T2_CORONAL', 'T2_SAGITTAL',
                                    'ADC_TRANSVERSAL', 'BVAL_TRANSVERSAL', 'CONTOURS', 'DCE']

    reorder_obj.organize_folders()


def reorder_radiomics(reorder_obj):
    """
    What this code does is separate the patients in their own folders, save a 'corresponding' LUT and
    removes the names from the folders.
    """
    reorder_obj.orig_folder_names = [['T2.FSE.AX', r'_Ax\S*T2_', '_Ax.t2', 't2.fse.ax', 'T2'],
                                     ['ADC', 'Apparent'],
                                     ['BVAL', 'DIFF.B'],
                                     ['Gene']]
    reorder_obj.new_folder_names = ['T2_TRANSVERSAL', 'ADC_TRANSVERSAL',
                                    'BVAL_TRANSVERSAL', 'CONTOURS']
    reorder_obj.organize_folders()


def reorder_ge(reorder_obj):
    # These are the ONLY FOLDERS we will move.
    reorder_obj.orig_folder_names = [
        [r'Aligned\*T2.FSE.AX', r'Aligned\*T2.AX.SFOV', 'T2.AX.SFOV', 'T2.FSE.AX', r'_Ax\S*T2_', 'T2.FSE.FS.AX',
         'T2.FSU.AX', 't2.fse.ax', 'Ax.T2.frFSE.Propeller'],
        ['T2.COR.SFOV', '.COR', r'_Cor\S*T2_', 't2.cor.sfov_', 'Cor.T2.frFSE.Propeller'],
        ['T2.SAG.SFOV', '.SAG', r'_Sag\S*T2_', '_Sag.T2', 'Sag.T2..RTr.PROPELLER', 't2.sag.sfov'],
        ['Apparent'],
        ['1000', 'BVAL'],
        [r'RTst\S*atlas.CNN', r'RTst\S*atlas', r'RTst\S*Atlas', r'RTst\S*MUSCLE', r'RTst\S*HRS',
         r'RTst\S*Prostate', r'RTst\S*PROSTATE', r'RTst\S*olmo', r'RTst\S*LAVA', r'RTst\S*Contours']]

    reorder_obj.new_folder_names = ['T2_TRANSVERSAL', 'T2_CORONAL', 'T2_SAGITTAL', 'ADC_TRANSVERSAL',
                                    'BVAL_TRANSVERSAL',
                                    'CONTOURS']
    reorder_obj.replace_chars = 15
    reorder_obj.organize_folders()


def reorder_px(reorder_obj) -> None:
    reorder_obj.orig_folder_names = [[r'tse.tra\S*00001', r'tse.tra\S*00000'], [r'tse.cor\S*00001', r'tse.cor\S*00000'],
                                     [r'tse.sag\S*00001', r'tse.sag\S*00000'],
                                     [r'Aligned.MR\S*ADC', r'ep2d.\S*ADC', 'ADC', 'Apparent'],
                                     [r'Aligned.MR\S*BVAL', r'ep2d.\S*BVAL', 'BVAL'],
                                     [r'Atlas.CNN', 'Atlas', 'atlas.CNN', 'atlas', 'Prostate2.0', 'Prostate-2',
                                      'prostate02_n1',
                                      'prostate2_n1', 'prostate_n1', 'Atlas']]

    reorder_obj.new_folder_names = ['T2_TRANSVERSAL', 'T2_CORONAL', 'T2_SAGITTAL',
                                    'ADC_TRANSVERSAL', 'BVAL_TRANSVERSAL', 'CONTOURS']
    reorder_obj.organize_folders()

    # Rename all folders to 'Case'
    # if system() == 'Linux':
    #     cmd = "find -maxdepth 1 {} -type d -name '*' | rename 's/ProstateX/Case/g'".format(reorder_obj.output_folder)
    #     print('*** Renaming folders with: {}'.format(cmd))
    #     os.system(cmd)


def reoder_maskrcnn(reorder_obj) -> None:
    """
    Similar than the other ones. In this case it only searches one plane (Axial) and a set of contours
    :param reorder_obj: An object of type ReorderMIMFolders used to reorder the folders
    """

    reorder_obj.orig_folder_names = [['tse.tra', 'T2.FSE.AX', 't2.fse.ax', 'AX.T2', 'T2.022317', 'MR', ''],
                                     ['Multi.struct', 'multi.struct', 'MASK']]
    reorder_obj.new_folder_names = ['T2_TRANSVERSAL', 'CONTOURS']
    reorder_obj.organize_folders()


def reorder_basic(reorder_obj) -> None:
    """
    Reorders the folders, it only searches for MR and RTst to differentiate between  folders
    """
    reorder_obj.orig_folder_names = [['MR'], ['RTst']]
    reorder_obj.new_folder_names = ['T2_TRANSVERSAL', 'CONTOURS']
    reorder_obj.organize_folders()


def reorder_every_folder(src_folder, output_folder, start_idx):
    """
    In this case we move EVERY folder inside the 'dates MIM folder' as a new case.
    """
    folder_txt = 'Case'
    final_folder_names = 'T2_TRANSVERSAL'
    original_date_folders = os.listdir(src_folder)

    # Iterate over all the source folders (dates of MIM)
    c_idx = start_idx
    for c_date_folder in original_date_folders:
        print('******************************* {} *************************************'.format(c_date_folder))
        all_folders_in_date = os.listdir(join(src_folder, c_date_folder))
        for idx_cf, c_folder in enumerate(all_folders_in_date):  # Iterate folders we are searching
            curr_dst_folder = join('%s-%04d' % (folder_txt, c_idx))
            src = join(src_folder, c_date_folder, c_folder)
            dst = join(output_folder, curr_dst_folder, final_folder_names)
            print(src)
            print(dst)
            print('----------')
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            c_idx += 1


def reorder_add_folder_per_image(src_folder, output_folder, start_idx):
    """ This function was only created to move images inside the 'images 'folder. To be used by
    Adrian on the MaskRCNN"""
    all_imgs = os.listdir(src_folder)
    c_idx = start_idx
    for c_img in all_imgs:
        print(F'***** {c_img} *****')
        src = join(src_folder, c_img)
        dst = join(output_folder, str(c_idx), 'images', c_img)
        print(src)
        print(dst)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        os.makedirs(join(output_folder, str(c_idx), 'images'))
        shutil.copy(src, dst)
        # shutil.move(src, dst)
        c_idx += 1


if __name__ == '__main__':
    main()
