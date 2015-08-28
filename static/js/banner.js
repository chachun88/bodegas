var ready = function(){

    var ready = true;
    var input = [];

    $("input:text").each(function(){
        if(!$(this).fileuploader('isready')){
            ready = false;
        }
    });

    if (!ready)
    {
        alert("Por favor espere que las fotos terminen de subirse");
    }

    return ready;
};

$(document).on('ready pjax:end', function(){
    

    $("input.upload:file").each(function(){
        var src = $(this).attr("src");
        var name = $(this).attr("name");
        var value = $(this).attr("valor");

        if(src === ""){
            $(this).fileuploader({
                "multi": false,
                "uploadurl" : 'https://static.loadingplay.com/image/upload'
            });
        } else {

            // var is_json = isJSON(value);  // detect if remote

            // if (is_json)  // load from remote 
            // {
            $(this).fileuploader({
                "multi": false,
                "uploadurl" : 'https://static.loadingplay.com/image/upload',
                "images": [{
                    "name" : 'name.png',
                    "src" : src,
                    "value" : value
                }],
                "thumbnail": "thumb_200",
                "thumbnail_origin": "remote"
            });
            // }
            // else  // load thumbnail from local
            // {
            //     $(this).fileuploader({
            //         "multi": false,
            //         "uploadurl" : 'https://static.loadingplay.com/image/upload',
            //         "images": [{
            //             "name" : 'name.png',
            //             "src" : src,
            //             "value" : value
            //         }]
            //     });
            // }
        }
    });

    $(document).on('click', 'button#preview-home, button#preview-background', function(){
        var action = $(this).attr("url-local") + '/preview/home';
        $("form").attr('action', action);
        if(ready()){
            $("form").submit();
        }
    });
    $(document).on('click', 'button#preview-section', function(){
        var action = $(this).attr("url-local") + '/preview/section?tag=' + $(this).attr("tag");
        $("form").attr('action', action);
        if(ready()){
            $("form").submit();
        }
    });
    $(document).on('click', 'button:submit', function(){
        $("form").attr('action', '/banner');
        $("form").removeAttr("target");
        if(ready()){
            $("form").submit();
        }
    });
});