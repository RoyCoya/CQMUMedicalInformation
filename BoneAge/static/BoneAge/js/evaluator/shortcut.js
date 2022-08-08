/* 任务切换到达边界的提示modal*/
var task_no_pre_modal = new bootstrap.Modal($('#modal_task_no_pre'), {keyboard: false})
/* 任务切换到达边界的提示modal*/
var task_no_next_modal = new bootstrap.Modal($('#modal_task_no_next'), {keyboard: false})

$(document).keypress(function (e) { 
    keycode = e.keyCode
    if($('.modal').hasClass('show')) return;
    console.log(keycode);
    switch(keycode){
        /* 回车保存骨骼信息，并自动向下切换 */
        case(13) : $("#modify_bone_detail").trigger('click');
        /* 按s向下切换骨骼 */
        case(115) : {
            bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
            index = bone_order.indexOf(bone_name_key);
            index += 1;
            if(index == bone_order.length) index=0;
            bone_name_key = bone_order[index]
            $("span[id^=view-]").parent().removeClass('active')
            $("span[id^=error-]").parent().removeClass('active')
            $("a[id^=fix-").attr('hidden','hidden')
            $("#view-" + bone_name_key).parent().addClass('active')
            $.fn.switch_bone(bone_name_key)
            cropper.setData(bones[bone_name_key])
            break;
        }
        /* 按w向上切换骨骼 */
        case(119) : {
            bone_name_key = $(".list-group-item-action.active>span[id^=view-]").attr('id').substring(5)
            index = bone_order.indexOf(bone_name_key);
            index -= 1;
            if(index == -1) index=bone_order.length-1;
            bone_name_key = bone_order[index]
            $("span[id^=view-]").parent().removeClass('active')
            $("span[id^=error-]").parent().removeClass('active')
            $("a[id^=fix-").attr('hidden','hidden')
            $("#view-" + bone_name_key).parent().addClass('active')
            $.fn.switch_bone(bone_name_key)
            cropper.setData(bones[bone_name_key])
            break;
        }
        /* 按a切换上一项任务 */
        case(97) : {
            if(is_task_has_pre) window.location.href = url_task_pre;
            else task_no_pre_modal.show()
            break;
        }
        /* 按d切换下一项任务 */
        case(100) : {
            if(is_task_has_next) window.location.href = url_task_next;
            else task_no_next_modal.show()
            break;
        }
        default:;
    }
});