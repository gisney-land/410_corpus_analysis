$(document).ready(function(){
    $("#file").on("change", function(e){
        var files = $(this)[0].files;
        if (files.length >= 2){
            alert("you can only choose one file!");
        }
        else{
            var filename = e.target.value.split('\\').pop();
            $("#label_span").text(filename);
        }
    })
})