 	$(document).ready(function(){
	
	$(".lp-autocomplete").lpAutoComplete({
		auto:true,
		onSelect:function(result){
			$("#product_id").val(result.key);
			var cellar_id = $("input[name=name]").attr("cellar_id");

			$.ajax({
			url:"/cellar/combobox" ,
			type: "post",
			data: {product_id: result.key, cellar_id:cellar_id},
			success: function(response)
			{
				$(".combobox").html(response);
			}
		});
		}
	});

	$(".load-products").click(function(event){
		$("#load").addClass("fa");	
	});

/*	//// Llenar combobox de output.html
	$(".name").change(function(){
		alert("entra");		
	});*/


	//// formulario para agregar productos

	var mouse_over = false;
	var animation_duration = 300;

	setTimeout( function(){
		console.log("close alert");
		$(".alert").hide(animation_duration);
	}, 5000 )

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
		var product_sku = $("input[name=product_sku]", $(this)).val();
		var quantity = $("input[name=quantity]", $(this)).val();
		var price = $("input[name=price]", $(this)).val();
		var size = $("input[name=size]", $(this)).val();
		var color = $("input[name=color]", $(this)).val();
		var cellar_name = $("input[name=cellar_name]", $(this)).val();
		var product_name = $("input[name=product_name]", $(this)).val();
		var new_cellar = $("select[name=new_cellar]", $(this)).val();
		var balance_price = $("input[name=balance_price]", $(this)).val();
		var transaction = $("input[name=transaction]", $(this)).val();
		var operation =$("input[name=operation]", $(this)).val();

		if (size == undefined){
			size = $("select[name=size]", $(this)).val();
		}

		if (color == undefined){
			color = $("select[name=color]", $(this)).val();
		}

		if (transaction== undefined){
			transaction="agregado";
		}

		if (new_cellar==undefined){
			new_cellar="delete"
		}

		if (price==undefined){
			price="0"
		}

		var post_data = {
			"cellar_id":cellar_id,
			"product_id":product_id,
			"product_sku":product_sku,
			"quantity":quantity,
			"price":price,
			"size":size,
			"color":color,
			"new_cellar":new_cellar,
			"balance_price":balance_price,
			"operation": operation
		};


		$(".lptooltip").hide(animation_duration);

		$.ajax({
			url: $(".form-add").attr("action"),
			type: "post",
			data: post_data,
			success: function(response)
			{

				if(response=="okok" || response=="ok"){
					$(".tit").html("Bien hecho!")
					$(".mmessage").html("Se han "+ transaction +" "+ quantity +" '" + product_name + "' a la bodega '" + cellar_name + "'" );
					$(".alert-success").show(animation_duration);

					setTimeout(function() {
						$(".alert-success").hide(animation_duration);
					}, 3000);
				}else{

					$(".tit").html("Problemas!")
					$(".mmessage").html("Cantidad supera a existencia en bodega");	
					$("#alert-message").removeClass("alert-success");
					$("#alert-message").addClass("alert-warning");
					$(".alert-warning").show(animation_duration);

					setTimeout(function() {
						$(".alert-warning").hide(animation_duration);
					}, 3000);
				}
				
			}
		});

		return false;
	});

	$(".form-period").submit(function(event)
	{
		var from = $("input[name=from]", $(this)).val();
		var until = $("input[name=until]", $(this)).val();
		var day = $("input[name=day]", $(this)).val();

		var post_data = {
			"from":from,
			"until":until,
			"day":day
		};

		$(".lptooltip").hide(animation_duration);		

		$.ajax({
			url: $(".form-period").attr("action"),
			type: "post",
			data: post_data,
			success: function(response)
			{
				/*$(".mmessage").html("Se han "+ transaction +" "+ quantity +" '" + product_name + "' a la bodega '" + cellar_name + "'" );*/
				$(".alert-success").show(animation_duration);
				$("#period").html(response);

				setTimeout(function() {
					$(".alert-success").hide(animation_duration);
				}, 3000);
			}
		});

		return false;
	});


	$(".cargarExcel").click(function(){

		var upload = $("input[name=upload]", $(this)).val();

		$.ajax({
			url:"/report/upload" ,
			type: "post",
			data: {load: upload},
			success: function(response)
			{
				alert("Se generó excel");
			}
		});

	});

});


