/* 自定函数 */

//切换骨骼时对骨骼详情部分（评分评级、备注）的页面变化
$.fn.switch_bone = function(bone_name_key){
    var bone = bones[bone_name_key]
    if(bone['error'] == 0){
        $("#bone_discription").attr('hidden','hidden')
        $("#form_bone_details").removeAttr('hidden')
        $("#modify_bone_position").attr('hidden','hidden')
        $("#modify_bone_detail").attr('hidden','hidden')
        $("#bone_details_name").text(bone['name'])
        $("#bone_details_remarks").val(bone['remarks'])
        if(bone['level'] > 0){
            $("#bone_discription").removeAttr("hidden", "hidden");
            $("#bone_discription_img").attr("src", "/static/BoneAge/img/" + bone_name_key + "-" + bone['level'] + ".png")
            $("#bone_discription_text_" + bone_name_key + "_" + bone['level']).removeAttr('hidden', 'hidden')
        }
        switch (bone_name_key) {
            case 'radius' : $("#bone_details_level").attr('max','14'); break;
            case 'ulna' : $("#bone_details_level").attr('max','12'); break;
            case 'first-metacarpal' : $("#bone_details_level").attr('max','11'); break;
            case 'third-metacarpal' : $("#bone_details_level").attr('max','10'); break;
            case 'fifth-metacarpal' : $("#bone_details_level").attr('max','10'); break;
            case 'first-proximal-phalange' : $("#bone_details_level").attr('max','12'); break;
            case 'third-proximal-phalange' : $("#bone_details_level").attr('max','12'); break;
            case 'fifth-proximal-phalange' : $("#bone_details_level").attr('max','12'); break;
            case 'third-middle-phalange' : $("#bone_details_level").attr('max','12'); break;
            case 'fifth-middle-phalange' : $("#bone_details_level").attr('max','12'); break;
            case 'first-distal-phalange' : $("#bone_details_level").attr('max','11'); break;
            case 'third-distal-phalange' : $("#bone_details_level").attr('max','11'); break;
            case 'fifth-distal-phalange' : $("#bone_details_level").attr('max','11'); break;
            default:
                alert('致命错误：json中未找到该骨骼');
        }
        if(bone['level'] >= 0){
            $("#bone_details_level_label").text(bone['level'])
            $("#bone_details_level").val(bone['level'])
        }
        else{
            $("#bone_details_level_label").text("？")
            $("#bone_details_level").val(0)
        }
    }
    else{
        $("#bone_details_name").text(bone['name'] + "（" + bone['error_message'] + "）")
        $("#form_bone_details").attr('hidden','hidden')
    }
};

/* 全局对象 */
//csrf token
const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();
const csrftoken = getCookie('csrftoken');
//骨龄填写的modal
var bone_age_modal = new bootstrap.Modal($('#modal_edit_bone_age'), {keyboard: false})
//任务存在未完成内容的提示modal
var task_notcompleted_modal = new bootstrap.Modal($('#modal_task_notcompleted'), {keyboard: false})
//完成任务的确认modal
var finish_task_modal = new bootstrap.Modal($('#modal_finish_task'), {keyboard: false})

/* image cropper初始化 */
var image = $('#dcm');
image.cropper({
    preview : '.img-preview',
    viewMode : 2,
    guides : false,
    movable : false,
    data : bones['radius'],
    cropmove(e){
        $("#modify_bone_position").removeAttr('hidden')
    }
});
var cropper = image.data('cropper');

/* 其他初始化 */
$(document).ready(function () {
    /*popover提示框全局覆盖*/
    var tooltipTriggerList = Array.prototype.slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
    /* 选中骨骼，默认从桡骨开始 */
    $("#view-radius").parent().addClass('active');
    $.fn.switch_bone('radius')
});


/* image cropper 工具栏 */
$('#setDragMode').click(function(e){
    $('#dcm').cropper('setDragMode','move');
});
$('#zoomIn').click(function(e){
    $('#dcm').cropper('zoom',0.1);
});
$('#zoomOut').click(function(e){
    $('#dcm').cropper('zoom',-0.1);
});
$('#resetCropper').click(function (e) { 
    var bone = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    cropper.setData(bones[bone])
});

/* 骨骼切换列表 */
$("span[id^=view-]").click(function (e) {
    $("span[id^=view-]").parent().removeClass('active')
    $("span[id^=error-]").parent().removeClass('active')
    $("a[id^=fix-").attr('hidden','hidden')
    $(this).parent().addClass('active')
    var bone_name_key = $(this).attr('id').substring(5);
    $.fn.switch_bone(bone_name_key)
    cropper.setData(bones[bone_name_key])
});
$("span[id^=error-]").click(function (e) {
    $("span[id^=view-]").parent().removeClass('active')
    $("span[id^=error-]").parent().removeClass('active')
    $("a[id^=fix-").attr('hidden','hidden')
    $(this).parent().addClass('active')
    var bone_name_key = $(this).attr('id').substring(6);
    $("#fix-" + bone_name_key).removeAttr('hidden')
    $.fn.switch_bone(bone_name_key)
    cropper.reset()
    cropper.setDragMode('crop')
});

/* 骨骼修复定位 */

