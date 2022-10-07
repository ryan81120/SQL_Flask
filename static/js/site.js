//共用ALERT mod by Ryan
function TargetAlert(result) {
    if (result.code == 1) {
        Swal.fire({
            title: result.title,
            html: result.msg,
            icon: 'success',
        }).then((confirm) => {
            if (confirm.isConfirmed) {
                if (location.href.indexOf("Server") != -1) {
                   document.location.href = '/Home';
                }else
                {
                    window.location.href = location.href;
                }
            };
       })
    }else if (result.code == 4) {
        Swal.fire({
            title: result.title,
            html: result.msg,
            icon: 'info',
        });
    }
}

//寄信反饋

function sendmail()
{
    let data = {"problem": $('#Problem').val(),
            "email": $('#Email').val(),
            "statement": $('#Statement').val()}
        $("button").attr("disabled", "disabled");
        $.ajax({
            url: "/Home/Server",
            method: "POST",
            data: JSON.stringify(data),
            dataType: "html",
            contentType:"application/json; charset=utf-8",
        }).then(result => {
         return JSON.parse(result)
         }).then (result => {
                console.log(result);
                TargetAlert(result);
        })
}
