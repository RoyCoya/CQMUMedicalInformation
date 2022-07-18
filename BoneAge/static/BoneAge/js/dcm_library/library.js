$("tbody tr").click(function (e) { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id') + "/"
});