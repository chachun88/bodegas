$(document).ready(function(){
    $("#aplicar").click(function(){

        var action = $("#default-select").val();
        var chkArray = [];
        var valores_checkbox = "";

        /* look for all checkboes that have a class 'chk' attached to it and check if it was checked */
        $(".iCheck:checked").each(function() {
            chkArray.push($(this).val());
        });

        valores_checkbox = chkArray.join(",")

        $.ajax({
            url: "/customer/actions",
            data: "values=" + valores_checkbox + "&action=" + action,
            type: "post",
            success: function(html){
                if(html=="ok"){
                    location.reload();
                } else {
                    alert(html);
                }
            }
        });
    });

    $('#clientes').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": {
            url: "/customer/list_ajax",
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
                    return '<input type="checkbox" name="clientes" class="iCheck" value="' + row.id + '">';
                }
            },
            { "targets": 1, "data": "status", "orderable": true },
            { "targets": 2, "data": "name", "orderable": true },
            { "targets": 3, "data": "email", "orderable": true },
            { "targets": 4, "data": "rut", "orderable": true },
            { "targets": 5, "data": "type", "orderable": true },
            { 
                "targets": 6,
                "data": "bussiness",
                "orderable": true
            },
            { "targets": 7, "data": "registration_date", "orderable": true },
            { "targets": 8, "data": "last_view", "orderable": true },
            { 
                "targets": 9,
                "data": null, 
                "orderable": false,
                render: function ( data, type, row ) {
                    return '<a class="btn btn-sm btn-success" href="/customer/view_contact?user_id=' + row.id + '">Ver Contactos</a>';
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
});
