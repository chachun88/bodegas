$(document).ready(function(){
    

    $("input.upload:file").each(function(){
        var src = $(this).attr("src");
        var name = $(this).attr("name");
        var value = $(this).attr("valor");

        console.log(typeof(value));

        if(src === ""){
            $(this).fileuploader({
                "multi": false,
                "uploadurl" : 'https://static.loadingplay.com/image/upload'
            });
        } else {
            $(this).fileuploader({
                "multi": false,
                "uploadurl" : 'https://static.loadingplay.com/image/upload',
                "images": [{
                    "name" : src,
                    "src" : '',
                    "value" : value
                }]
            });
        }
    });

    $(document).on('click', 'button:submit', function(evt)
    {
        // evt.preventDefault();

        var ready = false;
        
        if (!ready)
        {
            alert("Por favor espere que las fotos terminen de subirse");
        }

        return ready;

        // console.log("eeee");
    });
});