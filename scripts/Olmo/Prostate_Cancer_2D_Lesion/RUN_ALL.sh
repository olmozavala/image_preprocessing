#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/AI_UM_RadOn/imagevisualizer"
func_fix_folder_names(){
    LOCAL=$1
    # ------- Variables and print ------
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/, /\^/' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/ /\^/' {} \+`
    `find $LOCAL/MIM_ORIGINAL -exec rename -f 's/,\^/\^/' {} \+`
    `find $LOCAL/MIM_ORIGINAL -name '*, *' -type d -exec rm -R {} \;`
    `find $LOCAL/MIM_ORIGINAL -name '* *'  -type d -exec rm -R {} \;`
    `find $LOCAL/MIM_ORIGINAL -name '*,\^*'-type d -exec rm -R {} \;`
}


FOLDER='PX'
RUN_FOLDER='ProstatePZ_Segmentation'
SRC_PATH='/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/PreprocessData/'
CONFIG_PATH="${SRC_PATH}/RUN_OZ/${RUN_FOLDER}/"
MAIN_CONFIG="${SRC_PATH}/config"

REMOTE=/CIFS/Biomarkers_Group/DATA_MRI/
# These are used for PX or merged
LOCAL=/media/osz1/DATA/DATA/
LOCAL_MIRROR=/media/osz1/DATA_Old/ALL/
# These are used for RP
#LOCAL=/media/osz1/DATA_Old/ALL/
#LOCAL_MIRROR=/media/osz1/DATA/DATA/

echo '############################ Copying configuration file ############################ '
#cp Config_RP.py $MAIN_CONFIG/MainConfig.py
#cp Config_PX.py $MAIN_CONFIG/MainConfig.py

#echo '############################ Synchronizing MIM_ORIGINAL_PILOT_ONLY ############################ '
#rsync -r --info=progress2 $REMOTE/$FOLDER/MIM_ORIGINAL $LOCAL/$FOLDER/

#echo '############################ Fixing names from MIM ORIGINAL ############################ '
#func_fix_folder_names $LOCAL/$FOLDER

#echo '############################ Making internal link ############################ '
#ln -s $LOCAL/$FOLDER/ $LOCAL_MIRROR

#echo '############################ Reordering Folders ############################ '
#python $SRC_PATH/ReorderMIMFolders.py

#echo '############################ Sync Reordered folders ############################ '
#sudo rsync -r --info=progress2  $LOCAL/$FOLDER/MIM_ORGANIZED_NO_DATE $REMOTE/$FOLDER/

#echo '############################ Preprocessing ############################ '
#python $SRC_PATH/Preprocessing.py

#echo '############################ Sync Preproc folders ############################ '
#sudo rsync -r --info=progress2  $LOCAL/$FOLDER/Preproc_Pilot $REMOTE/$FOLDER/
