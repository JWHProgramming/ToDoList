$(document).ready(function(){
    $(".input_cbox").click(function(){
        var dv = $(this).attr("data-attr");
        var $el = document.getElementById("item_"+dv+"_form");
        $el.submit(function(e){
            e.preventDefault();
            $.ajax({
                method:"POST",
                url : "complete/"+dv,
                data : $el.serialize()
                })
        });
})




})

