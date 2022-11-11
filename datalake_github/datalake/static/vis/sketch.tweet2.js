var R = 850000;
let noDays = 100;
let margin = 60;
let rot;

function preload() {
  data = loadJSON('../../data/GIS.DBO.TG_ZonasPRC.geojson');
  geo = loadJSON('../../data/Unidades_Vecinales.geojson');
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

function drawMap(geo) {
  for (var i in geo.features) {
    var zone = geo.features[i];
    var id = geo.features[i].id;
    geometry = geo.features[i].geometry.coordinates;
    // let price = +geo.features[i].properties["AVALUO_TOT"];
    colorMode(HSL);
    // stroke('white'), strokeWeight(.5), noFill();
    fill(i*20,100,80), noStroke();
    // text(geo.features[i].properties.Name,-width/2+10,-height/2+i*20);
    if (geo.features[i].geometry.type === 'MultiPolygon') {
      for (var j = 0; j < geometry.length; j++) {
        push();
        let origin = latLonToCartesian([geometry[j][0][0][1], geometry[j][0][0][0]])
        let rot = constrain(sin(frameCount/20+i/10),0,1);//mouseX/width*PI;
        translate(rot*-100*cos(i),rot*100*sin(i));
        // translate(0,abs((mouseY-height/2)/height*20-i)<5? 20: 0);
        // translate(rot*-origin.x*cos(j),rot*-origin.x*sin(j));
        // translate(rot*map(log(price),13,25,-width2/2,width2/2),0)

        beginShape();
        for (var q in geometry[j][0]) {
          var pos = latLonToCartesian([geometry[j][0][q][1], geometry[j][0][q][0]]);
          vertex(pos.x, pos.y);
        }
        endShape(CLOSE);
        pop();
      }
    } else {
      beginShape();
      for (var q in geometry[0]) {
        var pos = latLonToCartesian([geometry[0][q][1], geometry[0][q][0]]);
        vertex(pos.x, pos.y);
      }
      endShape(CLOSE);
    }
  }
}

function setup () {
  createCanvas(windowWidth,windowHeight);
  // frameRate(8);
  console.log(data);
  width2 = width - margin * 2;
  height2 = height - margin * 2;

  translate(width / 2, height / 2);
  // noLoop();
  let q = {};
}

function draw() {
  clear();
  // background('white')
  rot = sin(frameCount/10);//mouseX/width*PI;
  translate(width / 2, height / 2);
  drawMap(data);
}
