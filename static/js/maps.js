var map;
var position;
var center
//導入網頁call api取座標全部北市位置
console.log("go");
var url = location.href;
url = new URL(url);
let area = url.searchParams.get('area').replaceAll("'","");
console.log("/Maps?area=" + area);
$.ajax({
    url: "/Maps?area=" + area,
    method: "POST",
    dataType: "html",
    async:false,
    contentType:"application/json; charset=utf-8",
    }).then(result => {
        center_setting()
        return JSON.parse(result)
    }).then(result => {
        position= result;
        if(result.length != null)
        {
            $("body").append('<script src="https://maps.googleapis.com/maps/api/js?key={google key}"></script>');
        }
    })

function center_setting()
{
    switch (area) {
      case '臺北市':
      case '新北市':
        center= { lat: 25.03746, lng: 121.564558 };
        break;
      case '臺南市':
        center= { lat: 23.1417, lng: 120.2513 };
        break;
    default:
       alert('Default case');
       break;
    }
}


//google map初始化級多個地標標點

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: center
  });

  for (var i = 0; i < position.length; i++) {
    addMarker(i);
  }
  function addMarker(e) {
      var lat_lng = { lat: parseFloat(position[e].lat), lng: parseFloat(position[e].lng) }
      position[e] = new google.maps.Marker({
        position: lat_lng,
        map: map
      });
    }
}



