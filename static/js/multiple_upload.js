var image_list = null;
var image_list_class = '.image-list';

$(document).ready(function() {
    image_list = new ImagesPreviewController(image_list_class);
});

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
                
            } else {

                size_sum = 0;

                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    size_sum += file.size;
                    var reader = new FileReader();
                    reader.onload = function(e) {
                        // console.log(e.target.result);
                        self.controller.AddFile(e.target.result);
                    };
                    reader.readAsDataURL(file);
                }

                console.log(size_sum);

                if(size_sum/1024/1024>4){
                    alert("El peso total de los archivos no debe superar 4MB");
                    $(this).val('');
                }
            }

            self.controller.ClearFileList();
        });

    $(document).on("click", ".remove", function() {
        var index = $(this).attr("index");
        self.controller.removeImage(index);
    });
};

ImagesPreviewView.prototype.render = function() {
    var images = this.controller.getImages();
    $(this.image_list_class).html("");
    for (i = 0; i < images.length; i++) {
        var img = images[i];
        var template = $(".template-image").html()
            .replace(";;src;;", img)
            .replace(";;index;;", i);

        $(this.image_list_class).append(template);
    }
};

ImagesPreviewController.prototype.AddFile = function(img) {
    this.model.push(img);
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
