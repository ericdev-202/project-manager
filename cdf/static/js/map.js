	
function tryingmap(){


	var mapOptions = {
		center:[51.055207338584964,10.72265625],
		zoom:6
	}
	//creating mao object
	var map = new L.map('map', mapOptions);
	//creating a layer object
	var layer = new L.tileLayer('http://server.arcgisonline.com/ArcGis/rest/services/World_Imagery/Mapserver/tile/{z}/{y}/{x}');
	//adding layer to map
	map.addLayer(layer);

	 var marker = new L.Marker([51.055207338584964,10.72265625]);
	 marker.addTo(map);
	 function GetColor(pop){
	 	if(pop>10000000){
	 		return "brown";
	 	}else if(pop>5000000){
	 		return "blue";
	 	}else if(pop>2000000){
	 		return "lime";
	 	}else{
	 		return "pink";
	 	}
	 }
	 function StateStyle(feature){
	 	return{
	 		fillColor:GetColor(feature.properties.population) ,
	 		weight: 2,
	 		opacity: 1,
	 		color:"white",
	 		dashArray:4,
	 		fillOpacity:0.9,
	 	}
	 }

	 var stateslayer = L.geoJson(states, {style:StateStyle}).addTo(map);
	 // var countylayer = L.geoJson(counties).addTo(map);

	 var legend = new L.control({position:"bottomright"});
	 legend.onAdd = function(map){
	 	var div = L.DomUtil.create('div','legend');
	 	var labels = [
	 		'Population greater than 10000000',
	 		'Population greater than 5000000',
	 		'Population greater than 2000000',
	 		'Population equal or less than 2000000',
	 	];
	 	var grades = [10000001,5000001,2000001,2000000];
	 	div.innerHTML = '<div><b>Legend</b></div>';
	 	for(var i = 0; i<grades.length; i++){
	 		div.innerHTML+='<i style="background:'
	 		 + GetColor(grades[i]) + '">&nbsp;&nbsp; </i> &nbsp;&nbsp;' 
	 		 + labels[i]+'<br/>';
	 	}
	 	return div;
	 }
	 legend.addTo(map);

	 map.on('click',function(e){
	 	new L.Marker([e.latlng.lat,e.latlng.lng]);
	 	alert(e.latlng.lat+","+e.latlng.lng)
	 });
	 //https://askubuntu.com/questions/490950/create-wifi-hotspot-on-ubuntu
	 }