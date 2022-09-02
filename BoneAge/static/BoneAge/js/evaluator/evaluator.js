/* 自定对象与函数 */

//切换骨骼时对骨骼详情部分（评分评级、备注、骨龄）的页面变化
$.fn.switch_bone = function(bone_name_key){
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $.fn.update_bone_age()
    var bone = bones[bone_name_key]
    if(bone['error'] == 0){
        $("#bone_discription").attr('hidden','hidden')
        $("#form_bone_details").removeAttr('hidden')
        $("#modify_bone_position").attr('hidden','hidden')
        $("#modify_bone_detail").attr('hidden','hidden')
        $('small[id^=bone_discription_text]').attr('hidden','hidden')
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
            $("#bone_details_level_label").text(bone['level'] + " | " + level14_to_level8[bone_name_key][bone['level']])
            $("#level-" + bone_name_key).text(bone['level'] + " | " + level14_to_level8[bone_name_key][bone['level']] + "级")
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
    $("#bone_details_level").focus()
};
/* 如果所有骨骼等级数据与定位正常，则计算分数并显示参考年龄 */
$.fn.update_bone_age = function(){
    $('#warning_age_misregistration').attr('hidden', 'hidden');
    $('#bone_age_great_differ_warning').hide();
    $("#bone_age").removeAttr('disabled');
    $("#bone_age").attr('placeholder','')
    $('#label_bone_age').removeClass('text-danger');
    $("#label_bone_age").text('');
    var is_valid = true
    $.each(bones, function(bone_name_key, bone_details){
        if(bone_details['level'] < 0) is_valid = false
        if(bone_details['error'] != 0) is_valid = false
    })
    if(is_valid){
        grade = 0
        bone_age = -1
        $.each(bones, function(bone_name_key,bone_details){
            grade += level_to_grade[sex][bone_name_key][bone_details['level']]
        })
        $.each(grade_to_age[sex], function(age,range){
            if(grade >= range['min'] && grade <= range['max']){
                bone_age = age
            }
        })
        if(bone_age >= 0){
            $("#bone_age").val(bone_age);
            $("#label_bone_age").text(bone_age + "岁");
            // 差距过大提示
            if(Math.abs(actual_age - bone_age) >= 1){
                $("#warning_age_misregistration").removeAttr('hidden');
                $("#bone_age_great_differ_warning").show()
            }
        }
    }
    else{
        $("#bone_age").attr('disabled', 'disabled');
        $("#bone_age").attr('placeholder', '*无法计算，骨骼数据存在错误*');
        $("#label_bone_age").addClass('text-danger');
        $("#label_bone_age").text('*无法计算*');
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
    modal: false,
    guides : false,
    data : bones[default_bone],
    cropmove(e){
        $("#modify_bone_position").removeAttr('hidden')
    }
});
var cropper = image.data('cropper');
image.on('ready', function () {
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
});

/* 其他初始化 */
$(document).ready(function () {
    /*popover提示框全局覆盖*/
    var tooltipTriggerList = Array.prototype.slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    //骨骼等级14转8
    $.fn.switch_bone('fifth-distal-phalange')
    $.fn.switch_bone('fifth-middle-phalange')
    $.fn.switch_bone('fifth-proximal-phalange')
    $.fn.switch_bone('fifth-metacarpal')
    $.fn.switch_bone('third-distal-phalange')
    $.fn.switch_bone('third-middle-phalange')
    $.fn.switch_bone('third-proximal-phalange')
    $.fn.switch_bone('third-metacarpal')
    $.fn.switch_bone('first-distal-phalange')
    $.fn.switch_bone('first-proximal-phalange')
    $.fn.switch_bone('first-metacarpal')
    $.fn.switch_bone('ulna')
    $.fn.switch_bone('radius')
    $.fn.update_bone_age()

    /* 选中默认骨骼 */
    $("#view-" + default_bone).parent().addClass('active');
    $.fn.switch_bone(default_bone)

    /* 焦点至评级条 */
    $("#bone_details_level").focus()

    /* 如果数据库中存在骨龄数据，则用数据库中的值 */
    if(task['bone_age'] >= 0){
        $("#bone_age").val(task['bone_age']);
        $("#label_bone_age").text(task['bone_age'] + "岁");
    }
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
$("#brightness_up").click(function (e) {
    brightness += 20
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    crop_brightness = brightness - 12
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ crop_brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#save_offset").removeClass('invisible')
});
$("#brightness_down").click(function (e) {
    brightness -= 20
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    crop_brightness = brightness - 12
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ crop_brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#save_offset").removeClass('invisible')
});
$("#contrast_up").click(function (e) {
    contrast += 5
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#save_offset").removeClass('invisible')
});
$("#contrast_down").click(function (e) {
    contrast -= 5
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#save_offset").removeClass('invisible')
});

/* 图像亮度对比度调整 */
$("#save_offset").click(function (e) { 
    $.ajax({
        type: "post",
        url: url_api_save_image_offset,
        data: 
        {
            'dcm_id' : dcm_id,
            'brightness' : brightness,
            'contrast' : contrast,
        },
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
    $("#save_offset").addClass('invisible')
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

/* 评分评级修改后弹出保存按钮 */
$("#bone_details_level").on('input', function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    var bone = bones[bone_name_key]
    level = bone['level']
    $("#level-fifth-metacarpal").removeClass('text-danger')
    $("#bone_details_level_label").text($(this).val() + " | " + level14_to_level8[bone_name_key][$(this).val()])
    $("#level-" + bone_name_key).text(bone['level'] + " | " + level14_to_level8[bone_name_key][bone['level']] + "级")
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
    
    bone['level'] = $("#bone_details_level").val()
    $.fn.update_bone_age()
    bone['level'] = level
});
/* 备注修改后弹出保存按钮 */
$("#bone_details_remarks").on('input', function () {
    $("#modify_bone_detail").removeAttr('hidden')
});

/* 骨骼修复错误定位 */
$("a[id^=fix-]").click(function (e) { 
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
    $("span[id=level-" + bone_name_key + "]").removeClass('text-danger')
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

/* 手动修改骨龄 */
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
        task['bone_age'] = bone_age
        $.ajax({
            type: "post",
            url: url_api_modify_bone_age,
            data: task,
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken}
        });
        bone_age_modal.hide()
    }
});
/* 修改时骨龄差距过大显示 */
$("#bone_age").on('input', function (e) {
    $(this).val($(this).val().replace(/[^\d\.]/g,''))
    bone_age = $(this).val()
    if($(this).val() < 0) $(this).val(0);
    if($(this).val() > 18) $(this).val(18);
    $("#bone_age_great_differ_warning").hide()
    $("#warning_age_misregistration").attr('hidden','hidden')
    bone_age = $(this).val()
    $("#label_bone_age").text(bone_age + '岁');
    if(bone_age >= 0 && Math.abs(actual_age - bone_age) >= 1){
        $("#warning_age_misregistration").removeAttr('hidden');
        $("#bone_age_great_differ_warning").show()
    }
});
/* 关闭骨龄输入页面时刷新骨龄 */
$('#modal_edit_bone_age button[data-bs-dismiss=modal]').click(function (e) { 
    $.fn.update_bone_age()
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
        if(!is_shortcut_enable) finish_task_modal.show();
        this.checked = true
        $('#label_task_status').text('已完成')
        $('#label_task_status').removeClass('text-success')
        $('#label_task_status').addClass('text-primary')
        task['closed'] = true
        task['bone_age'] = bone_age
        $.ajax({
            type: "post",
            url: url_api_finish_task,
            data: task,
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

/* 收藏任务 */
$("#task_marked").click(function (e) {
    if($(this).hasClass('bi-star')){
        $(this).removeClass('bi-star');
        $(this).addClass('bi-star-fill');
        $.ajax({
            type: "post",
            url: url_api_mark_task,
            data: {
                'marked' : true,
                'task' : task['id'],
            },
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken}
        });
    }
    else{
        $.ajax({
            type: "post",
            url: url_api_mark_task,
            data: {
                'marked' : false,
                'task' : task['id'],
            },
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken}
        });
        $(this).removeClass('bi-star-fill');
        $(this).addClass('bi-star');
    }
});