$(function(){
$(".btn-default").click(function(){
    $(".btn-perm-bot").css("display", "inline");
    $(".btn-perm").css("display", "none");
    $(".btn-cellars-bot").css("display", "inline");
    $(".btn-cellars").css("display", "none");
});

});

var text;
function addElement(texto){

/*    var perm = document.getElementById("perm");
    var a = document.createElement("a");
    a.id="perm_top"+texto;
    a.className="btn-sm btn-primary";*/
    //a.onclik=addElementBot(texto);
/*    a.onclick = function() { 
        alert('blah'); 
        var perm = document.getElementById("perm_bot");
        var a = document.createElement("a");
        a.id="perm_"+texto;
        a.className="btn-sm btn-primary";
        //a.onclick=addElement(texto);
        a.innerHTML = texto;
        perm.appendChild(a);

        var elem = document.getElementById("perm_top"+texto);
        elem.parentNode.removeChild(elem);
        text=texto;

    };*/

/*    a.innerHTML = texto;
    perm.appendChild(a);*/

    //delete element
/*    var elem = document.getElementById("perm_"+texto);
    elem.parentNode.removeChild(elem);
    text=texto;*/
    $("#perm_"+texto).css("display", "none");
    $("#perm_top"+texto).css("display", "inline");
    

}

function removeElement(texto){

    $("#perm_"+texto).css("display", "inline");
    $("#perm_top"+texto).css("display", "none");


    //alert('blah'); 
/*        var perm = document.getElementById("perm_bot");
        var a = document.createElement("a");
        a.id="perm_"+texto;
        a.className="btn-sm btn-primary";
        a.innerHTML = texto;
        perm.appendChild(a);

        var elem = document.getElementById("perm_top"+texto);
        elem.parentNode.removeChild(elem);
        text=texto;*/
}

function addElementCellars(texto){
    $("#cellars_"+texto).css("display", "none");
    $("#cellars_top"+texto).css("display", "inline");
}

function removeElementCellars(texto){

    $("#cellars_"+texto).css("display", "inline");
    $("#cellars_top"+texto).css("display", "none");


    //alert('blah'); 
/*        var perm = document.getElementById("perm_bot");
        var a = document.createElement("a");
        a.id="perm_"+texto;
        a.className="btn-sm btn-primary";
        a.innerHTML = texto;
        perm.appendChild(a);

        var elem = document.getElementById("perm_top"+texto);
        elem.parentNode.removeChild(elem);
        text=texto;*/
}