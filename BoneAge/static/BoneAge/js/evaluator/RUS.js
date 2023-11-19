/* RUS全局方法 */

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
            $("#bone_discription_img").attr("src", url_static + "BoneAge/img/RUS/" + bone_name_key + "-" + bone['level'] + ".png")
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
            $("#bone_details_level_label").text(bone['level'] + " | " + Level_14_8[bone_name_key][bone['level']])
            $("#level-" + bone_name_key).text(bone['level'] + " | " + Level_14_8[bone_name_key][bone['level']] + "级")
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
            grade += Level_Grade[sex][bone_name_key][bone_details['level']]
        })
        $.each(Grade_Age[sex], function(index,interval){
            if(grade >= interval['min'] && grade <= interval['max']){
                bone_age = interval['score'];
                return false;
            }
        })
        if(bone_age >= 0){
            $("#bone_age").val(bone_age);
            $("#label_bone_age").text(bone_age);
            $("#label_bone_grade").text(grade);
            // 差距过大提示
            if(Math.abs(actual_age - bone_age) >= 1){
                $("#warning_age_misregistration").removeAttr('hidden');
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

/* RUS页面初始化 */
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
    $.fn.switch_bone(default_bone)

    /* 焦点至评级条 */
    $("#bone_details_level").focus()

    /* 如果数据库中存在骨龄数据，则用数据库中的值 */
    if(task['bone_age'] >= 0){
        $("#bone_age").val(task['bone_age']);
        $("#label_bone_age").text(task['bone_age']);
    }
});

/* 评分评级修改后修改骨骼等级，弹出保存按钮 */
$("#bone_details_level").on('input', function (e) { 
    var bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
    var bone = bones[bone_name_key]
    level = bone['level']
    $("#level-fifth-metacarpal").removeClass('text-danger')
    $("#bone_details_level_label").text($(this).val() + " | " + Level_14_8[bone_name_key][$(this).val()])
    $("#level-" + bone_name_key).text(bone['level'] + " | " + Level_14_8[bone_name_key][bone['level']] + "级")
    $("#modify_bone_detail").removeAttr('hidden')
    if($(this).val() >= 0){
        $("#bone_discription").removeAttr("hidden", "hidden");
        $("small[id^=bone_discription_text_]").attr('hidden', 'hidden')
        $("#bone_discription_text_" + bone_name_key + "_" + $(this).val()).removeAttr('hidden', 'hidden')
        $("#bone_discription_img").attr("src", url_static + "BoneAge/img/RUS/" + bone_name_key + "-" + $(this).val() + ".png")
    }
    else{
        $("#bone_discription").attr('hidden','hidden')
    }
    
    bone['level'] = $("#bone_details_level").val()
    $.fn.update_bone_age()
    bone['level'] = level
});

/* 骨龄复制到剪贴板 */
$("#label_bone_age").click(async function (e) { 
    var text = "骨龄（左手）：约" + $(this).text() + "岁。";
    try{
        await navigator.clipboard.writeText(text);
        alert("已复制到剪贴板：\n" + text);
    } catch(e){
        alert('发生错误：' + e)
    }
});

/* 骨骼分数复制到剪贴板 */
$("#label_bone_grade").click(async function (e) { 
    var text = "按RUS-CHN法测算，左手、腕骨发育成熟度评分为" + $(this).text() + "分。";
    try{
        await navigator.clipboard.writeText(text);
        alert("已复制到剪贴板：\n" + text);
    } catch(e){
        alert('发生错误：' + e)
    }
});