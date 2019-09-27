#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/AI_UM_RadOn/imagevisualizer"
# IMPORTANT!!!!! The input data is the same as the RADIOMICS folder

LOCAL='/media/osz1/DATA/DATA/RADIOMICS_and_MRI_Normalization/'
REMOTE='/CIFS/Biomarkers_Group/DATA_MRI/RADIOMICS_and_MRI_Normalization/'
CONFIG_PATH='/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/ProstateSegCNN/code/RUN/MRI_Normalization_Prostate'
MAIN_CONFIG='/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/ProstateSegCNN/code/config'
SRC_PATH='/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/ProstateSegCNN/code'

echo '############################ Copying configuration file ############################ '
cp Config_Normalization.py $MAIN_CONFIG/MainConfig.py
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------

# For renaming files or folders
find . -exec rename -f 's/ctr_pro/ctr_Prostate/' {} \+


#echo '############################ Synchronizing MIM_ORIGINAL ############################ '
#sudo rsync -r --info=progress2 $REMOTE/MIM_ORIGINAL /media/osz1/DATA_Old/ALL/RADIOMICS_and_MRI_Normalization/

#echo '############################ Reordering Folders ############################ '
#python $SRC_PATH/ReorderMIMFolders.py

#echo '############################ Sync Reordered folders ############################ '
#sudo rsync -r --info=progress2  $LOCAL/ORGANIZED_Normalization /CIFS/Biomarkers_Group/DATA_MRI/RADIOMICS_and_MRI_Normalization/

#echo '############################ Preprocessing ############################ '
#python $SRC_PATH/Preprocessing.py

#echo '############################ Sync Preproc folders ############################ '
#rsync -r --info=progress2   /media/osz1/DATA_Old/ALL/RADIOMICS_and_MRI_Normalization/PreprocNormmalization /CIFS/Biomarkers_Group/DATA_MRI/RADIOMICS_and_MRI_Normalization/

### --------- Generate images ------------------
#echo '############################ Making visualizations ############################ '
#python $SRC_PATH/Image_Contour_Visualizer.py

## --------- Synchronize output folders ------------------
#echo '############################ Sync Image folder with S drive ############################ '
#sudo rsync -r --info=progress2  $LOCAL/Input_MaskR-CNN_Normalization $REMOTE

