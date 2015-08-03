var image_list = null;
var image_list_class = '.image-list';

$(document).on('ready pjax:end', function() {
    image_list = new ImagesPreviewController(image_list_class);
});


var LPFile = function(name, img)
{
    this.name = name === undefined ? "" : name;
    this.img = img === undefined ? "" : img;
};


var ImagesPreviewController = function(image_list_class) {
    this.model = [];
    this.view = new ImagesPreviewView(this, image_list_class);
};

var ImagesPreviewView = function(controller, image_list_class) {
    this.controller = controller;
    this.initEvents();
    this.image_list_class = image_list_class;
};

ImagesPreviewView.prototype.initEvents = function() {
    var self = this;
    $("input[name=image]").change(
        function() {

            var files = $(this).get(0).files;

            if(files.length>6){
                alert("No puede subir mas de 6 fotos");
                $(this).val('');
                $(image_list_class).html('');
            } else {

                size_sum = 0;
                var extension_ok = true;
                var extensions = ['png','jpeg','jpg'];

                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    size_sum += file.size;

                    if(extensions.indexOf(file.name.split('.').pop().toLowerCase()) == -1){
                        // console.log("·");
                        extension_ok = false;
                    }
                }

                // console.log(size_sum);

                if(size_sum/1024/1024>4){
                    alert("El peso total de los archivos no debe superar 4MB");
                    $(this).val('');
                    $(image_list_class).html('');
                } else {
                    if(!extension_ok){
                        alert("Los formatos permitidos son png, jpeg, jpg");
                        $(this).val('');
                        $(image_list_class).html('');
                    } else {
                        self.loadImages( files );
                    }
                }
            }
        });

    $(document).on("click", ".remove", function() {
        var index = $(this).attr("index");
        self.controller.removeImage(index);
    });
};


ImagesPreviewView.prototype.loadImage = function(file) 
{
    var self = this;
    var reader = new FileReader();
    reader.onload = function(e) 
    {
        // console.log(e.target.result);
        self.controller.setImageData(file.name, e.target.result);
    };

    self.controller.AddFile(file.name);
    reader.readAsDataURL(file);
};


ImagesPreviewView.prototype.loadImages = function(image_list) 
{
    var self = this;
    var counter = 0;
    var length = image_list.length;
    self.controller.ClearFileList();

    for (var i = 0; i < image_list.length; i++) 
    {
        self.loadImage(image_list[i]);
    }
};

ImagesPreviewView.prototype.render = function() 
{
    // console.log("render");
    var images = this.controller.getImages();
    $(this.image_list_class).html("");
    for (i = 0; i < images.length; i++) {
        var img = images[i];
        var template = $(".template-image").html()
            .replace(";;src;;", img.img)
            .replace(";;index;;", i)
            .replace(";;image_name;;", img.name);

        $(this.image_list_class).append(template);
    }
};

ImagesPreviewController.prototype.AddFile = function(name) 
{
    var file = new LPFile(name);
    this.model.push(file);
};

ImagesPreviewController.prototype.setImageData = function(name, data) 
{
    for (var i = 0; i < this.model.length; i++) 
    {
        var image = this.model[i];
        if (image.name === name)
        {
            image.img = data;
        }
    }

    this.view.render();
};

ImagesPreviewController.prototype.ClearFileList = function() {
    this.model = [];
};

ImagesPreviewController.prototype.getImages = function() {
    return this.model;
};

ImagesPreviewController.prototype.removeImage = function(index) {
    this.model.splice(index, 1);
    this.view.render();
};
