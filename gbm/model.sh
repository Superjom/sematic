source "../env.sh"
source "../utils.sh"

gbm() {
    cmd="python random_forest_model.py $LABELED_DATA_LABEL_PH  \
        ${DATA_PATH}/random_forest_model.predict \
        ${LABELED_DATA_PH}_cleaned_titles.subseq.sim \
        ${LABELED_DATA_PH}.tfidf \
        ${TEST_DATA_PH}_cleaned_titles.subseq.sim \
        ${TEST_DATA_PH}.tfidf"
    echo $cmd; $cmd;

    predict_ph=${DATA_PATH}/random_forest_model.predict 
    upload_ph=${predict_ph}.upload
    cd ..
    cmd="$PYPY gen_predict_res_format.py $predict_ph $TEST_DATA_PH $upload_ph"
    echo $cmd; $cmd
    cd linear_model 
    zip -r ${upload_ph}.zip $upload_ph
}

gbm
