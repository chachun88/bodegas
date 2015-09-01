var formFastEdit = function(sku){
    var json = $("#"+sku).val();
    var json_obj = $.parseJSON(json);

    var category = json_obj.category; // nombre de la categoria
    var category_id = json_obj.category_id;
    var brand = json_obj.brand;
    var bulk_price = json_obj.bulk_price;
    var bullet_1 = json_obj.bullet_1;
    var bullet_2 = json_obj.bullet_2;
    var bullet_3 = json_obj.bullet_3;
    var color = json_obj.color;
    var currency = json_obj.currency;
    var deleted = json_obj.deleted;
    var delivery = json_obj.delivery;
    var description = json_obj.description;
    var for_sale = json_obj.for_sale;
    var id = json_obj.id;
    var image = json_obj.image;
    var image_2 = json_obj.image_2;
    var image_3 = json_obj.image_3;
    var image_4 = json_obj.image_4;
    var image_5 = json_obj.image_5;
    var image_6 = json_obj.image_6;
    var images = json_obj.images;
    var manufacturer = json_obj.manufacturer;
    var material = json_obj.material;
    var name = json_obj.name;
    var price = json_obj.price;
    var promotion_price = json_obj.promotion_price;
    var sell_price = json_obj.sell_price;
    var size = json_obj.size; // tipo string
    var upc = json_obj.upc;
    var which_size = json_obj.which_size;
    var position = json_obj.position;

    var form = $("#fastedit");

    $("input[name='id']", form).val(id);
    $("input[name='category']", form).val(category);
    $("input[name='name']", form).val(name);
    $('#fastedit-textarea').data("wysihtml5").editor.setValue(description);
    // $("textarea[name='description']", form).text(description);
    $("input[name='color']", form).val(color);
    $("input[name='sell_price']", form).val(sell_price);
    $("input[name='price']", form).val(price);
    $("input[name='sku']", form).val(sku);
    //$("input[name='brand']", form).val(brand);
    $("input[name='promotion_price']", form).val(promotion_price);
    $("input[name='bulk_price']", form).val(bulk_price);
    $("input[name='position']", form).val(position);
    $('#myModal').modal('show');
};

var FastEdit = function(form_id){
    var sku = $("input[name=sku]", $(form_id)).val();
    var data = $(form_id).serialize();
    var url = $(form_id).attr("action");
    var method = $(form_id).attr("method");

    var json = $("#"+sku).val();
    var json_obj = $.parseJSON(json);
    json_obj.category = $(form_id+" input[name='category']").val();
    json_obj.name = $(form_id+" input[name='name']").val();
    json_obj.description = $(form_id+" textarea[name='description']").text();
    json_obj.color = $(form_id+" input[name='color']").val();
    json_obj.sell_price = $(form_id+" input[name='sell_price']").val();
    json_obj.price = $(form_id+" input[name='price']").val();
    json_obj.promotion_price = $(form_id+" input[name='promotion_price']").val();
    json_obj.bulk_price = $(form_id+" input[name='bulk_price']").val();
    json_obj.position = $(form_id+" input[name='position']").val();
    $("#"+sku).val(JSON.stringify(json_obj));
    
    $.ajax({
        url:url,
        data:data,
        type:method,
        success: function(obj){
            if(obj.success){
                /*var search = $("input[type=search]").val();*/
                //$('input#hidden_search').trigger("keyup");
                if($("#productos").length){
                    $("#productos").DataTable().ajax.reload(null, false);
                }
                $('#myModal').modal('hide');
            } else {
                alert(obj.error);
            }
        }
    });
};

