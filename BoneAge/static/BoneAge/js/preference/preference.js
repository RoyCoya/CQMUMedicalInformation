/* 偏好设置 */

// 初始化
$(document).ready(function () {
    $('#index_standard').val(index_standard);
    $('#chn_default_bone').val(chn_default_bone);
    $('#rus_default_bone').val(rus_default_bone);
});

// 保存设置
$('#preference').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    formData.append('shortcut', $("#shortcut").prop('checked')? "True":"False");
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
