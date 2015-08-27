// function isJSON(value)
// {
//     var is_json = false;
//         // detect if an string can be converted to json
//     try
//     {
//         var val = $.parseJSON(value);
//         is_json = true;
//     }
//     catch(ex)
//     {
//         // nothing here
//         is_json = false;
//     }

//     return is_json;
// }


$(document).ready(function(){
    

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

    $(document).on('click', 'button:submit', function(evt)
    {
        // evt.preventDefault();

        var ready = true;
        
        if (!ready)
        {
            alert("Por favor espere que las fotos terminen de subirse");
        }

        return ready;

        // console.log("eeee");
    });

    $(document).on('click', 'button#preview-home', function(){
        location.href = 'http://giani.ondev.today/preview/home?' + $("form").serialize();
    });
});