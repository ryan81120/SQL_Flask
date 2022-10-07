//時間初始化
$(function(){
	$("#InstantTime").flipcountdown({
		size:"sm"
	});
})
//DataTable語言包
$(function () {
    $("#hospital").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.24/i18n/Chinese-traditional.json",
            "emptyTable": "查無資料",
        }
    });
});


//初始化tooltip
$(function(){
    $('[data-toggle="tooltip"]').tooltip()
})


//colorbox

function colorbox(str, HospitalId=null) {
    if (str == "Add")
    {
        let url = "/Home/Add";
        $.colorbox({
        href: url,
        width: 700,
        height: 450,
        overlayClose: true
    });
    };
    if (str == "Edit")
    {
        let url = "/Home/Edit";
        $.colorbox({
        href: url,
        width: 700,
        height: 450,
        overlayClose: true,
        data:{HospitalId:HospitalId}
    });
    };

}


//編輯資料
function push(id) {
        let data = { "id": id,
            "hospitalname": $('#HospitalName').val(),
            "hospitaladdress": $('#HospitalAddress').val(),
            "telephone": $('#Telephone').val(),
            "url": $('#URL').val(),
             "longitude": $('#Longitude').val(),
             "latitude": $('#Latitude').val()}
        $.ajax({
            url: "/Home/Edit",
            method: "PUT",
            data: JSON.stringify(data),
            dataType: "html",
            contentType:"application/json; charset=utf-8",
        }).then(result => {
         $("#colorbox").colorbox.close();
         return JSON.parse(result)
         }).then (result => {
                console.log(result);
                TargetAlert(result);
            })
}


//新增資料

function add() {
        let data = {"hospitalname": $('#HospitalName').val(),
            "hospitaladdress": $('#HospitalAddress').val(),
            "telephone": $('#Telephone').val(),
            "url": $('#URL').val(),
             "longitude": $('#Longitude').val(),
             "latitude": $('#Latitude').val()}
        $.ajax({
            url: "/Home/Add",
            method: "POST",
            data: JSON.stringify(data),
            dataType: "html",
            contentType:"application/json; charset=utf-8",
        }).then(result => {
         $("#colorbox").colorbox.close();
         return JSON.parse(result)
         }).then (result => {
                console.log(result);
                TargetAlert(result);
            })
}


function del(id) {
        Swal.fire({
            title: '你確定要刪除嗎?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            confirmButtonText: "確定",
            cancelButtonColor: '#d33',
            cancelButtonText: "取消"
        }).then((result) => {
            console.log(result)
            if (result.isConfirmed) {
                $.ajax({
                url: "/Home/Del",
                method: "DELETE",
                data: JSON.stringify({"id": id}),
                dataType: "html",
                contentType:"application/json; charset=utf-8",
                }).then(result => {
                     $("#colorbox").colorbox.close();
                     return JSON.parse(result)
                     }).then (result => {
                            console.log(result);
                            TargetAlert(result);
                })
            }
        })
}


// openmap
function openmap(longitude, latitude)
{
    var url = `/Home/Map?longitude=${longitude}&latitude=${latitude}`
    window.open(url,'Map','toolbar=no,location=no,directories=no,width=800,height=600')
};

//search_byArea 地區搜尋
function search_byArea()
{
    var area = document.getElementById("areaid").value
    var township = ''
    if (location.pathname != '/Home/')
    {
        township = document.getElementById("townshipid").value
    }
//      window.location.href='/Home/Search?areaid=' + area ;
    window.location.href='/Home/Search?areaid=' + area + '&townshipid=' + township;
}


//地區變化自動更換行政區
$("#areaid").on("change", function () {
    var areaid = document.getElementById("areaid").value
    if (areaid == "")
    {
        $("#townshipid").attr("disabled", "disabled");
    }
    if (areaid != "" && location.pathname != '/Home')
    {
        $("#townshipid").removeAttr("disabled", "disabled");
        console.log("變化")
        $.ajax({
            type: "POST",
            url: "/Home/GetTownship",
            data: JSON.stringify({"areaid": areaid})
        }).done(function(result){
            $("#townshipid option").remove();
            if (result.length != 0) {
                for (var i = 0; i < result.length; i++) {
                    var option = `<option value=${result[i].Id}>${result[i].TownshipName}</option>`;
                    $("#townshipid").append(option);
            }
            }
        })
    }
});