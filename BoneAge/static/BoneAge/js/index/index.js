$("tr[id^=evaluator]").click(function () { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/"
});
$("div[id^=evaluator]").click(function () { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/"
});