var urlParams = new URLSearchParams(window.location.search);
/* 加载已经存在的查询条件 */
$(document).ready(function () {
    $('#filter input').each(function () {
        var inputName = $(this).attr('name');
        if (urlParams.has(inputName)) {
            $(this).val(urlParams.get(inputName));
        }
    });
});

/* 搜索结果点击跳转至评分器 */
$("tbody tr").click(function (e) { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id').replace('task_','') + "/"
});