$(document).on('pjax:end ready',function(){

    $('#fastedit-textarea').wysihtml5({
        "font-styles": false, //Font styling, e.g. h1, h2, etc. Default true
        "emphasis": true, //Italics, bold, etc. Default true
        "lists": true, //(Un)ordered lists, e.g. Bullets, Numbers. Default true
        "html": false, //Button which allows you to edit the generated HTML. Default false
        "link": false, //Button to insert a link. Default true
        "image": false, //Button to insert an image. Default true,
        "color": false, //Button to change color of font  
        "locale": "es"
    });

    if ( !$.fn.dataTable.isDataTable( '#productos' ) ) {
        var products_table = $('#productos').DataTable({
            "order": [[ 3, "asc" ]],
            "serverSide": true,
            "processing": true,
            "ajax": {
                url: "/product/list",
                type: "post",
                data: function ( d ) {
                    //d.start = d.start
                }
            },
            "lengthChange": true,
            "pageLength": 20,
            "dom": 'T<"clear">lfrtip',
            "tableTools": {
                "sSwfPath": "../static/swf/copy_csv_xls_pdf.swf",
                "aButtons": [
                    {
                        "sExtends": "copy",
                        "sButtonText": "Copiar",
                        fnComplete: function(nButton, oConfig, flash, text) {
                            var lines = text.split('\n').length;
                            if (oConfig.bHeader) lines--;
                            if (this.s.dt.nTFoot !== null && oConfig.bFooter) lines--;
                            var plural = (lines==1) ? "" : "s";
                            this.fnInfo( '<h6>Tabla copiada</h6>'+
                                '<p>'+lines+' fila'+plural+' copiada' + plural +' al portapapeles.</p>',
                                1500
                            );
                        }
                    },
                    "xls",
                    {
                        "sExtends": "pdf",
                        "sButtonText": "PDF"
                    },
                    {
                        "sExtends": "print",
                        "sButtonText": "Imprimir",
                        fnClick: function() {
                            window.print();
                        }
                    }
                ]
            },
            "columnDefs": [
                {   "targets": 0,
                    "data": "for_sale", 
                    "orderable": true,
                    render: function ( data, type, row ) {
                        if(row.for_sale == 1){
                            return '<a class=\"for_sale\" onclick=\"for_sale(\'' +
                                   row.id + 
                                   '\')"><i class="fa fa-eye" id="' +
                                   row.id +
                                   '"></i></a>';
                        } else {
                            return '<a class=\"for_sale\" onclick=\"for_sale(\'' +
                                   row.id + 
                                   '\')"><i class="fa fa-eye disabled" id="' +
                                   row.id + '"></i></a>';
                        }
                    }
                },
                { 
                    "targets": 1,
                    "data": "image", 
                    "orderable": false,
                    render: function(data, type, row){
                        // console.log(row.image);
                        return '<img src=\"/image/' + row.image + '?mw=60\" width=\"60\">';
                    }
                },
                { "targets": 2,"data": "sku", "orderable": true },
                { "targets": 3,"data": "name", "orderable": true },
                { "targets": 4,"data": "size", "orderable": false },
                { 
                    "targets": 5,
                    "data": "price",
                    "orderable": true,
                    render: function(data, type, row){
                        return row.price.formatMoney(0);
                    }
                },
                { 
                    "targets": 6,
                    "data": "sell_price", 
                    "orderable": true,
                    render: function(data, type, row){
                        return row.sell_price.formatMoney(0);
                    }
                },
                { 
                    "targets": 7,
                    "data": "promotion_price", 
                    "orderable": true,
                    render: function(data, type, row){
                        return row.promotion_price.formatMoney(0);
                    }
                },
                { 
                    "targets": 8,
                    "data": "bulk_price", 
                    "orderable": true,
                    render: function(data, type, row){
                        return row.bulk_price.formatMoney(0);
                    }
                },
                { 
                    "targets": 9,
                    "data": "position", 
                    "orderable": true,
                    render: function(data, type, row){

                        var total = products_table.page.info().recordsTotal;


                        var botones = '<select class="position" id="';
                        botones += row.id;
                        botones += '">';
                        
                        for(var i=1; i<=total; i++){
                            botones += '<option value="';
                            botones += i;
                            if(i===row.position){
                                botones += '" selected>';
                            } else {
                                botones += '">';
                            }
                            botones += i;
                            botones += '</option>';
                        }
                        botones += '</select>';
                        return botones;
                    }
                },
                { 
                    "targets": 10,
                    "data": null, 
                    "orderable": false,
                    render: function(data, type, row){
                        var botones = '<a class="btn btn-sm btn-primary" href="/product/edit?id=' + row.id + '">Editar</a>'+
                                    '<br/>' +
                                    '<a class="btn btn-sm btn-danger" href="/product/remove?id='+ row.id +
                                    '" onclick="return confirm("¿Está seguro que desea eliminar el producto?");">'+
                                    'Eliminar' +
                                    '</a>' +
                                    '<br/>' +
                                    "<input type='hidden' id='" + row.sku + "' value='" + JSON.stringify(row) + "'>" +
                                    "<a class=\"btn btn-warning btn-sm\" onclick=\"formFastEdit('" + row.sku + "')\">Edici&oacute;n R&aacute;pida</a>";
                        return botones;
                    }
                }
            ],
            "language":{
                "zeroRecords": "No hay resultados para esta busqueda",
                "search": "Busqueda:",
                "paginate": {
                    "first":      "Primera",
                    "last":       "Ultima",
                    "next":       "Siguiente",
                    "previous":   "Anterior"
                },
                "info":           "Mostrando _START_ a _END_ de _TOTAL_ entradas",
                "infoEmpty":      "Mostrando 0 a 0 de 0 entradas",
                "processing":     "Cargando..."
            }
        });
    }

    $('input[type=search]').on( 'keyup', function () {
        $('input#hidden_search').val( this.value );
    });
    $('input#hidden_search').on( 'keyup', function () {
        products_table.search( this.value ).draw();
    });
    $(document).on('change', "select.position", function(){
        var product_id = $(this).attr("id");
        var position = $(this).val();
        $.ajax({
            url: "/product/change_position",
            type: "post",
            data: "product_id=" + product_id + "&position=" + position,
            success: function(response){
                if(response==='ok'){
                    if($("#productos".length)){
                        $("#productos").DataTable().ajax.reload(null, false);
                    }
                } else {
                    alert(response);
                }
            }
        });
    });
});