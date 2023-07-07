/* 全局对象 */
//csrf token
const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();
const csrftoken = getCookie('csrftoken');
// 提交成功modal
var modal_allocation_submited = new bootstrap.Modal($('#modal_allocation_submited'), {keyboard: false})

// dcm全选，更新选中dcm计数
$("#select_all").click(function (e) { 
    if($("#select_all_checkbox").attr('checked') == 'checked'){
        $("#unallocated_dcms tbody input").removeAttr('checked');
        $("#select_all_checkbox").removeAttr('checked');
    }
    else{
        $("#unallocated_dcms tbody input").attr('checked', 'checked');
        $("#select_all_checkbox").attr('checked', 'checked');
    }
    $("#selected_dcm_count").text($('#unallocated_dcms tbody input[checked="checked"]').length);
});

// 单个dcm选中，更新选中dcm计数（点击单元格）
$("#unallocated_dcms tbody tr").click(function (e) {
    if($("#allocate_" + $(this).attr('id').substring(5)).attr('checked') == 'checked'){
        $("#allocate_" + $(this).attr('id').substring(5)).removeAttr('checked');
    }
    else{$("#allocate_" + $(this).attr('id').substring(5)).attr('checked', 'checked')}
    if($("#unallocated_dcms input[id^=allocate_]:not([checked])").length > 0){
        $("#select_all_checkbox").removeAttr('checked');
    }
    else $("#select_all_checkbox").attr('checked', 'checked');
    $("#selected_dcm_count").text($('#unallocated_dcms tbody input[checked="checked"]').length);
});

// 提交任务分配
$("#allocate_tasks").click(function (e) { 
    dcms_id = ''
    $.each($('#unallocated_dcms tbody input[checked^="checked"]'), function () { 
        dcms_id += ($(this).attr('id').substring(9)) + ' '
    });
    if(dcms_id.length > 0){
        $.ajax({
            type: "post",
            url: url_api_allocate_tasks,
            data: 
            {
                'dcms_id' : dcms_id,
                'allocate_standard' : $("#allocate_standard option:selected").val(),
                'allocated_to' : $("#allocated_to option:selected").val(),
            },
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken}
        });
    }
    modal_allocation_submited.show()
});

// 分配确认
$("#submit_confirm").click(function (e) { 
    window.location.replace(location)
});