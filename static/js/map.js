// 初始化地圖及設定
var map;
function initMap(){
    var url = location.href
    url = new URL(url);
    let longitude = url.searchParams.get('longitude')
    let latitude = url.searchParams.get('latitude')
    var lat_lng = { lat: parseFloat(latitude), lng: parseFloat(longitude) }
    map = new google.maps.Map(document.getElementById('map'), {
        center: lat_lng,
        zoom: 18,
    });
    var marker = new google.maps.Marker({
        position: lat_lng,
        map: map,
        label: '醫'
    });
}