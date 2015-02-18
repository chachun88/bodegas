var ValidateTracking = function(){

    var empty = false;

    $('#myModal input').each(function(){
        if($(this).val().trim()=='')
            empty = true;
    });

    if(!empty){
        /*$("#shipping-tracking").submit();*/
        $.ajax({
            url: $("#shipping-tracking").attr("action"),
            data: $("#shipping-tracking").serialize(),
            dataType: 'json',
            type: $("#shipping-tracking").attr('method'),
            success: function(res){
                var html_str = JSON.stringify(res);
                obj = $.parseJSON(html_str);
                if (obj["state"]==0) {
                    location.reload()
                } else {
                    alert(obj["obj"]);
                }
            }
        });
    } else{
        alert("Debe llenar todos los campos");
        return false;
    }
}

$(document).ready(function(){
    $("#aplicar").click(function(){

        var action = $("#default-select").val();
        var chkArray = [];
        var valores_checkbox = "";

        /* look for all checkboes that have a class 'chk' attached to it and check if it was checked */
        

        if (parseInt(action) == 4) {

            $(".iCheck:checked").each(function() {
                var tracking_code = $(this).attr("tracking-code");
                if(tracking_code=='None')
                    chkArray.push($(this).val());
            });

            addUser(chkArray);

            $('#myModal').modal('show');

        } else {

            $(".iCheck:checked").each(function() {
                chkArray.push($(this).val());
            });

            valores_checkbox = chkArray.join(",")

            $.ajax({
                url: "/orders/actions",
                data: "values=" + valores_checkbox + "&action=" + action,
                type: "post",
                dataType: 'json',
                success: function(html) {
                    var html_str = JSON.stringify(html);
                    obj = $.parseJSON(html_str);
                    if (obj["success"]) {
                        location.reload();
                    } else {
                        alert(obj.error);
                    }
                }
            });
        }
    });

    var addUser = function(arr){


        

        var f = document.getElementById("shipping-tracking");

        f.innerHTML = '';

        for (var cont = 0; cont < arr.length; cont++) {

            var form_group = document.createElement("div");
            form_group.setAttribute("class","form-group");

            f.appendChild(form_group);

            var col_md_12 = document.createElement("div");
            col_md_12.setAttribute("class","col-md-12");

            var col_md_1 = document.createElement("div");
            col_md_1.setAttribute("class","col-md-1");

            var label = document.createElement("label"); //input element, text
            label.setAttribute('class', "control-label");
            label.innerHTML = "Pedido nro: " + arr[cont];

            form_group.appendChild(label);
            
            var input = document.createElement("input"); //input element, text
            input.setAttribute('type', "text");
            input.setAttribute("class","col-md-6");
            input.setAttribute('name', 'tracking_code');

            var input_hidden = document.createElement("input"); //input_hidden element, text
            input_hidden.setAttribute('type', "hidden");
            input_hidden.setAttribute('name', 'order_id');
            input_hidden.value = arr[cont];


            col_md_12.appendChild(input);
            col_md_12.appendChild(col_md_1);

            var array = [1,2];
            var array_text = ["Chilexpress","Correos de Chile"]

            //Create and append select list
            var selectList = document.createElement("select");
            selectList.setAttribute('name', 'provider_id');
            selectList.setAttribute("class","col-md-5");

            //Create and append the options
            for (var i = 0; i < array.length; i++) {
                var option = document.createElement("option");
                option.value = array[i];
                option.text = array_text[i];
                selectList.appendChild(option);
            }

            col_md_12.appendChild(selectList);
            form_group.appendChild(input_hidden);
            form_group.appendChild(col_md_12);
        };
        
        //f.appendChild(s);

    }

    /*dialog = $( "#dialog-form" ).dialog({
      autoOpen: true,
      height: 300,
      width: 350,
      modal: true,
      buttons: {
        "Create an account": addUser,
        Cancel: function() {
          dialog.dialog( "close" );
        }
      },
      close: function() {
        form[ 0 ].reset();
        allFields.removeClass( "ui-state-error" );
      }
    });*/

    $('#myModal').on('shown.bs.modal', function() {
        //addUser();
    });

    //$('#myModal').modal('show');
});
