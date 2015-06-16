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
                var obj = $.parseJSON(html_str);
                var html_res = '';

                // console.log(obj);
                
                if(obj.length > 0){
                    for(var i = 0; i < obj.length; i++){
                        if("error" in obj[i]){
                            html_res += obj[i].error + '\n';
                        }
                    }
                    if(html_res != ''){
                        alert(html_res);
                    } else {
                        location.reload();
                    }
                } else {
                    location.reload();
                }
            }
        });
    } else{
        alert("Debe llenar todos los campos");
        return false;
    }
}


$(document).ready(function(){

    $('#pedidos').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": {
            url: "/order/list_ajax",
            data: function ( d ) {
                //d.start = d.start
            }
        },
        "lengthChange": false,
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
                "data": null, 
                "orderable": false,
                render: function ( data, type, row ) {
                    if ( row.state != 3 ) {
                        return '<input type="checkbox" name="pedidos" class="iCheck" value="' + row.order_id + '" tracking-code="-">';
                    } else {
                        console.log('<input type="checkbox" name="pedidos" class="iCheck" value="' + row.order_id + '" tracking-code="' + row.tracking_code + '">');
                        return '<input type=\"checkbox\" name=\"pedidos\" class=\"iCheck\" value=\"' + row.order_id + '" tracking-code="' + row.tracking_code + '">';
                    }
                    return data;
                }
            },
            { "targets": 1,"data": "order_id", "orderable": true },
            { "targets": 2,"data": "date", "orderable": true },
            { "targets": 3,"data": "customer", "orderable": true },
            { 
                "targets": 4,
                "data": "tipo_cliente",
                "orderable": true
            },
            { "targets": 5,"data": "source", "orderable": true },
            //{ "targets": 6,"data": "items_quantity", "orderable": true },
            { 
                "targets": 6,
                "data": "total", 
                "orderable": true,
                render: function(data, type, row){
                    return row.total.formatMoney(0);
                } 
            },
            { 
                "targets": 7,
                "data": "state",
                "orderable": true,
                render: function(data, type, row) {
                    if (row.state == 1) {
                        if (row.payment_type == 1) {
                            return '<span class="label label-warning">POR CONFIRMAR</span>';
                        } else {
                            return '<span class="label label-danger">RECHAZADO</span>';
                        }
                    } else if (row.state == 2) {
                        return '<span class="label label-success">CONFIRMADO</span>';
                    } else if (row.state == 3) {
                        return '<span class="label label-info">LISTO PARA DESPACHO</span>';
                    } else if (row.state == 4) {
                        return '<span class="label label-primary">DESPACHADO</span>';
                    } else if (row.state == 5) {
                        return '<span class="label label-danger">CANCELADO</span>';
                    }

                }
            },
            { 
                "targets": 8,
                "data": "payment_type",
                "orderable": true,
                "render" : function(data, type, row)
                {
                    if(row.payment_type == 1){
                        return 'TRANSFERENCIA';
                    } else {
                        return 'WEBPAY';
                    }
                } 
            },
            {
                "targets": 9,
                "data": "trx_id",
                "orderable": false
            },
            { 
                "targets": 10,
                "data": null, 
                "orderable": false,
                render: function ( data, type, row ) {
                    if ( type === 'display' ) {
                        return '<a class="btn btn-primary btn-sm detail-button" href="/order-detail/list?order_id=' + row.order_id + '">Ver Detalle</a>';
                    }
                    return data;
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

    $('span.state-filter').click(function(){
        var valor = $(this).html();
        if(valor=='TODOS'){
            $('input[type=search]').val('');
        } else {
            $('input[type=search]').val(valor);
        }
        $('input[type=search]').trigger('keyup');
    });

    $("#aplicar").click(function(){

        var action = $("#default-select").val();
        var chkArray = [];
        var valores_checkbox = "";

        /* look for all checkboes that have a class 'chk' attached to it and check if it was checked */
        

        if (parseInt(action) == 4) {

            $(".iCheck:checked").each(function() {
                var tracking_code = $(this).attr("tracking-code");
                if(tracking_code=='null')
                    chkArray.push($(this).val());
            });

            addUser(chkArray);

            if (chkArray.length > 0){
                $('#myModal').modal('show');
            } else{
                alert("Por favor seleccione pedidos listos para ser despachados");
            }

        } else {

            $(".iCheck:checked").each(function() {
                chkArray.push($(this).val());
            });

            valores_checkbox = chkArray.join(",");

            $.ajax({
                url: "/orders/actions",
                data: "values=" + valores_checkbox + "&action=" + action,
                type: "post",
                dataType: 'json',
                success: function(html) {

                    var html_str = JSON.stringify(html);
                    obj = $.parseJSON(html_str);

                    var html_res = '';

                    if(obj.length > 0){
                        for(var i = 0; i < obj.length; i++){
                            if("error" in obj[i]){
                                html_res += obj[i]["error"] + '\n';
                            }
                        }
                        if(html_res !== ''){
                            alert(html_res);
                        } else {
                            location.reload();
                        }
                    } else {
                        location.reload();
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

    $('#myModal, #iframe_detalle').on('shown.bs.modal', function() {
        //addUser();
    });

    $(document).on('click', "a.detail-button", function(e){
        e.preventDefault();
        $("#iframe_detalle iframe").attr('src', $(this).attr('href'));
        $("#iframe_detalle").modal('show');
    });

    //$('#myModal').modal('show');
});
