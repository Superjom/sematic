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
    $PYPY trans_linear_model_format.py test $test_wid_path $test_linear_file
    # train
    cmd="$liblinear_train -s 2 -c 4 -e 0.001 -v 5 $train_linear_file"
    echo $cmd; $cmd

    cmd="$liblinear_train -s 2 -c 4 -e 0.001 $train_linear_file $model_path"
    echo $cmd; $cmd
    # predict
    echo predicting
    $liblinear_predict $test_linear_file $model_path $predict_ph
    # to upload format
    echo gen predict upload
    cd ..
    $PYPY gen_predict_res_format.py  $TEST_DATA_PH $predict_ph $upload_ph
    cd linear_model 
    # zip it
    echo zip the result
    zip -r ${upload_ph}.zip $upload_ph 
}

# ================================ main ==============================

one_gram_word_main() {
    dic_path=$TOTAL_DIC_PATH
    for seg_path in ${LABELED_DATA_PH}_titles_seg ${TEST_DATA_PH}_titles_seg; do
        replace_word_with_wid $seg_path $dic_path
    done

    linear_model_predict ${LABELED_DATA_PH}_titles_seg_wid ${TEST_DATA_PH}_titles_seg_wid
}

two_gram_word_main() {
    dic_path=$TOTAL_DIC_PATH2
    # replace 2gram pairs with pid
    for seg_path in $LABELED_DATA_PH $TEST_DATA_PH; do
        cmd="replace_word_with_wid ${seg_path}_titles_2gram $dic_path"
        echo $cmd; $cmd
    done
    # train
    cmd="linear_model_predict ${LABELED_DATA_PH}_titles_2gram_wid ${TEST_DATA_PH}_titles_2gram_wid"
    echo $cmd; $cmd
}

one_gram_token_main() {
    dic_path=$TOTAL_TOKEN_DIC
    for seg_path in ${LABELED_DATA_PH}_titles_seg_tokens  ${TEST_DATA_PH}_titles_seg_tokens  ; do
        replace_word_with_wid $seg_path $dic_path
    done

    linear_model_predict ${LABELED_DATA_PH}_titles_seg_tokens_wid ${TEST_DATA_PH}_titles_seg_tokens_wid
}

two_gram_token_main() {
    dic_path=$TOTAL_TOKEN_2_DIC
    for seg_path in $LABELED_DATA_PH $TEST_DATA_PH; do
        cmd="$PYPY gen_2gram_titles.py ${seg_path}_titles_seg_tokens  ${seg_path}_titles_seg_tokens_2gram"
        echo $cmd; $cmd
        cmd="replace_word_with_wid ${seg_path}_titles_seg_tokens_2gram $dic_path"
        echo $cmd; $cmd
    done
    linear_model_predict ${LABELED_DATA_PH}_titles_seg_tokens_2gram_wid ${TEST_DATA_PH}_titles_seg_tokens_2gram_wid
}

# with:
# word: 1-gram 2-gram 
# token: 1-gram 2-gram
# edit distance: word, token
word_and_token_and_edit_dis() {
}


#one_gram_main
#two_gram_main
#one_gram_token_main
two_gram_token_main
