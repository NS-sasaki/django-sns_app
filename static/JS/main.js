// dropzone IDを持つ要素に適用
Dropzone.autoDiscover = false;
//ファイル数、ファイル形式、ファイルサイズを制限
const myDropzone = new Dropzone("#my-dropzone", {
    maxFiles: 1,
    maxFilesize: 2,
    acceptedFiles: '.jpg, .png', 
})

// popupクラスの要素にMagnific Popupを適用
$('.popup').magnificPopup({
    type: 'image',
});