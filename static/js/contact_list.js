$(document).on('pjax:end ready',function(){
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
            url: "/contact/actions",
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
});
