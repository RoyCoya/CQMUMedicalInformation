var urlParams = new URLSearchParams(window.location.search);
/* 加载已经存在的查询条件 */
$(document).ready(function () {
    $('#form_filter input').each(function () {
        var inputName = $(this).attr('name');
        if (urlParams.has(inputName)) {
            $(this).val(urlParams.get(inputName));
        }
    });
});

/* ID导航器跳转至对应页面 */
$('#form_navigator').on('submit', function (e) {
    e.preventDefault();
    $.ajax({
        url: url_navigator,
        type: 'post',
        data: $('#form_navigator').serialize(),
        success: function (data) {
            if (data.url) {
                window.location.href = data.url;
            } else {
                alert('url传输丢失，请联系管理员检查代码');
            }
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    })
});

/* 筛选结果表单中点击任意任务跳转至对应评分器 */
$("tbody tr").click(function (e) { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id').replace('task_','') + "/"
});