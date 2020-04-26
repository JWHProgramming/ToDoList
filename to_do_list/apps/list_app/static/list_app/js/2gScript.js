$(document).ready(function(){
    $(".input_cbox").click(function(){
        var dv = $(this).attr("data-attr");
        document.getElementById("item_"+dv+"_form").submit();
    })
})
