/* 搜索结果点击跳转至评分器 */
$("tbody tr").click(function (e) { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id').replace('task_','') + "/"
});