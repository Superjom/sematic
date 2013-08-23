# =========== tools ====================
wordseg() {
    path=$1
    encode=$2
    tag=$3
    cd tools/word_seg
    if [ $tag -eq 0 ]; then
        tpath=${path}_seg_tag
        ./wordseg_tag $path $tpath $encode
    else
        tpath=${path}_seg
        ./wordseg $path $tpath $encode
    fi
    cd ../../
}

convert_encoding() {
    fpath=$1
    tpath=$2
    fe=$3
    te=$4
    cd tools
    # convert
    python convert_encoding.py $fpath $tpath $fe $te
    cd ..
}

