$(document).ready(function() {

    $("#salida select#sku").change(function() {

        var json_string = $("#salida input#product_list").val()
        obj = $.parseJSON(json_string);

        for (i = 0; i < obj.length; i++) {

            if (obj[i]["sku"] == $(this).val()) {

                $("#salida select#size").empty();

                var sizes = obj[i]["size"].split(",");

                $("#salida select#size").append($('<option>', {
                        value: '',
                        text: 'Seleccione'
                }));

                for (j = 0; j < sizes.length; j++) {
                    $("#salida select#size").append($('<option>', {
                        value: sizes[j],
                        text: sizes[j]
                    }));
                }
            }
        }
    });

    $("#entrada select#sku").change(function() {

        var json_string = $("#entrada input#product_list").val()
        obj = $.parseJSON(json_string);

        for (i = 0; i < obj.length; i++) {

            if (obj[i]["sku"] == $(this).val()) {

                $("#entrada select#size").empty();

                var sizes = obj[i]["size"].split(",");

                $("#entrada select#size").append($('<option>', {
                        value: '',
                        text: 'Seleccione'
                }));

                for (j = 0; j < sizes.length; j++) {
                    $("#entrada select#size").append($('<option>', {
                        value: sizes[j],
                        text: sizes[j]
                    }));
                }
            }
        }
    });

    $("#movimiento select#sku").change(function() {

        var json_string = $("#movimiento input#product_list").val()
        obj = $.parseJSON(json_string);

        for (i = 0; i < obj.length; i++) {

            if (obj[i]["sku"] == $(this).val()) {

                $("#movimiento select#size").empty();

                var sizes = obj[i]["size"].split(",");

                $("#movimiento select#size").append($('<option>', {
                        value: '',
                        text: 'Seleccione'
                }));

                for (j = 0; j < sizes.length; j++) {
                    $("#movimiento select#size").append($('<option>', {
                        value: sizes[j],
                        text: sizes[j]
                    }));
                }
            }
        }
    });

    $(".form-easy").submit(function(event) {
        // agregar productos a bodega
        var cellar_id = $("select[name=cellar_id]", $(this)).val();
        var new_cellar = $("select[name=new_cellar]", $(this)).val();
        var product_sku = $("select[name=sku]", $(this)).val();
        var quantity = $("input[name=quantity]", $(this)).val();
        var price = $("input[name=price]", $(this)).val();
        var size = $("select[name=size]", $(this)).val();
        var operation = $("input[name=operation]", $(this)).val();

        if (product_sku == ''){
            alert("Por favor seleccione un producto");
            return false;
        }

        if (quantity == ''){
            alert("Por favor ingrese cantidad");
            return false;
        }

        if (price == ''){
            alert("Por favor ingrese el precio");
            return false;
        }

        if (size == ''){
            alert("Por favor seleccione una talla");
            return false;
        }

        if (cellar_id == new_cellar){
            alert("Debe elegir una bodega distinta a la de origen");
            return false;
        }

        var post_data = {
            "cellar_id": cellar_id,
            "new_cellar": new_cellar,
            "sku": product_sku,
            "quantity": quantity,
            "price": price,
            "size": size,
            "operation": operation
        };

        //console.log(post_data)

        $.ajax({
            url: $(".form-easy").attr("action"),
            type: "post",
            data: post_data,
            dataType: "json",
            success: function(html) {

                var response_str = JSON.stringify(html);
                var response = $.parseJSON(response_str);

                console.info(response);

                if (response.state == "error") {
                    alert(response.message);
                    return false;
                } else {
                    alert(response.message);
                }

            }
        });

        return false;
    });

    $("a.a_tab").click(function(){
        var identifier = $(this).attr("href");
        $(identifier).removeClass("hidden").siblings().addClass("hidden");
    });
});