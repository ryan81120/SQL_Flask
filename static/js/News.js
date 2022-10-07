//時間初始化
$(function(){
	$("#InstantTime").flipcountdown({
		size:"sm"
	});
})
//DataTable語言包
$(function () {
    $("#News").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Chinese-traditional.json",
            "emptyTable": "查無資料",
        }
    });
});

$(document).ajaxStart(function() {
  $("#loading_img").show();
});

$(document).ajaxStop(function() {
  $("#loading_img").hide();
});

//更新新聞
function update_new()
{
    $.ajax({
            url: "/News/Update",
            method: "POST",
        }).then(result => {
         return JSON.parse(result)
         }).then (result => {
                TargetAlert(result);
        })

}