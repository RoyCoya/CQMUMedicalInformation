/* 全局对象 */
//csrf token
const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();
const csrftoken = getCookie('csrftoken');
// 进入页面时的默认骨骼调整
if(bone_fixed != undefined){    
    default_bone = bone_fixed;
    $("#view-" + default_bone).parent().addClass('active');
}
else{ $("#view-" + default_bone).parent().addClass('active'); }

/* image cropper初始化 */
var image = $('#dcm');
image.cropper({
    preview : '.img-preview',
    viewMode : 2,
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
    if(!task['closed']){ $("#save_offset").removeClass('invisible'); }
});
$("#brightness_down").click(function (e) {
    brightness -= 20
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    crop_brightness = brightness - 12
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ crop_brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    if(!task['closed']){ $("#save_offset").removeClass('invisible'); }
});
$("#contrast_up").click(function (e) {
    contrast += 5
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    if(!task['closed']){ $("#save_offset").removeClass('invisible'); }
});
$("#contrast_down").click(function (e) {
    contrast -= 5
    $("div[class=cropper-canvas] img").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("div[class=cropper-crop-box]").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    $("#img_preview").css('filter', 'contrast('+ contrast +'%)' + 'brightness('+ brightness +'%)');
    if(!task['closed']){ $("#save_offset").removeClass('invisible'); }
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
    cropper.setData(bones[bone_name_key])
    cropper.setDragMode('crop')
});

/* 备注修改后弹出保存按钮 */
$("#bone_details_remarks").on('input', function () {
    $("#modify_bone_detail").removeAttr('hidden')
});

/* 骨骼修复错误定位 */
$("a[id^=fix-]").click(function (e) { 
    var bone_name_key = $(this).attr('id').substring(4);
    var bone = bones[bone_name_key]
    bone['error'] = 202
    bone['error_message'] = "未评估"
    bone['x'] = cropper.getData()['x']
    bone['y'] = cropper.getData()['y']
    bone['width'] = cropper.getData()['width']
    bone['height'] = cropper.getData()['height']
    //将定位错误的group item重组为一个正常的骨骼group item
    var new_bone_group_item = '<span id="view-' + bone_name_key + '" class="col-12">'
    new_bone_group_item += '<span>' + bone['name'] + '</span>：'
    if(bone['level'] >= 0) new_bone_group_item += '<span id="level-'+ bone_name_key + '">' + bone['level'] + '级</span>'
    else new_bone_group_item += '<span id="level-' + bone_name_key + '"><i class="bi bi-exclamation-triangle-fill text-danger">未评估</i></span>'
    new_bone_group_item += "</span>"
    $(this).parent().html(new_bone_group_item)
    $.fn.switch_bone(bone_name_key)
    $.ajax({
        type: "post",
        url: url_api_modify_bone_position,
        data: bone,
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
    if(String(location).includes('?')) window.location.assign(location + "&bone_fixed=" + bone_name_key);
    else window.location.assign(location + "?bone_fixed=" + bone_name_key);
});

/* 骨骼修改评分评级保存 */
$("#modify_bone_detail").click(function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    var bone = bones[bone_name_key]
    bone['error'] = 0
    bone['error_message'] = "正常"
    bone['level'] = $("#bone_details_level").val()
    bone['level_message'] = $("#bone_details_level").val() + " 级"
    $("span[id=level-" + bone_name_key + "]").text(bone['level_message'])
    $("span[id=level-" + bone_name_key + "]").removeClass('text-danger')
    bone['remarks'] = $("#bone_details_remarks").val()
    $.fn.switch_bone(bone_name_key)
    $.ajax({
        type: "post",
        url: url_api_modify_bone_detail,
        data: bone,
        dataType: "json",
        headers:{'X-CSRFToken': csrftoken}
    });
});

/* 骨骼修改定位保存 */
$('#modify_bone_position').click(function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    var bone = bones[bone_name_key]
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
    $("#bone_details_level").focus()
});

/* 修改时骨龄差距过大显示 */
$("#bone_age").change(function (e) {
    $(this).val($(this).val().replace(/[^\d\.]/g,''))
    bone_age = $(this).val()
    if($(this).val() < 0) $(this).val(0);
    if($(this).val() > 18) $(this).val(18);
    $("#warning_age_misregistration").attr('hidden','hidden')
    bone_age = $(this).val()
    $("#label_bone_age").text(bone_age);
    if(bone_age >= 0 && Math.abs(actual_age - bone_age) >= 1){
        $("#warning_age_misregistration").removeAttr('hidden');
    }
});

/* 收藏任务 */
// $("#task_marked").click(function (e) {
//     if($(this).hasClass('bi-star')){
//         $(this).removeClass('bi-star');
//         $(this).addClass('bi-star-fill');
//         $.ajax({
//             type: "post",
//             url: url_api_mark_task,
//             data: {
//                 'marked' : true,
//                 'task' : task['id'],
//             },
//             dataType: "json",
//             headers:{'X-CSRFToken': csrftoken}
//         });
//     }
//     else{
//         $.ajax({
//             type: "post",
//             url: url_api_mark_task,
//             data: {
//                 'marked' : false,
//                 'task' : task['id'],
//             },
//             dataType: "json",
//             headers:{'X-CSRFToken': csrftoken}
//         });
//         $(this).removeClass('bi-star-fill');
//         $(this).addClass('bi-star');
//     }
// });