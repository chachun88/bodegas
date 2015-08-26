$(document).ready(function(){
    $("input:file").fileuploader({
        "multi": false,
        "uploadurl" : 'https://static.loadingplay.com/image/upload'
    });
});