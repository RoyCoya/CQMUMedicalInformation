/* 全局对象 */
//csrf token
const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();
const csrftoken = getCookie('csrftoken');
// modals
var modal_allocation_confirm = new bootstrap.Modal($('#modal_allocation_confirm'), {keyboard: false});
var modal_allocation_submited = new bootstrap.Modal($('#modal_allocation_submited'), {keyboard: false});
var modal_delete_confirm = new bootstrap.Modal($('#modal_delete_confirm'), {keyboard: false});
var modal_delete_submited = new bootstrap.Modal($('#modal_delete_submited'), {keyboard: false});

// 全选
$("#select_all").click(function (e) { 
    if($("#select_all_checkbox").attr('checked') == 'checked'){
        $("#unallocated_dcms tbody input").removeAttr('checked');
        $("#select_all_checkbox").removeAttr('checked');
        $("#unallocated_dcms tbody tr").css("background-color", "");
    }
    else{
        $("#unallocated_dcms tbody input").attr('checked', 'checked');
        $("#select_all_checkbox").attr('checked', 'checked');
        $("#unallocated_dcms tbody tr").css("background-color", "rgb(226,226,227)");
    }
    $("#selected_dcm_count").text($('#unallocated_dcms tbody input[checked="checked"]').length);
});

// 单个选中
$("#unallocated_dcms tbody tr").click(function (e) {
    var id = $(this).attr('id').substring(5)
    if($("#allocate_" + id).attr('checked') == 'checked'){
        $("#allocate_" + id).removeAttr('checked');
        $("#info_" + id).css("background-color", "");
    }
    else{
        $("#allocate_" + id).attr('checked', 'checked')
        $("#info_" + id).css("background-color", "rgb(226,226,227)");
    }
    if($("#unallocated_dcms input[id^=allocate_]:not([checked])").length > 0){
        $("#select_all_checkbox").removeAttr('checked');
    }
    else $("#select_all_checkbox").attr('checked', 'checked');
    $("#selected_dcm_count").text($('#unallocated_dcms tbody input[checked="checked"]').length);
});

// 回到顶端
$(window).scroll(function() {
  if ($(this).scrollTop() > window.innerHeight) {
    $("#back_to_top").show();
  } else {
    $("#back_to_top").hide();
  }
});
$("#back_to_top").click(function (e) { 
    $('html, body').animate({scrollTop: 0}, 'fast'); 
});

// 选择处理方式
$("#operation").change(function (e) { 
    switch ($(this).val()) {
        case "allocate": 
            $(".operation").removeClass("col-3");
            $(".operation").addClass("col-7");
            $("#selected_dcm_count").removeClass("text-danger");
            $("#submit").removeClass("btn-outline-danger");
            $("#selected_dcm_count").addClass("text-primary");
            $("#submit").addClass("btn-outline-primary");
            $(".allocate_choice").show();
            break;
        case "delete": 
            $(".operation").removeClass("col-7");
            $(".operation").addClass("col-3");
            $("#selected_dcm_count").removeClass("text-primary");
            $("#submit").removeClass("btn-outline-primary");
            $("#selected_dcm_count").addClass("text-danger");
            $("#submit").addClass("btn-outline-danger");
            $(".allocate_choice").hide();
            break;
        default: break;
    }
});
// 确认处理
$("#submit").click(function (e) { 
    if($("#selected_dcm_count").text() != "0"){
        switch ($("#operation").val()) {
            case "allocate": 
                modal_allocation_confirm.show();
                break;
            case "delete": 
                modal_delete_confirm.show();
                break;
            default: break;
        }
    }
});
// 分配任务
$("#allocation_confirm").click(function (e) { 
    modal_allocation_confirm.hide()
    modal_allocation_submited.show()
    dcm_id_list = ''
    $.each($('#unallocated_dcms tbody input[checked^="checked"]'), function () { 
        dcm_id_list += ($(this).attr('id').substring(9)) + ' '
    });
    standard_list = $('input.standard_select:checked').map(function() {return this.value;}).get();
    if(dcm_id_list.length > 0 && standard_list.length > 0){
        $.ajax({
            type: "post",
            url: url_api_allocate_tasks,
            data: 
            {
                'dcm_id_list' : dcm_id_list,
                'standard_list' : JSON.stringify(standard_list),
                'allocated_to' : $("#allocated_to option:selected").val(),
            },
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken},
            success : function(){
                
            },
            error : function(){
                
            },
        });
    }
});
// 删除任务
$("#delete_confirm").click(function (e) { 
    modal_delete_submited.show()
    dcm_id_list = ''
    $.each($('#unallocated_dcms tbody input[checked^="checked"]'), function () { 
        dcm_id_list += ($(this).attr('id').substring(9)) + ' '
    });
    if(dcm_id_list.length > 0){
        $.ajax({
            type: "post",
            url: url_api_delete_tasks,
            data: 
            {
                'dcm_id_list' : dcm_id_list,
                'type' : $('input[name="delete_type"]:checked').val(),
            },
            dataType: "json",
            headers:{'X-CSRFToken': csrftoken},
            success : function(){
                
            },
            error : function(){
                
            },
        });
    }
});