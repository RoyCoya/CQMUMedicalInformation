/* 偏好设置 */

// 初始化
$(document).ready(function () {
    $('#index_standard').val(index_standard);
    $('#chn_default_bone').val(chn_default_bone);
    $('#rus_default_bone').val(rus_default_bone);
    var chn_order = new Sortable($("#bone_order_CHN").get(0),{
        animation: 300,
    });
    var rus_order = new Sortable($("#bone_order_RUS").get(0),{
        animation: 300,
    });
});

// 保存设置
$('#preference').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);

    // 启用快捷键与否
    formData.append('shortcut', $("#shortcut").prop('checked') ? "True" : "False");

    // 骨骼排序
    var bone_order_CHN = $('#bone_order_CHN li').map(function() { return $(this).attr('bone-name'); }).get().join('|');
    formData.append('bone_order_CHN', bone_order_CHN);
    var bone_order_RUS = $('#bone_order_RUS li').map(function() { return $(this).attr('bone-name'); }).get().join('|');
    formData.append('bone_order_RUS', bone_order_RUS);


    $.ajax({
        url: api_preference_save,
        type: 'post',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            alert(data.message);
        },
        error: function (xhr, status, error) {
            var exception = "【" + xhr.status + "】" + xhr.responseJSON.message;
            alert(exception);
        }
    })
});
