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

func_preprocessing(){
    FOLDER=$1
    REMOTE=$2
    LOCAL=$3
    CONFIG_PATH=$4
    MAIN_CONFIG=$5
    SRC_PATH=$6
    echo '######### Synchronizing MIM_ORIGINAL #####'
    rsync -r --info=progress2  $REMOTE/MIM_ORIGINAL $LOCAL
    echo '######### Fixing MIM names ###############'
    func_fix_folder_names $LOCAL

    echo '######### Copying configuration file #####'
    cp Preproc_$FOLDER.py $MAIN_CONFIG/MainConfig.py

    echo '######### Reordering Folders #############'
    python $SRC_PATH/ReorderMIMFolders.py
    echo '######## Sync Reordered folders ###########'
    sudo rsync -r --info=progress2  $LOCAL/MIM_ORGANIZED_NO_DATE $REMOTE

    echo '######### Preprocessing Folders #############'
    python $SRC_PATH/ReorderMIMFolders.py
    echo '######### Sync Preproc folders ###########'
    rsync -r --info=progress2 $LOCAL/Preproc $REMOTE
}

SRC_PATH='/media/osz1/DATA/Dropbox/UMIAMI/WorkUM/PreprocessData/'
CONFIG_PATH="${SRC_PATH}/RUN_OZ/Cervix_Plan_Structures/"
MAIN_CONFIG="${SRC_PATH}/config"

# %%%%%%%%%%%%%%%%%%%%%%%       PREPROCESSING         %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
FOLDER='Cervix_Plan_Structures'
REMOTE=/CIFS/Biomarkers_Group/DATA_MRI/
LOCAL=/media/osz1/DATA/DATA/
LOCAL_MIRROR=/media/osz1/DATA_Old/ALL/
IMAGES=/media/osz1/DATA/DATA/$FOLDER/IMAGES

cp Config_Cervix.py $MAIN_CONFIG/MainConfig.py

#echo '############################ Synchronizing MIM_ORIGINAL_PILOT_ONLY ############################ '
#rsync -r --info=progress2 $REMOTE/$FOLDER/MIM_ORIGINAL $LOCAL/$FOLDER/
#
#echo '############################ Fixing names from MIM ORIGINAL ############################ '
#func_fix_folder_names $LOCAL/$FOLDER
#
#echo '############################ Making internal link ############################ '
#ln -s $LOCAL/$FOLDER/ $LOCAL_MIRROR
#
echo '############################ Reordering Folders ############################ '
python $SRC_PATH/ReorderFolders.py

echo '############################ Preprocessing ############################ '
python $SRC_PATH/Preprocessing.py

