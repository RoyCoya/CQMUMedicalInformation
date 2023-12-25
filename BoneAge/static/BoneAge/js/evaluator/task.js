/* 评测员提交任务错误至管理员进行审核 */
$("#confirm_report").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_report,
        data: { 
            "id": task["id"],
            "comment" : $("#comment_report").val()
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});

/* 评测员提交完成任务至管理员进行审核 */
$("#confirm_submit").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_submit,
        data: { 
            "id": task["id"], 
            "comment" : $("#comment_submit").val()
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});

/* 评测员撤回上次提交的审核申请 */
$("#confirm_withdraw").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_withdraw,
        data: { 
            "id": task["id"],
            "comment" : $("#comment_withdraw").val()
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});

/* 管理员通过任务完成审核 */
$("#confirm_verify_submit").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_verify,
        data: { 
            "id" : task["id"],
            "comment" : $("#comment_verify_submit").val()
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});

/* 管理员通过任务报错审核 */
$("#confirm_verify_report").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_verify,
        data: { 
            "id" : task["id"], 
            "type" : $("#verify_type").val(),
            "comment" : $("#comment_verify_report").val()
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.assign(url_personal_index);
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});

/* 管理员拒绝通过任务完成审核 */
$("#confirm_reject_submit").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_reject,
        data: { 
            "id" : task["id"],
            "comment" : $("#comment_reject_submit").val(),
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});
/* 管理员拒绝通过任务报错审核 */
$("#confirm_reject_report").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_reject,
        data: { 
            "id" : task["id"],
            "comment" : $("#comment_reject_report").val()
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});

/* 管理员删除任务 */
$("#confirm_delete").click(function (e) {
    post_data = {
        "id": task["id"],
        "type": $("#delete_type").val(),
        "comment" : $("#comment_delete").val()
    }
    $.ajax({
        type: "post",
        url: url_api_task_delete,
        data: post_data,
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.assign(url_personal_index);
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});

/* 管理员快捷完成任务 */
var task_notcompleted_modal = new bootstrap.Modal($('#modal_task_notcompleted'), { keyboard: false })
$("#confirm_finish").click(function (e) {
    var is_valid = true
    var bone_age = $("#bone_age").val()
    $.each(bones, function (bone_name_key, bone_details) {
        if (bone_details['level'] < 0) is_valid = false
        if (bone_details['error'] != 0) is_valid = false
    })
    if (bone_age == '') is_valid = false
    if (is_valid) {
        console.log(1)
        task['closed'] = true
        task['bone_age'] = bone_age
        task.comment = $("#comment_finish").val()
        $.ajax({
            type: "post",
            url: url_api_task_finish,
            data: task,
            dataType: "json",
            headers: { 'X-CSRFToken': csrftoken },
            success: function (data) {
                window.location.reload();
            },
            error: function (xhr, status, error) {
                var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
                alert(exception);
            }
        });
    }
    else {
        task_notcompleted_modal.show()
    }
    
});

// window.location.assign(url_personal_index);
/* 管理员重开任务 */
$("#confirm_reopen").click(function (e) {
    $.ajax({
        type: "post",
        url: url_api_task_reopen,
        data: {
            "id": task["id"],
            "comment" : $("#comment_reopen").val()
        },
        dataType: "json",
        headers: { 'X-CSRFToken': csrftoken },
        success: function (data) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            var exception = "【" + status + "】" + xhr.responseJSON.message + '\n' + error;
            alert(exception);
        }
    });
});
