$(document).on('pjax:end ready',function(){

    if ( !$.fn.dataTable.isDataTable( '#cellar_detail' ) ) {
        var products_table = $('#cellar_detail').DataTable({
            "order": [[ 0, "asc" ]],
            "serverSide": true,
            "processing": true,
            "ajax": {
                url: "/cellar/detail?id=" + $("#cellar_id").val(),
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
                    "data": "sku", 
                    "orderable": true
                },
                { 
                    "targets": 1,
                    "data": "name", 
                    "orderable": true
                },
                { "targets": 2,"data": "size", "orderable": true },
                { "targets": 3,"data": "color", "orderable": true },
                { "targets": 4,"data": "balance_units", "orderable": true },
                { "targets": 5,"data": "balance_total", "orderable": true }
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
});