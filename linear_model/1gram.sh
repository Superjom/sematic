source "../env.sh"
source "../utils.sh"

# works for 1gram and 2gram
replace_word_with_wid() {
    seg_ph=$1
    dic_ph=$2
    wid_ph=${seg_ph}_wid
        cmd="$PYPY replace_word_with_wid.py $dic_ph $seg_ph $wid_ph"
        echo $cmd
        $cmd
}

# input widpath
# train and get result
linear_model_predict() {
    train_wid_path=$1
    test_wid_path=$2
    train_linear_file=${train_wid_path}_linear
    model_path=${train_linear_file}.model

    test_linear_file=${test_wid_path}_linear
    predict_ph=${test_linear_file}_predict
    upload_ph=${predict_ph}_upload

    # trans format
    echo transing format
    $PYPY trans_linear_model_format.py word $LABELED_DATA_LABEL_PH $train_wid_path $train_linear_file
    $PYPY trans_linear_model_format.py test $test_wid_path
    # train
    echo training
    $liblinear_train -s 3 -c 4 -e 0.001 -v 5 $train_linear_file $model_path
    # predict
    echo predicting
    $liblinear_predict $test_linear_file $model_path $predict_ph
    # to upload format
    echo gen predict upload
    $PYPY gen_predict_res_format.py  $TEST_DATA_PH $predict_ph $upload_ph
    # zip it
    echo zip the result
    zip -r ${upload_ph}.zip $upload_ph 
}


one_gram_main() {
    dic_path=$TOTAL_DIC_PATH
    for seg_path in ${LABELED_DATA_PH}_titles_seg ${TEST_DATA_PH}_titles_seg; do
        replace_word_with_wid $seg_path $dic_path
    done

    linear_model_predict ${LABELED_DATA_PH}_titles_seg_wid ${TEST_DATA_PH}_titles_seg_wid
}
one_gram_main
