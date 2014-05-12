 	$(document).ready(function(){
	$(".lp-autocomplete").lpAutoComplete({
		auto:true,
		onSelect:function(result){
			$("#product_id").val(result.key);

		}
	});

	$(".load-products").click(function(event){
		$("#load").addClass("fa");	
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
		var size = $("input[name=size]", $(this)).val();
		var color = $("input[name=color]", $(this)).val();
		var cellar_name = $("input[name=cellar_name]", $(this)).val();
		var product_name = $("input[name=product_name]", $(this)).val();
		var new_cellar = $("select[name=new_cellar]", $(this)).val();
		var balance_price = $("input[name=balance_price]", $(this)).val();
		var transaction = $("input[name=transaction]", $(this)).val();

		console.log("entra " + product_id);

		if (transaction== undefined){
			transaction="agregado";
		}

		if (new_cellar==undefined){
			new_cellar="delete"
		}

		var post_data = {
			"cellar_id":cellar_id,
			"product_id":product_id,
			"quantity":quantity,
			"price":price,
			"size":size,
			"color":color,
			"new_cellar":new_cellar,
			"balance_price":balance_price
		};

		$(".lptooltip").hide(animation_duration);

		$.ajax({
			url: $(".form-add").attr("action"),
			type: "post",
			data: post_data,
			success: function(response)
			{
				$(".mmessage").html("Se han "+ transaction +" "+ quantity +" '" + product_name + "' a la bodega '" + cellar_name + "'" );
				$(".alert-success").show(animation_duration);

				setTimeout(function() {
					$(".alert-success").hide(animation_duration);
				}, 3000);
			}
		});

		return false;
	});
});