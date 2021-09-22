// TODO
// tooltip
// table name as variable in html 

var R = 850000;
let noDays = 100;
let margin = 60;
let rot;
let predios, unidades, data;
let range, timerange;
let colorbins = 4;
let colorscale;
let timeslider;
let phase;
let layer;
let canvas;
let timehist;

function preload() {
  data = loadTable(data_var,'header').rows;
  predios = loadJSON(predios_var);
  unidades = loadJSON(unidades_var);
  monotype = loadFont(monotype_var);
}

function setup () {
  canvas = createCanvas(600,windowHeight);
  frameRate(24);
  
  width2 = width - margin * 2;
  height2 = height - margin * 2;
  colorscale = [color(255),color(0,0,255)];
  
  // PREDIOS LAYER
  layer = createGraphics(width*2,height*2);
  layer.push(), layer.translate(width / 2, height / 2);
  layer.stroke(255), layer.noFill(),layer.strokeWeight(.2);
  drawMapOnLayer(layer, predios); 

  // PREPROCESSING 
// Modificaciones necesarias

  data = data.map( a => a.obj);
  data.forEach( a => a['uv'] = floor(random()*26)+1); // simulate uv ; borrar esta linea. 
  summarize(data);
  
  data.forEach( a => a['created'] = new Date(a['created'])); // ccambiar marca temporal por created
  created = data.map( a => a.created);
  timerange = [Math.min(...created), Math.max(...created)];
  phase = data;

  timehist = new Array(100).fill(0);
  created.forEach ( a => timehist[floor((a-timerange[0])/(timerange[1]-timerange[0])*(timehist.length-1))]++);

  // TIMESLIDER
  timeslider = {
    x1: 0,
    x2: 400,
    t: timerange,
    margin: 100,
    draw: function() {
      push(), translate(this.margin, height-50);
      stroke(100), strokeWeight(2);
      line(0,0,width-this.margin*2,0);
      // this.x1 = map(this.range[0],timerange[0],timerange[1],0,width-this.margin*2);
      this.x1 = constrain(this.x1,0,this.x2-20);
      this.x2 = constrain(this.x2,this.x1,width-this.margin*2);
      this.t = [this.x1,this.x2].map( a => map(a,0,width-margin*2,timerange[0],timerange[1]) );
      // this.x2 = map(this.range[1],timerange[0],timerange[1],0,width-this.margin*2);
      stroke('orange');
      line(this.x1,0,this.x2,0);
      noStroke(), fill('orange'), textSize(10), textAlign(CENTER);
      ellipse(this.x1,0,20);
      text(formatDate(new Date(this.t[0])),this.x1,-20);
      // text((new Date(this.t[0])).getHours()+':'+(new Date(this.t[0])).getMinutes(),this.x1,-20);
      ellipse(this.x2,0,20);
      text(formatDate(new Date(this.t[1])),this.x2,26);
      // text((new Date(this.t[1])).getHours()+':'+(new Date(this.t[1])).getMinutes(),this.x2,50);

      fill(100);
      text(formatDate(new Date(timerange[0])),-this.margin/2,4);
      text(formatDate(new Date(timerange[1])),width-this.margin*1.5,4);
      // text((new Date(timerange[1])).getHours()+':'+(new Date(timerange[1])).getMinutes(),width-this.margin*2,30);
      pop();
    },
    chronophase: function(d) {
      return d.filter( a => a.created >= this.t[0] && a.created <= this.t[1]);
    } 
  }
}

function draw() {
  clear();

  timehist.forEach( (a, i) => {
    let x = 100+(width-200)/timehist.length*i;
    stroke(timeslider.x1+100 <= x && x <= timeslider.x2+100? color('orange') : 100), strokeWeight(1);
    line(x,height-50,x, height-50-(a/Math.max(...timehist)*40) )
  });

  // TIME SLIDER
  timeslider.draw();
  phase = timeslider.chronophase(data);
  summarize(phase);

  textFont(monotype);
  //LEGEND
  push(), translate(100,50);
  let r = (width-100*2)/(colorbins+1);
  for(let i = 0; i <= colorbins; i++) {
    stroke(230,140,30), strokeWeight(.5), textSize(10), fill(lerpColor(colorscale[0],colorscale[1],i/colorbins));
    rect(r*i,0,r,10);
    fill(100), noStroke(), textAlign(CENTER);
    text (floor(range[1]*i/colorbins),r*(colorbins+1)*i/(colorbins+1),30);
  }
  // text (range[1],r*(colorbins+1),30);
  
  pop();

  // MAP

  push(), translate(width / 2, height / 2);
  stroke(220), noFill(),strokeWeight(2);
  drawMap(unidades, hist);
  // stroke(255,50), noFill(),strokeWeight(.5); //stroke(80,140,230)
  // drawMap(predios);
  
  
  pop();
  image(layer,0,0,width*2,height*2);


  // TOOLTIP
  push(), translate(width / 2, height / 2);
  unidades.features.forEach( (b,i) => {
    let mousexy = [mouseX-width/2,mouseY-height/2];
    if (inside(mousexy,b.cartesian)) {
      fill(255,200),noStroke();
      rect (mousexy[0],mousexy[1],60,-40);
      noStroke(), fill(100), textSize(14);
      text('UV '+b.properties.Name,mousexy[0]+5,mousexy[1]-25);
      text((hist[b.properties.Name]?hist[b.properties.Name]:0),mousexy[0]+5,mousexy[1]-5);//+ ' Registros entre '+formatDate(new Date(timerange[0])) + ' y '+formatDate(new Date(timerange[1])),mousexy[0],mousexy[1]);
    }
  });
  pop();
  
}

// -----------------

function formatDate(date) {
  return date.getDate()+'-'+(1+date.getMonth())+'-'+date.getFullYear();
}

function summarize(d) {
  let uv = d.map(a => a.uv);
  hist = uv.reduce( (dict, a) => {
    dict[a]? dict[a]+=1: dict[a] = 1;
    return dict; 
  } , {});
  range = [0, Math.max(...Object.keys(hist).map( a => hist[a]))];
}

function mouseDragged() {
  if (dist(mouseX,mouseY,timeslider.x1+timeslider.margin,height-50)<10) timeslider.x1 = mouseX-timeslider.margin;
  else if (dist(mouseX,mouseY,timeslider.x2+timeslider.margin,height-50)<10) timeslider.x2 = mouseX-timeslider.margin;
  else if (timeslider.x1+timeslider.margin < mouseX && mouseX < timeslider.x2+timeslider.margin && mouseY > height-60) {
    let d = mouseX-dragStart[1];
    timeslider.x1 = dragStart[0]+d;
    timeslider.x2 = dragStart[2]+d;
  }
}

function mousePressed() {
  dragStart = [timeslider.x1, mouseX, timeslider.x2];
}

function mouseClicked() {
  unidades.features.forEach( (b,i) => {
    let mousexy = [mouseX-width/2,mouseY-height/2];
    if (inside(mousexy,b.cartesian)) {
      console.log(b.properties.Name + ' clicked');
      console.log(phase.filter(a => +b.properties.Name === a.uv));
    }
  })
}
