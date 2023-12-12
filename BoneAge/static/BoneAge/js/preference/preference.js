/* 偏好设置 */
$(document).ready(function () {
    // 初始化
    $('#preference_standard').val(preference_standard);
    $('#preference_default_bone').val(preference_default_bone);
});

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