function drawMapOnLayer(cnv, geo) {
    for (var i in geo.features) {
      var zone = geo.features[i];
      var id = geo.features[i].id;
      geometry = geo.features[i].geometry.coordinates;
      if (geo.features[i].geometry.type === 'MultiPolygon') {
        for (var j = 0; j < geometry.length; j++) {
          cnv.beginShape();
          for (var q in geometry[j][0]) {
            var pos = latLonToCartesian([geometry[j][0][q][1], geometry[j][0][q][0]]);
            cnv.vertex(pos.x, pos.y);
          }
          cnv.endShape(CLOSE);
        }
      } else {
        geo.features[i].cartesian = [];
        cnv.beginShape();
        for (var q in geometry[0]) {
          var pos = latLonToCartesian([geometry[0][q][1], geometry[0][q][0]]);
          geo.features[i].cartesian.push([pos.x,pos.y]);
          cnv.vertex(pos.x, pos.y);
  
        }
        cnv.endShape(CLOSE);
      }
    }
  }
  
  function drawMap(geo, d) {
    for (var i in geo.features) {
      var zone = geo.features[i];
      var uv = 1*geo.features[i].properties.Name;
      geometry = geo.features[i].geometry.coordinates;
      if (d) d[uv]? fill(lerpColor(colorscale[0], colorscale[1], d[uv]/range[1])): fill(255);
      if (geo.features[i].geometry.type === 'MultiPolygon') {
        for (var j = 0; j < geometry.length; j++) {
          beginShape();
          for (var q in geometry[j][0]) {
            var pos = latLonToCartesian([geometry[j][0][q][1], geometry[j][0][q][0]]);
            vertex(pos.x, pos.y);
          }
          endShape(CLOSE);
        }
      } else {
        geo.features[i].cartesian = [];
        beginShape();
        for (var q in geometry[0]) {
          var pos = latLonToCartesian([geometry[0][q][1], geometry[0][q][0]]);
          geo.features[i].cartesian.push([pos.x,pos.y]);
          vertex(pos.x, pos.y);
        }
        endShape(CLOSE);
      }
    }
  }

  function inside(point, vs) {
    // ray-casting algorithm based on
    // https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html/pnpoly.html
    
    var x = point[0], y = point[1];
    var inside = false;
    for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        var xi = vs[i][0], yi = vs[i][1];
        var xj = vs[j][0], yj = vs[j][1];
        
        var intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    return inside;
  };
  
  function getRange( d, field ) {
    return d.map( a => a[field]).reduce( (acc,a) => [min(acc[0],a),max(acc[1],a)], [Infinity,-Infinity]);
  }
  
  function angleBetween(a, b) { // a, b points on cartesian plane; E = 3PI/4, N = 2PI
    var angle = atan2(b.x - a.x, b.y - a.y);
    return angle;
  }
  
  function latLonToCartesian(latLng) {
    let origin = [-70.6655, -33.4154];
    let lat = latLng[0] - origin[1], //33.66
      lon = latLng[1] - origin[0]; //70.54
    return {
      'x': R * cos(radians(lat)) * sin(radians(lon)) * .85,
      'y': -R * sin(radians(lat)),
      'z': R * cos(radians(lat)) * cos(radians(lon)) - (R - 300)
    };
  }