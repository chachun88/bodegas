$(document).ready(function(){
	$(".lp-autocomplete").lpAutoComplete({
		auto:true,
		onSelect:function(result){
			$("#product_id").val(result.key)
		}
	});

	$(".cellar").click(function(){
		var idcellar = $(this).attr("cellar-id");
		
			$.ajax({
            url: "/cellar/detail?cellar_id=" + idcellar,
            type: "get",
            success: function(response){
                alert(idcellar);
            }
        });

	});
})