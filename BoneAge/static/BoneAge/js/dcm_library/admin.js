/* 自定函数 */

/* 全局对象 */
//csrf token
const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();
const csrftoken = getCookie('csrftoken');

//上传时显示旋转圈
$("#upload_dcms").click(function (e) { 
    $("#spinner_upload").removeAttr('hidden','hidden');
});

//解析时显示旋转圈
$("#analyze").click(function (e) { 
    $("#spinner_analyze").removeAttr('hidden','hidden');
});