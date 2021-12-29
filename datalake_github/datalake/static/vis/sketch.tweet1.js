var R = 850000;
let noDays = 100;
let margin = 60;
let rot;
var comunas = ['Renca', 'Quilicura', 'Conchalí', 'Huechuraba', 'Vitacura', 'Lo Barnechea',
  'Cerro Navia', 'Quinta Normal', 'Independencia', 'Recoleta', 'Providencia', 'Las Condes',
  'Pudahuel', 'Lo Prado', 'Estación Central', 'Santiago', 'Ñuñoa', 'La Reina',
  'Cerrillos', 'Pedro Aguirre Cerda', 'San Miguel', 'San Joaquín', 'Macul', 'Peñalolén',
  'Maipú', 'Lo Espejo', 'La Cisterna', 'San Ramón', 'La Granja', 'La Florida',
  0, 'San Bernardo', 'El Bosque', 'La Pintana', 'Puente Alto',
]; // space linearization

function preload() {
  data = loadJSON('../../data/PREDIOS_INDEPENDENCIA.geojson');
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
    let price = +geo.features[i].properties["AVALUO_TOT"];
    colorMode(HSL);
    // stroke('white'), strokeWeight(.5), noFill();
    fill((log(price))*20,100,80), noStroke();
    if (geo.features[i].geometry.type === 'MultiPolygon') {
      for (var j = 0; j < geometry.length; j++) {
        push();
        let origin = latLonToCartesian([geometry[j][0][0][1], geometry[j][0][0][0]])
        let rot = constrain(sin(frameCount/10),0,1);//mouseX/width*PI;
        translate(rot*-origin.x,0);
        translate(rot*map(log(price),13,25,-width2/2,width2/2),0)

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
  // data.rows.sort( (a,b) => a.obj['edad'] > b.obj['edad']? 1: 0 );
  console.log(geo);
  // console.log(toDay(data));
  // noLoop();
  width2 = width - margin * 2;
  height2 = height - margin * 2;

  translate(width / 2, height / 2);
  // noLoop();
  let q = {};
  // for (let c in centroids) {
  //   q[centroids[c][1]] = centroids[c][0];
  // }
  // geo.features.forEach( comuna => {
  //   let c = comuna.properties.centroid;
  //   let d = [c[1],c[0]];
  //   q[comuna.properties.NOM_COM] = d;
  // })
  // console.log(q);
  // centroids = q;
  // noLoop();
}

function draw() {
  clear();
  // background('white')
  rot = constrain(sin(frameCount/10),0,1);//mouseX/width*PI;
  rectMode(CENTER);
  noFill();
  stroke(300,10,90),strokeWeight(20);

  translate(width / 2, height / 2);
  rect(0,0,width2,height2);
  // stroke('magenta'), strokeWeight(1);
  // drawMap(geo);
  // stroke('cyan'), strokeWeight(.5);
  // noStroke();
  drawMap(data);
  // fill('white'),textFont('Avenir'), textStyle(BOLD), textAlign(CENTER);
  // text('DÍA '+constrain(frameCount,0,noDays), width/2, 40);

  // let n = 100;
  // let c = 0;
  // let s = width2/10;
  //
  // for (let i =0; i< n; i++) {
  //   for (let j = 0; j < n; j++) {
  //     let index = i*n+j;
  //     if (data.rows.length > index && data.rows[index].obj.day < frameCount && centroids[data.rows[index].obj.comuna]) {
  //       let row = data.rows[index];
  //       let person = row.obj;
  //       fill(255,100), noStroke();
  //       let comuna = person['comuna'];
  //       let center = centroids[comuna];
  //
  //       let pos = latLonToCartesian(center);
  //       let angle = person.angle;
  //       let r = person.r;
  //
  //       //ENCODING
  //       let age = int(person['edad'].split(' ')[0]);
  //       stroke(person['causa_detalle'] === 'COVID-19 Confirmado'? 255: 120), strokeWeight(1);
  //       let c;
  //       person['genero'] === 'Mujer'? c = color(255,255-age*3,255-age*3): c = color(255-age*3,255-age*3,255);
  //       fill(c), stroke(c);
  //       person['causa_detalle'] === 'COVID-19 Sospechoso'? noFill(): null;
  //       let diam = age/24;
  //       let f = angle+frameCount/100//mouseX/50;
  //       ellipse(pos.x+r*sin(f)*cos(f), pos.y+r*sin(f)*sin(f)-40,diam,diam);
  //     }
  //   }
  // }
}

function toDay(data) {
  let day = -1;
  let yesterday = null;
  for (let i = 0; i < data.rows.length; i++) {
    let today = data.rows[i].obj['fecha'];
    if (today !== yesterday) day++;
    data.rows[i].obj['day'] = day;
    data.rows[i].obj['r'] = 5+ random(80);
    data.rows[i].obj['angle'] = random(TWO_PI);
    yesterday = today;
  }
  return day;
}
