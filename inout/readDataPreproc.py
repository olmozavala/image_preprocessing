from img_viz.medical import MedicalImageVisualizer

from os.path import join, isdir
import numpy as np
from os import listdir
import SimpleITK as sitk

viz_obj = MedicalImageVisualizer()

def read_preproc_imgs_and_ctrs_np(input_folder, folders_to_read='all', avoid_patients=[],
                                  img_names=['roi_tra.nrrd'], ctr_names=['roi_mask']):
    """
    Reads images and contours from a 'Preproc' folder.
    :param input_folder: The path to the 'Preproc' folder where cases will be searched
    :param folders_to_read: Indicates which folder to read it can be 'all' or an array of integers
    :param avoid_patients: Indicates which folder to avoid (usefull when reading all cases) it should be an array
     of integers
    :param img_names: list with the name of the images we want to read
    :param ctr_names: list with the name of the ctrs we want to read
    :return:
    """


    # Obtain everything in itk format
    imgs_itk, ctrs_itk, sizes, start_pos, end_pos = \
        read_preproc_imgs_and_ctrs_itk(input_folder, folders_to_read=folders_to_read,
                                       avoid_patients=avoid_patients,
                                       img_names=img_names,
                                       ctr_names=ctr_names)

    # Trainsform to numpy array
    imgs_np = []
    ctrs_np = []
    for c_folder in imgs_itk:
        imgs_np.append([sitk.GetArrayFromImage(img_itk) for img_itk in imgs_itk])
        ctrs_np.append([sitk.GetArrayFromImage(ctr_itk) for ctr_itk in ctrs_itk])

    # Remove unused dimensions
    imgs_np = np.queeze(np.array(imgs_np))
    ctrs_np = np.queeze(np.array(ctrs_np))

    return imgs_np, ctrs_np, sizes, start_pos, end_pos



def read_preproc_imgs_and_ctrs_itk(input_folder, folders_to_read='all', avoid_patients=[],
                                   img_names=['roi_tra.nrrd'], ctr_names=['roi_mask']):
    """
    Reads images and contours from a 'Preproc' folder.
    :param input_folder: The path to the 'Preproc' folder where cases will be searched
    :param folders_to_read: Indicates which folder to read it can be 'all' or an array of integers
    :param avoid_patients: Indicates which folder to avoid (usefull when reading all cases) it should be an array
     of integers
    :param img_names: list with the name of the images we want to read
    :param ctr_names: list with the name of the ctrs we want to read
    :return:
    """

    # print("Reading data...........")
    # ================= Reading data ===================
    # Reading all folders
    folder_names = np.array([f for f in listdir(input_folder) if isdir(join(input_folder, f))])
    folder_names.sort()

    if not( isinstance(folders_to_read,str)):
        folder_names = [join(input_folder, 'Case-{num:04d}'.format(num=f)) for f in folders_to_read]
    else:
        if folders_to_read != 'all':
            print('Reading all the folders inside {}'.format(input_folder))

    tot_ctrs = len(ctr_names)
    tot_imgs = len(img_names)

    # Iterating over 'studies' folder
    passed_folders = 0
    for folder in folder_names:

        # Search folder inside the list of 'avoid patients'
        avoid_this_folder = np.any(np.array([folder.find(i) != -1 for i in avoid_patients]))
        if not(avoid_this_folder):
            try:
                temp_imgs = [] # Temporal variable that will hold the images of this patient
                temp_ctrs = [] # Temporal variable that will hold the contours of this patient
                for img_idx in range(tot_imgs):
                    temp_imgs.append(sitk.ReadImage(join(input_folder,folder,img_names[img_idx])))

                for ctr_idx in range(tot_ctrs):
                    temp_ctrs.append(sitk.ReadImage(join(input_folder,folder,ctr_names[ctr_idx])))

                if passed_folders == 0: # If first folder, then we initilize the variables with 0's
                    imgs_dims = temp_imgs[0].GetSize() # Assuming at least we read one image
                    all_sizes = np.zeros((len(folder_names), 3), dtype=np.int16)
                    all_starts = np.zeros((len(folder_names), 3), dtype=np.int16)
                    all_names = np.zeros((len(folder_names)), dtype=np.str)
                    all_imgcube = []
                    all_imgcontour = []

                all_sizes[passed_folders,:] = imgs_dims
                all_starts[passed_folders,:] = np.genfromtxt(join(input_folder,folder,'start_ROI.csv'))
                all_names[passed_folders] = folder

                all_imgcube.append(temp_imgs)
                all_imgcontour.append(temp_ctrs)
                # viz_obj.plot_img_and_ctrs_itk(temp_imgs[img_idx], temp_ctrs, slices=SliceMode.MIDDLE, title=F"Tra {folder}")

                passed_folders += 1
            except Exception as e:
                print("----- Failed for: ", folder, " ERROR: ", str(e))
            print("   {} done!".format(folder))

    return [all_imgcube[0:passed_folders], all_imgcontour[0:passed_folders], all_sizes[0:passed_folders,:], all_starts[0:passed_folders,:], all_names[0:passed_folders]]
