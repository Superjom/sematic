PROJECT_PATH=/home/chunwei/sematic
DATA_PATH=$PROJECT_PATH/data


# split word for titles and gen a dic
split_word() {
    python database.py gen_target_title_file
    python database.py gen_source_title_file
    # split word
    for path in "$DATA_PATH/source_titles.txt" "$DATA_PATH/target_titles.txt"; do
        python split_word.py $path ${path}_split
    done
    # gen dic
    python database.py gen_word_dic
}

# replace title's words with their word indexs
gen_wordid_titles() {
    python database.py gen_word_id_titles
}

split_word
