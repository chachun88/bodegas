$(document).on('pjax:end ready', function(){
    var type_id = $("#user_type_id").val();
    $("select#type_id").val(type_id);
});