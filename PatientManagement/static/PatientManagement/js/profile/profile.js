$(document).ready(function () {
    console.log(info_tab);
    if(info_tab!=""){
        $("#nav_" + info_tab).addClass('active');
        $("#tab_" + info_tab).addClass('active');
    }
    else{
        $("#nav_overview").addClass('active');
        $("#tab_overview").addClass('active');
    }
});