/* 评分评级修改后弹出保存按钮 */
$("#bone_details_level").on('input', function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    $("#bone_details_level_label").text($(this).val())
    $("#modify_bone_detail").removeAttr('hidden')
    if($(this).val() > 0){
        $("#bone_discription").removeAttr("hidden", "hidden");
        $("small[id^=bone_discription_text_]").attr('hidden', 'hidden')
        $("#bone_discription_text_" + bone_name_key + "_" + $(this).val()).removeAttr('hidden', 'hidden')
        $("#bone_discription_img").attr("src", "/static/BoneAge/img/" + bone_name_key + "-" + $(this).val() + ".png")
    }
    else{
        $("#bone_discription").attr('hidden','hidden')
    }
});
/* 备注修改后弹出保存按钮 */
$("#bone_details_remarks").on('input', function () {
    $("#modify_bone_detail").removeAttr('hidden')
});

/* 骨骼修复错误定位 */
$("a[id^=fix-").click(function (e) { 
    var bone_name_key = $(this).attr('id').substring(4);
    var bone = bones[bone_name_key]
    bone['error'] = 0
    bone['error_message'] = "正常"
    bone['x'] = cropper.getData()['x']
    bone['y'] = cropper.getData()['y']
    bone['width'] = cropper.getData()['width']
    bone['height'] = cropper.getData()['height']
    //将定位错误的group item重组为一个正常的骨骼group item
    var new_bone_group_item = '<span id="view-' + bone_name_key + '" class="col-12">'
    new_bone_group_item += '<span>' + bone['name'] + '</span>：'
    if(bone['level'] >= 0) new_bone_group_item += '<span id="level-'+ bone_name_key + '">' + bone['level'] + '级</span>'
    else new_bone_group_item += '<span id="level-' + bone_name_key + '" class="text-danger">*' + bone['level_message'] + '*</span>'
    new_bone_group_item += "</span>"
    $(this).parent().html(new_bone_group_item)
    $("#view-" + bone_name_key).on('click',function (e) { 
        $("span[id^=view-]").parent().removeClass('active')
        $("span[id^=error-]").parent().removeClass('active')
        $("a[id^=fix-").attr('hidden','hidden')
        $(this).parent().addClass('active')
        bone = $(this).attr('id').substring(5);
        $.fn.switch_bone(bone)
        cropper.setData(bones[bone])
    });
    $.ajax({
        type: "post",
        url: url_api_modify_bone_position,
        data: bone,
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
    $.fn.switch_bone(bone_name_key)
});

/* 骨骼修改评分评级保存 */
$("#modify_bone_detail").click(function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    var bone = bones[bone_name_key]
    bone['level'] = $("#bone_details_level").val()
    bone['level_message'] = $("#bone_details_level").val() + " 级"
    $("span[id=level-" + bone_name_key + "]").text(bone['level_message'])
    $("span[id=level-" + bone_name_key + "]").removeClass('text-secondary')
    bone['remarks'] = $("#bone_details_remarks").val()
    $.ajax({
        type: "post",
        url: url_api_modify_bone_detail,
        data: bone,
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
    $.fn.switch_bone(bone_name_key)
});

/* 骨骼修改定位保存 */
$('#modify_bone_position').click(function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    var bone = bones[bone_name_key]
    bone['error'] = 0
    bone['error_message'] = "正常"
    bone['x'] = cropper.getData()['x']
    bone['y'] = cropper.getData()['y']
    bone['width'] = cropper.getData()['width']
    bone['height'] = cropper.getData()['height']
    $.ajax({
        type: "post",
        url: url_api_modify_bone_position,
        data: bone,
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
    $.fn.switch_bone(bone_name_key)
});

/* 修改骨龄 */
$("#confirm_edit_bone_age").click(function (e) { 
    var bone_age = $("#bone_age").val()
    if(bone_age == ''){
        $("#bone_age_invalid").show()
    }
    else{
        $("#bone_age_invalid").hide()
        bone_age = parseFloat(bone_age)
        $("#label_bone_age").text(bone_age + " 岁")
        $("#label_bone_age").removeClass('text-danger')
        bone_age_instance['bone_age'] = bone_age
        $.ajax({
            type: "post",
            url: url_api_modify_bone_age,
            data: bone_age_instance,
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken}
        });
        bone_age_modal.hide()
    }
});

/* 将本条评测任务标记为已完成 */
$("#task_closed").click(function (e) {
    var is_valid = true
    var bone_age = $("#bone_age").val()
    $.each(bones, function(bone_name_key,bone_details){
        if(bone_details['level'] < 0) is_valid = false
        if(bone_details['error'] != 0) is_valid = false
    })
    if(bone_age == '') is_valid = false
    if(is_valid){
        finish_task_modal.show()
        this.checked = true
        $('#label_task_status').text('任务已完成')
        $('#label_task_status').removeClass('text-success')
        $('#label_task_status').addClass('text-primary')
        bone_age_instance['closed'] = true
        $.ajax({
            type: "post",
            url: url_api_finish_task,
            data: bone_age_instance,
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken}
        });
    }
    else{
        task_notcompleted_modal.show()
        this.checked = false
    }
});

/* 完成任务，跳转至个人主页 */
$("#finish_task").click(function (e) { 
    window.location.replace(url_personal_index);
});