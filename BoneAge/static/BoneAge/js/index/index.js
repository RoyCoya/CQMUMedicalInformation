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
});

/* 列表表头排序跳转 */
$("#tasks th[id^=order_]").click(function () {
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
$("#tasks tr[id^=evaluator]").click(function () { 
    window.location.assign("/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/")
});
$("#tasks div[id^=evaluator]").click(function () { 
    window.location.assign("/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/")
});

/* 页面跳转 */
$("#page_jump").click(function (e) { 
    page_jump_number = $("#page_jump_number").val();
    if(page_jump_number < 1) page_jump_number = 1;
    else if(page_jump_number > page_count) page_jump_number = page_count;
    page_jump_url = $("#page_jump_url").text().replace('/0/', '/' + page_jump_number + '/');
    window.location.assign(page_jump_url)
});