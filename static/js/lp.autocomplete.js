(function($){
	$.fn.lpAutoComplete = function(options){
		var defaults = 
		{
			auto: true,
			showTitle:false,
			title:"Resultados",
			source:"/product/search",
			onSelect:function(result){}
		};

		// pisa las configuraciones por defecto por las del usuario
		var options = $.extend(defaults, options);
		var first_result = {"key":"", "value":""};

		var showResults = function(text, dom, input)
		{
			console.log(text);

			hholder = $(".lpac-holder", dom);
			html = "<ul>";

			$.ajax({
				type: "GET",
				url: options.source + "?q=" + input.val()
			}).done(function(data){
				
				results = eval(data);

				var is_first = true;
				first_result = {"key":"", "value":""};
				
				for (var i = 0; i <= results.length - 1; i++) 
				{
					if (is_first) 
					{
						first_result = {"key":results[i].key, "value":results[i].value};
						is_first = false;
					}

					html += "<li id='"+results[i].key+"'>" + results[i].value + "</li>";
				};
				html += "</ul>";

				hholder.html(html);

				$("li", hholder).click(function(){
					alert($(this).html());
				});
			});
		};

		var counter = 0;

		this.each(function(){
			self = $(this);
			self.attr("key", "");

			//self.css("position","relative");
			html_holder = "<div id='lpac-"+counter+"' style='position:absolute;display:none' class='lpac-tooltip'>";

			// adding title div
			if (options.showTitle) {
				html_holder+="<div class='lpac-title'>"+options.title+"</div>";
			}
			html_holder+="<div class='lpac-holder'></div></div>";

			self.after(html_holder);
			holder = $("#lpac-"+ counter);

			self.focus(function(){
				holder.css("display", "block");
				showResults(self.val(), holder, self);
			});

			self.keyup(function(){
				showResults(self.val(), holder, self);
			});

			self.blur(function(){
				self.val(first_result["value"]);
				self.attr("key", first_result["key"]);
				holder.css("display", "none");
				options.onSelect(first_result);
			});

			counter += 1;
		})
	}
})(jQuery);