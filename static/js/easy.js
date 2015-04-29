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

    $(".form-easy").submit(function(event) {
        // agregar productos a bodega
        var cellar_id = $("select[name=cellar_id]", $(this)).val();
        var product_sku = $("select[name=sku]", $(this)).val();
        var quantity = $("input[name=quantity]", $(this)).val();
        var price = $("input[name=price]", $(this)).val();
        var size = $("select[name=size]", $(this)).val();
        var operation = $("input[name=operation]", $(this)).val();

        var post_data = {
            "cellar_id": cellar_id,
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
                    alert("ok");
                }

            }
        });

        return false;
    });
});