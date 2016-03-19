# EON Maps

Real-time location tracking powered by [PubNub](http://pubnub.com) and [MapBox](http://mapbox.com).

![](http://i.imgur.com/25Zg5YB.gif)

# Examples

* [One Marker](http://pubnub.com/developers/eon/map/index/)
* [Multiple Markers + Follow Marker](http://pubnub.com/developers/eon/map/extra/)
* [Custom Marker Image + Rotation](http://pubnub.com/developers/eon/map/flight/)
* [Bus Tracking](http://pubnub.com/developers/eon/map/bus/)

## Quickstart

```html
<script type="text/javascript" src="http://pubnub.github.io/eon/lib/eon-map.js"></script>
<link type="text/css" rel="stylesheet" href="http://pubnub.github.io/eon/lib/eon.css" />
<div id='map'></div>
<script type="text/javascript">
eon.map({
  id: 'map',
  mb_token: 'mapbox api token',
  mb_id: 'mapbox map id',
  subscribe_key: 'demo',
  channel: 'my map channel'
});
</script>
```

### Init

Parameter | Value | Default
| :------------ |:---------------| -----:|
| id | The ID of the element where the map will be rendered. | ```undefined```
| mb_token | Mapbox API Token. | ```undefined```
| mb_id | Mapbox Map ID. | ```undefined```
| transform | Method for changing the payload format of your stream. See [example](https://github.com/pubnub/eon-map/blob/master/examples/transform.html) | ```function(m){}```
| history | Use PubNub history call to retrieve last message. This will display points at their last known location. Requires [PubNub storage](http://www.pubnub.com/how-it-works/storage-and-playback/) to be enabled. | ```false```
| pubnub | An instance of the PUBNUB javascript global. This is required when using your own keys. See the ```subscribe_key``` example. | ```false```
| connect | A function to call when PubNub makes a connection. See [PubNub subscribe](http://www.pubnub.com/docs/javascript/api/reference.html#subscribe) | ```function(){}``` |
| marker | A custom Mapbox marker object. Use this to change the marker icon, tooltip, etc. | L.marker |
| rotate | Add bearing to markers in ```options.angle```. This won't have any effect unless you're using [a rotated marker type](https://www.mapbox.com/mapbox.js/example/v1.0.0/rotating-controlling-marker/). | ```false``` |

## Simple Example

Call ```eon.map({})```. Check out the table of options above for more information.

```js
var channel = 'pubnub-mapbox';

eon.map({
  id: 'map',
  mb_token: 'pk.eyJ1IjoiaWFuamVubmluZ3MiLCJhIjoiZExwb0p5WSJ9.XLi48h-NOyJOCJuu1-h-Jg',
  mb_id: 'ianjennings.l896mh2e',
  channel: channel,
  connect: connect
});
```

![](http://i.imgur.com/QtJ7E3d.gif)

## Lat/Long Values

```eon.map``` expects an array of objects to be published on the same channel it's subscribed to. More on publishing in the next section.

For example, below you can find a list of all the Torchy's Tacos in Austin, TX.

```js
var torchys = [
  { latlng: [30.370375, -97.756138] },
  { latlng: [30.323118, -97.739144] },
  { latlng: [30.302816, -97.699490] },
  { latlng: [30.293479, -97.742405] },
  { latlng: [30.250337, -97.754593] },
  { latlng: [30.236689, -97.762730] }
];
```

## Publishing Messages

The function below is called ```connect``` and fires when the ```pubnub_mapbox``` library is ready.

This function uses the included PubNub library to pubnub.publish() 
packets to the pubnub.subscribe() call waiting inside the 
Mapbox framework. 

Notice how the ```subscribe_key``` and ```channel```  matches.

```js

function connect() {

var point = {
  latlng: [37.370375, -97.756138]
};

var pn = PUBNUB.init({
  publish_key: 'demo'
});

setInterval(function(){

  var new_point = JSON.parse(JSON.stringify(point));

  new_point.latlng = [
    new_point.latlng[0] + (getNonZeroRandomNumber() * 0.1),
    new_point.latlng[1] + (getNonZeroRandomNumber() * 0.2)
  ];

  pn.publish({
    channel: channel,
    message: [new_point] // even a single point should be an array
  });

}, 500);

};
```

You probably want to publish data from the back-end instead. 
Check out our docs for more info:

http://www.pubnub.com/documentation/

## Following a Point

You can tell the map to follow a point to it's new location whenever data is received by supplying a ```message``` callback.

```js
var map = eon.map({
  id: 'map',
  mb_id: 'ianjennings.l896mh2e',
  //...
  message: function (data) {
    map.setView(data[3].latlng, 13);
  }
});
```

## Marker Customization

You can supply a custom Mapbox marker object with custom tooltips by extening the ```L.marker``` object provided by mapbox. Learn more about custom markers [here](https://www.mapbox.com/mapbox.js/example/v1.0.0/custom-marker/).

```html
<div id='map'></div>
<script>
  L.RotatedMarker = L.Marker.extend({
    options: { angle: 0 },
    _setPos: function(pos) {
      L.Marker.prototype._setPos.call(this, pos);
      if (L.DomUtil.TRANSFORM) {
        // use the CSS transform rule if available
        this._icon.style[L.DomUtil.TRANSFORM] += ' rotate(' + this.options.angle + 'deg)';
      } else if (L.Browser.ie) {
        // fallback for IE6, IE7, IE8
        var rad = this.options.angle * L.LatLng.DEG_TO_RAD,
        costheta = Math.cos(rad),
        sintheta = Math.sin(rad);
        this._icon.style.filter += ' progid:DXImageTransform.Microsoft.Matrix(sizingMethod=\'auto expand\', M11=' +
          costheta + ', M12=' + (-sintheta) + ', M21=' + sintheta + ', M22=' + costheta + ')';
      }
    }
  });

  var map = eon.map({
    id: 'map',
    mb_id: 'ianjennings.lec77m70',
    mb_token: 'pk.eyJ1IjoiaWFuamVubmluZ3MiLCJhIjoiZExwb0p5WSJ9.XLi48h-NOyJOCJuu1-h-Jg',
    channel: 'rutgers-bus-data',
    rotate: true,
    history: true,
    marker: function (latlng, data) {

      var marker = new L.RotatedMarker(latlng, {
        icon: L.icon({
          iconUrl: 'http://i.imgur.com/2fmFQfN.png',
          iconSize: [9, 32]
        })
      });

      marker.bindPopup('Route ' + data.routeTag.toUpperCase());

      return marker;

    }
  });
</script>
```

## Configure using your own PubNub API Keys
#### Using your own API Key with Eon Maps

You can set the `pubnub` init parameter when using Eon Maps.  This allows you to configure PubNub client connections with extra security options such a `auth_key` and your `cipher_key`.  You should also set `secure: true` and `ssl: true` as well.

```html
<div id="map"></div>
<script>
  var pubnub  = PUBNUB({ subscribe_key : 'YOUR_SUBKEY_HERE', ssl : true });
  var channel = 'my-map';
  eon.map({
    pubnub   : pubnub,  // < - - - here < - - - //
    channel  : channel,
    id       : 'map',
    mb_id    : 'mapbox.streets',
    mb_token : 'pk.ey31IjoiaWRtc3giLCJhIjoiZZ1zMGI2ZjBlNTMxZjk5YTEwNjM5WNJlOWI4MmJiZGIifQ.U1jMQo2QVeuUtt85oD7hkQ'
  });
</script>
```


## Kitchen Sink

Check out the ```bus.html``` and ```flight.html``` for full featured examples.

## Customizing with Mapbox

The MapBox map object is returned by ```eon.mapbox``` and can be customized using the [Mapbox API](https://www.mapbox.com/mapbox.js/api/v3.1.5/). Also see the [Mapbox examples page](https://www.mapbox.com/mapbox.js/example/v1.0.0/).

Also note that you can customize your map using Mapbox map editor. You can change the map background style, add static markers, etc. Visit [Mapbox](https://www.mapbox.com/) for your own API key.

## Distributed Systems

The EON library compiles all messages at designated intervals. This means you can publish from multiple sources into one map. For example, you can map the individual locations of 3 phones by supplying the same channel to your PubNub publish requests. The [flight example](http://pubnub.com/developers/eon/map/flight/) works like this; not every flight is updated on every subscribe call.
