/*
    通用变量、函数
*/
const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();
const csrftoken = getCookie('csrftoken');

/* 全局初始化内容 */
$(document).ready(function () {
    // 列表表头样式
    $("th[id^=order_" + order + "]").addClass('order');
    is_descend == 1 ? 
        $("th[id^=order_" + order + "] i").addClass('bi-caret-down-fill') :
        $("th[id^=order_" + order + "] i").addClass('bi-caret-up-fill')

    // 偏好设置
    $('#preference_standard').val(preference_standard);
    $('#preference_default_bone').val(preference_default_bone);
});

/* 列表表头排序跳转 */
$("th[id^=order_]").click(function () {
    order_next = $(this).attr("id").replace("order_","")
    if(order == order_next)
        is_descend = is_descend == 1 ? 0 : 1
    url = "page/" +
        page_number +
        "/?"+ "order=" +
        order_next
        + '&is_descend=' +
        is_descend
    if(tasks_finished) url = "/boneage/finished/" + url
    else url = "/boneage/" + url
    window.location.href = url
});

/* 任务列表跳转 */
$("tr[id^=evaluator]").click(function () { 
    window.location.replace("/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/" + back_page_params)
});
$("div[id^=evaluator]").click(function () { 
    window.location.replace("/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/" + back_page_params)
});

/* 偏好设置 */
// 开关快捷键
$("#preference_shortcut").click(function (e) { 
    $.ajax({
        type: "post",
        url: url_api_preference_switch_shortcut,
        data: {"shortcut" : this.checked,},
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
});
// 切换评测标准
// 切换默认骨骼
$('#preference_default_bone').change(function (e) { 
    $.ajax({
        type: "post",
        url: url_api_preference_switch_default_bone,
        data: {"default_bone" : $(this).val()},
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
});