/* 列表表头样式 */
$(document).ready(function () {
    $("th[id^=order_" + order + "]").addClass('order');
    is_descend == 1 ? 
        $("th[id^=order_" + order + "] i").addClass('bi-caret-down-fill') :
        $("th[id^=order_" + order + "] i").addClass('bi-caret-up-fill')
});

/* 列表表头排序跳转 */
$("th[id^=order_]").click(function () {
    order_next = $(this).attr("id").replace("order_","")
    if(order == order_next)
        is_descend = is_descend == 1 ? 0 : 1
    url = "/boneage/page/" +
        page_number +
        "/order/" +
        order_next
        + '/descend/' +
        is_descend + '/'
    window.location.href = url
});

/* 列表跳转 */
$("tr[id^=evaluator]").click(function () { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/"
});
$("div[id^=evaluator]").click(function () { 
    window.location.href = "/boneage/evaluator/" + $(this).attr('id').replace("evaluator_","") + "/"
});