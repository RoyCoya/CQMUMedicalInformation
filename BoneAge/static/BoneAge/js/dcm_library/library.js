$("tbody tr").click(function (e) { 
    console.log(1);
    window.location.href = "/boneage/evaluator/" + $(this).attr('id') + "/"
});