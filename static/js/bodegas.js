$(document).ready(function(){
	$(".lp-autocomplete").lpAutoComplete({
		auto:true,
		onSelect:function(result){
			$("#product_id").val(result.key)
		}
	});

	$(".cellar").click(function()
	{
		var idcellar = $(this).attr("cellar-id");
		
		$.ajax({
			url: "/cellar/detail?cellar_id=" + idcellar,
			type: "get",
			success: function(response)
			{
				alert(idcellar);
			}
		});

	});


	//// formulario para agregar productos

	var mouse_over = false;
	var animation_duration = 300;

	$("html").click(function()
	{
		if (!mouse_over) 
		{
			$(".lptooltip").hide(animation_duration);
		}
	});

	$(".lptooltip").mouseover(function()
	{
		mouse_over = true;
	});

	$(".lptooltip").mouseout(function()
	{
		mouse_over = false;
	});

	$(".btn-add").click(function(event)
	{
		var tooltip = $(".lptooltip", $(this).parent());

		$(".lptooltip").hide(animation_duration); // hide others opened tooltips
		tooltip.show(animation_duration);
		$("input[name=quantity]", tooltip).focus();

		return false;
	});

	$(".close").click(function()
	{
		$(".alert-success").hide(animation_duration);
		return false;
	});

	$(".form-add").submit(function(event)
	{
		// agregar productos a bodega
		var cellar_id = $("input[name=cellar_id]", $(this)).val();
		var product_id = $("input[name=product_id]", $(this)).val();
		var quantity = $("input[name=quantity]", $(this)).val();
		var price = $("input[name=price]", $(this)).val();
		var cellar_name = $("input[name=cellar_name]", $(this)).val();
		var product_name = $("input[name=product_name]", $(this)).val();

		var post_data = {
			"cellar_id":cellar_id,
			"product_id":product_id,
			"quantity":quantity,
			"price":price
		};

		$(".lptooltip").hide(animation_duration);

		$.ajax({
			url: $(".form-add").attr("action"),
			type: "post",
			data: post_data,
			success: function(response)
			{
				$(".mmessage").html("Se han agregado "+ quantity +" '" + product_name + "' a la bodega '" + cellar_name + "'" );
				$(".alert-success").show(animation_duration);

				setTimeout(function() {
					$(".alert-success").hide(animation_duration);
				}, 3000);
			}
		});

		return false;
	});
})