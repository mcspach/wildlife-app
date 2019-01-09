/**
 * @ David Bailey
 * Note: Main Javascript
 */

// Intiate jquery
$(document).ready(function (){

  var map, aDiv;
  var centerlatlng = L.latLng(39.614203, -105.285319);

  var southWest = L.latLng(-19.4758729,-166.6377901),
      northEast = L.latLng(76.6191662,-9.401469),
      bounds = L.latLngBounds(southWest, northEast)

  // Title Case function for Gen and Common Name
  function titleCase(str) {
    str.toLowerCase();
    var strAr = str.split(" ");
    for(var i=0;i<strAr.length;i++)
      {
        strAr[i] = strAr[i].charAt(0).toUpperCase() + strAr[i].substring(1).toLowerCase();
      }
        str = strAr.join(" ");
        return str;
      }

  // Creating a tile layer for basemap using MapBox
  var basemap1 = L.tileLayer('http://api.tiles.mapbox.com/v4/davidjbailey.jg612ji1/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZGF2aWRqYmFpbGV5IiwiYSI6InFxSzA5bjgifQ.tDw01mG43kf6hWUIAtBEAw#4/33.75/-117.87', {
            attribution: '<a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18
      });

	//Create our Map Object
	map = L.map('myMap', {
				center: centerlatlng,
				zoom:	10,
				maxBounds: bounds,
				minZoom: 4,
				zoomControl: false,
				fullscreenControl: false,
				layers: [basemap1]
			});

  // Create a point marker from GeoJSON housed in Geoserver via WFS
  var rootUrl = 'http://138.68.62.194:8080/geoserver/wildlife/ows';
  var getParameters = {
      service: 'WFS',
      version: '1.0.0',
      request: 'GetFeature',
      typeName: 'wildlife:wildlife_pt',
      maxFeatures: 500,
      outputFormat: 'text/javascript',
      format_options: 'callback: getJson'
  };

  // AJAX to get GeoJSON data
  var parameters = L.Util.extend(getParameters);
  var get_wfst = rootUrl + L.Util.getParamString(parameters)
  console.log(get_wfst)

  $.ajax({
      url: get_wfst,
      dataType: 'jsonp',
      jsonpCallback: 'getJson',
      success: handleJson
  });

  // Read GeoJSON data | specify what icons are used and make it into a point on map
  function handleJson(data) {

    L.geoJson(data, {
      pointToLayer: function (feature, latlng) {
        var marker_var = L.marker(latlng)
        return marker_var;
      },
      onEachFeature: function (feature, layer) {
        //set marker icon
        var myIcon = L.icon({
          iconUrl: feature.properties["marker"],
          iconSize: [25, 28]
        });
        layer.setIcon(myIcon);

        // popup for each marker
        wildlife_popup = "<dl><dt>" + titleCase(feature.properties["gen_name"]) + "</dt>"+
                          "<dd>Common Name: " + titleCase(feature.properties["com_name"]) + "<dd>"+
                          "<dd>Comments: " + feature.properties["comments"] + "<dd>"+
                          "<dd>Date: " + feature.properties["encountered_date"] + "<dd>"+
                          "<dd>What Time: " + feature.properties["encountered_time"] + "<dd>"+
                          "<dd>" + feature.properties["photo_s3_url1"] + "<dd>"

        layer.bindPopup(L.Util.template(wildlife_popup, feature.properties));

        }

    }).addTo(map);//.bindPopup(wildlife_popup);

  }; // END of handleJson Function



  // Adding a zoom in and out button
	L.control.zoom({ position: 'bottomright' }).addTo(map);
	//Adding a Scale Control
	L.control.scale().addTo(map);

  // Creating points - add to PostGIS (hosted by Geoserver)

  // Set the button title text for the polygon button
  L.drawLocal.draw.toolbar.buttons.marker = 'Add a Wildlife Sighting!';
  // Marker to draw (add point)
  var AddMarker = L.icon({
    iconUrl: "icons/add_marker.png",
    iconSize: [27, 30]
  });

  var post_wfs = 'http://138.68.62.194:8080/geoserver/cite/wfs';

  var postParameters = {
      service: 'WFS',
      version: '1.1.0',
      request: 'Transaction',
      typeName: 'cite:wildlife_pt',
      maxFeatures: 500,
      outputFormat: 'text/xml'
      //format_options: 'callback: jQuery'
      };

  var parameters2 = L.Util.extend(postParameters);
  var post_wfst = post_wfs + L.Util.getParamString(parameters2)

  // Drawing format_options
  var options = {
        position: 'topleft',
        draw: {
            polyline: false, // Turns off this drawing tool
            polygon: false, // Turns off this drawing tool
            circle: false, // Turns off this drawing tool
            rectangle: false, // Turns off this drawing tool
            marker: {
                icon: AddMarker
            },
        edit:{featureGroup: post_wfst} }
        }

  // Create Drawing tool
  var drawControl = new L.Control.Draw(options)
  map.addControl(drawControl);

  // Add point to map and load into PostGIS
  map.on('draw:created', function (e) {
    var marker_coord = JSON.stringify(e.layer.toGeoJSON());
    console.log(marker_coord)

    //var common_name_placeholder = "HELLO"

    var layer = e.layer,
        type = e.layerType;
        point = layer.toGeoJSON()
        lng = point.geometry.coordinates[0]
        lat = point.geometry.coordinates[1]
        console.log(lng)

  // Submit form for wildlife Sighting
    if (type === 'marker') {
        map.addLayer(layer);

        //'<div class="ui-widget">'+
          //'<label for="common_name"><strong>Common Name</strong></label>'+ "<br>" +
          //'<input id="common_name"/>'+
      //'</div>'+

          var popup = L.popup({maxWidth: 1400})
             .setLatLng(layer.getLatLng())
             // next to river, next to trail, on trail, in the river, next to lake, in the lake, on road, next to road, in field
             .setContent('<form role="form" id="form" enctype="multipart/form-data" onsubmit="addMarker()">'+

                      '<div class="form-group">'+
                       '<label class="control-label col-sm-10"><strong>What animal did you see?</strong></label>'+ "<br>" +
                       '<input type="text" placeholder="Bear, Snake, Coyote" id="animal" name="animal" class="form-control" required="true"/>'+
                   '</div>'+

                   '<div class="form-group">'+
                      '<label class="control-label col-sm-10"><strong>Common Name</strong></label>'+ "<br>" +
                      '<input type="text" placeholder="" id="common_name" name="common_name" class="form-control" required="true"/>'+
                  '</div>'+

                    '<div class="form-group">'+
                       '<label class="control-label col-sm-10"><strong>Date animal was seen </strong></label>'+ "<br>" +
                       '<input type="date" placeholder="8/1/2015" id="date" name="date" class="form-control" required="true"/>'+
                   '</div>'+

                   '<div class="form-group">'+
                       '<label class="control-label col-sm-10"><strong>Time animal was seen </strong> </label>'+ "<br>" +
                       '<input type="time" placeholder="Morning, Afternoon, or Night" id="time" name="time" class="form-control" required="true"/>'+
                   '</div>'+

                   '<div class="form-group">'+
                       '<label class="control-label col-sm-10"><strong>Comments </strong></label>'+ "<br>" +
                       '<input type="text" placeholder="Optional" id="comments" name="comments" class="form-control"/>'+
                   '</div>'+

                   '<div class="form-group">'+
                       '<label class="control-label col-sm-10"><strong>Upload Photo </strong></label>'+ "<br>" +
                       '<input type="text" placeholder="Optional" id="photo" name="photo" class="form-control"/>'+
                   '</div>'+

                   '<input style="display: none;" type="text" id="lat" name="lat" value="'+lat+'" />'+
                   '<input style="display: none;" type="text" id="lng" name="lng" value="'+lng+'" />'+

                   '<div class="form-group">'+
                         '<div style="text-align:center;" class="col-xs-11"><button style="text-align:center;" type="submit" id="submit" value="submit" class="btn btn-primary trigger-submit">Submit</button></div>'+
                   '</div>'+ "<br>" +

                   '</form>')
              .openOn(map);

              //oCell1.innerHTML = "<input type='text' class='nbtext' maxlength='500' name='rc_client' value='' >";

              //var common_names = ["ActionScript","Python","Ruby"];

              //initiate the plugin in the new input field
              //$(document).find('input').autocomplete({
                  //source: common_names,
                  //minLength: 2,
                  //messages: {
                      //noResults: '',
                      //results: function () {}
                  //}
              //});

              //$(document).on('#common_name', function() {

                //var common_names = ["ActionScript","Python","Ruby"];
                //autocomplete(document.getElementById("common_name"), common_names);

                //$(this).autocomplete({
                   //source:common_names,
                   //minLength:2
                //});
                //end of autocomplete function
                //});

/*
            $('#form').submit(function(e){
          		e.preventDefault();
          		});

*/
              // get timestamp using momment.js
              var ts_time = moment().format('hh:mm:ss'); // 2001-09-27 23:00:00
              console.log(ts_time);

              // get timestamp using momment.js
              var ts_date = moment().format('YYYY-MM-DD'); // 2001-09-27 23:00:00
              console.log(ts_date);

           	$('#submit').click(function(e) {
   	    	     console.log('clicked!');

               // gen_name MUST be populated
               var animal = document.getElementById('animal').value

               if (animal !== ""){

                 //conver to time to postgres time
                 var time = document.getElementById('time').value
                 console.log(time);

                 function convertTime12to24(time12h) {
                    const [time, modifier] = time12h.split(' ');

                    let [hours, minutes] = time.split(':');

                    if (hours === '12') {
                      hours = '00';
                    }

                    if (modifier === 'PM') {
                      hours = parseInt(hours, 10) + 12;
                    }

                    return hours + ':' + minutes + ':00';
                  }
                  var new_time = convertTime12to24(time)

                  console.log(convertTime12to24(new_time));

                 var postData =
                         '<wfs:Transaction\n'
                    + '  service="WFS"\n'
                    + '  version="1.1.0"\n'
                    + '  xmlns:cite="http://138.68.62.194:8080/geoserver/cite"\n'
                    + '  xmlns:wfs="http://www.opengis.net/wfs"\n'
                    + '  xmlns:gml="http://www.opengis.net/gml"\n'
                    + '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
                    + '  xsi:schemaLocation="http://www.opengis.net/wfs\n'
                    + '                      http://schemas.opengis.net/wfs/1.1.0/WFS-transaction.xsd\n'
                   + '                      http://138.68.62.194:8080/geoserver/cite\n'
                    + '                      http://138.68.62.194:8080/geoserver/cite/wfs/DescribeFeatureType?typename=cite:wildlife_pt">\n'
                    + '  <wfs:Insert>\n'
                    + '    <wildlife_pt>\n'
                    + '      <cite:point>\n'
                    + '        <gml:Point srsDimension="2" srsName="urn:x-ogc:def:crs:EPSG:4326">\n'
                    + '          <gml:coordinates decimal="." cs="," ts=" ">' + lat + ',' + lng + '</gml:coordinates>\n'
                    + '        </gml:Point>\n'
                    + '      </cite:point>\n'
                   + '      <cite:gen_name>' + document.getElementById('animal').value + '</cite:gen_name>\n'
                   + '      <cite:com_name>' + document.getElementById('common_name').value + '</cite:com_name>\n'
                   + '      <cite:encountered_date>' + document.getElementById('date').value + '</cite:encountered_date>\n'
                   + '      <cite:encountered_time>' + new_time + '</cite:encountered_time>\n'
                   + '      <cite:photo_s3_url1>' + document.getElementById('photo').value + '</cite:photo_s3_url1>\n'
                   + '      <cite:comments>' + document.getElementById('comments').value + '</cite:comments>\n'
                   + '      <cite:lat>' + document.getElementById('lat').value + '</cite:lat>\n'
                   + '      <cite:long>' + document.getElementById('lng').value + '</cite:long>\n'
                   + '      <cite:username>admin</cite:username>\n'
                   + '      <cite:ts_time>' + ts_time + '</cite:ts_time>\n'
                   + '      <cite:ts_date>' + ts_date + '</cite:ts_date>\n'
                    + '    </wildlife_pt>\n'
                    + '  </wfs:Insert>\n'
                    + '</wfs:Transaction>';

                   // AJAX to post JSON data
                   $.ajax({
                       type: "POST",
                       url: post_wfs,
                       dataType: "xml",
                       contentType: "text/xml",
                       data: postData,
                       //: Error handling
                       success: function(xml) {
                         console.log("success")
                            //TODO: User feedback
                  }
                     });

                /// Wildlife recorded! Thanks for mapping!

               }


          });

      }
    });


});// end Javascript
