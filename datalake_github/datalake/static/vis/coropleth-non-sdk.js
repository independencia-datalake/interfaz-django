// Visualización de reportería de uso general
// Tabla y filtros: datos crudos, coropleta: agregación por UV
// TODO: Botón de exportar...



var selected = '';
var lockedField = '';
var uv, uvdata, data;
var hovered;
var rows;
let timeRange = [0,365];
let palette = ['#009CDE', '#C20079', '#F9D43F', '#89C60C'];



var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var projection = d3.geoMercator()
    .center([-70.664, -33.415])
    .scale(800000)
    .translate([ width/2, height/2 ])

var geoGenerator = d3.geoPath()
    .pointRadius(5)
    .projection(projection);

d3.queue()
  .defer(d3.json, uv_url)  // World shape
  .defer(d3.csv, form_url)
  //.defer(d3.csv, "../../data/DENUNCIAS SEGURIDAD - coordenadas.csv")
  .defer(d3.csv, streets_url)
  .await(ready);

function ready(error, dataGeo, data, streets) {
  console.log(d3.map());
  console.log(data);
  console.log(streets);
  let centroids = dataGeo.features.map( a => geoGenerator.centroid(a))
  console.log(centroids);

  let addressToUV = mapStreets(streets);

  console.log(data);
  uvdata = data;
  console.log(uvdata);

  var peopleTable = tabulate(uvdata, Object.keys(uvdata[0]));
  document.getElementsByTagName("th")[0].innerText += '▼';
  dates = getDateRange()
  updateSlider();
  filterLoop();

  // Draw the map
  uv = svg.append("g")
      .selectAll("path")
      .data(dataGeo.features)
      .enter()
      .append("path")
      .attr('class', 'UV')
      .attr('id', d => 'UV'+d.properties.Name)
      .attr("fill", d => {

        var valueExtent = d3.extent( uvdata.map( a => +a[selected]));
        var size = d3.scaleLinear()
          .domain([0,valueExtent[1]])
          .range([25,100])
        // let c = d3.hsl(size(uvdata[d.properties.Name-1][selected]),1,.8).rgb() //255-size(uvdata[d.properties.Name-1][selected]);
        let c = hsluv.hsluvToRgb([200,100,80]).map( a => a*255);
        let alpha = selected? size(uvdata[d.properties.Name-1][selected])/100 : .5;
        return 'rgb(0,0,0'+','+alpha+')'//'rgb('+c[0]+','+c[1]+','+c[2]+','+alpha+')'
      } ) // falta append data de consulta
      .attr("d", d3.geoPath()
          .projection(projection)
      )
      .style("stroke", "white")
      .style("stroke-width", "4")
      .style("opacity", 1)

  // Add text on paths
  svg.append("g")
      .selectAll("text")
      .data(dataGeo.features)
      .enter()
      .append("text")
      .html(d => "<b>uv</b> "+d.properties.Name)
      .attr("text-anchor", "start")
      .style("fill", "white")
      .attr("x", d => centroids[d.properties.Name-1][0])
      .attr("y", d => centroids[d.properties.Name-1][1])
      .attr("width", 90)
      .style("font-size", 11)
      .style("font-family", "avenir")


}

function mapData (d) {
  if (!lockedField || d == lockedField) {
    selected = d; // d = field name
    d3.selectAll('th')
      .style("background-color", d=> selected === d? palette[Object.keys(uvdata[1]).indexOf(d)%palette.length]: 'transparent');
      var valueExtent = d3.extent( uvdata.map( a => +a[selected]));
      var size = d3.scaleLinear()
        .domain([0,valueExtent[1]])
        .range([25,100])
      uv
        .transition().duration(200)
        .style('fill', d => {
        // let c = d3.hsl(size(uvdata[d.properties.Name-1][selected]),1,.8).rgb() //255-size(uvdata[d.properties.Name-1][selected]);
        let c = hsluv.hsluvToRgb([200,100,80]).map( a => a*255);
        let alpha = size(uvdata[d.properties.Name-1][selected])/100;
        return 'rgb(0,0,0'+','+alpha+')'
      } )}
}

// --------------- //
// ----TABLE----- //
function tabulate(data, columns) {
    var table = d3.select("body").append("table")
            .attr('id', 'table')
            .attr("style", "font-family: helvetica")
            .style('font-size','14px')
            .style('position','absolute')
            .style('top', '40px')
            .style('left', '600px')
        thead = table.append("thead"),
        tbody = table.append("tbody");
    let sortAscending = false;
    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columns)
        .enter()
        .append("th")
        .attr('class', 'header')
        .attr('id', (d, i) => 'th'+i)
        .text( d => d )
        .style("background-color", d => selected === d? palette[Object.keys(uvdata[1]).indexOf(d)%palette.length]: 'transparent')
        .on("mouseover", function(d){
          d3.select(this)
            .style("background-color", palette[Object.keys(uvdata[1]).indexOf(d)%palette.length]);
        })
        .on("mouseout", function(d){
          d3.select(this)
            .style("background-color", d=> selected === d? palette[Object.keys(uvdata[1]).indexOf(d)%palette.length]: 'transparent');
        })
        .on("click", function (d) {
          let mode = this.innerText.substring(this.innerText.length-1);
          if (mode == '▲') {
            mode = '';
            Array.prototype.slice.call($('th')).forEach((item, i) => {
              item.innerText = item.innerText.replace( '▲', '');
              item.innerText = item.innerText.replace( '▼', '');
            });
          } else if (mode == '▼') {
            mode = '▲';
            Array.prototype.slice.call($('th')).forEach((item, i) => {
              item.innerText = item.innerText.replace( '▲', '');
              item.innerText = item.innerText.replace( '▼', '');
            });
            this.innerText += mode;
          } else {
            mode = '▼';
            Array.prototype.slice.call($('th')).forEach((item, i) => {
              item.innerText = item.innerText.replace( '▲', '');
              item.innerText = item.innerText.replace( '▼', '');
            });
            this.innerText += mode;
          }
          if (mode == '▼') {
            rows.sort(function(a, b) {return d3.descending(b[d], a[d]);  });
            sortAscending = false;
            this.className = 'aes';
          }
          else if (mode == '▲') {
            rows.sort(function(a, b) { return d3.ascending(b[d], a[d]); });
            sortAscending = true;
            this.className = 'des';
          }
        } );
        // .on("click", mapData);

    rows = tbody.selectAll("tr")
        .data(data)
        .enter()
        .append("tr")
        // .attr('id', d => 'row'+d.UV)
        .attr('class', 'uv')
        .style('background-color', (d, i) => i%2? 'GhostWhite':'white')

    // create a cell in each row for each column
    var cells = rows.selectAll("td")
        .data(function(row) {
            return columns.map(function(column) {
                return {column: column, value: row[column], uv: row['UV']};
            });
        })
        .enter()
        .append("td")
        .attr('class', 'uv')
        .attr('id', (d, i) => 'uv'+'c'+i+'r'+d.uv)
        .style('text-align','right')
        .style('padding-left', '15px')
        .style('font-weight', d => d.column === 'UV'? 'bold': 'normal')
        .html(function(d) { return d.value; })

    return table;
}

function sortTableBy() {
  var table, i, x, y;
  table = document.getElementById("table");


  columnNumber = this.id.substring(2);
  var switching = true;

  while (switching) {
    switching = false;
    var rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
        var mustSwitch = false;
        x = rows[i].getElementsByTagName("td")[columnNumber];
        y = rows[i + 1].getElementsByTagName("td")[columnNumber];
        if (mode == '▼'? x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()
            : mode == '▲'? x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()
            : false) {
          mustSwitch = true;
          break;
        }
    }
    if (mustSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}
// ---------------- //
// ----FILTERS----- //
function filterLoop() { //Runs and adds up all filters
  // Declare variables
  var inputs, filters, table, rows;
  inputs = Array.prototype.slice.call($('.Input'));
  rows = $("tr");
  // Loop through rows, and hide those who don't match the search query
  for (let i = 0; i < rows.length; i++) {
    let hide = false;

    // Filtro temporal
    let td = rows[i].getElementsByTagName("td")[0];
    if (td) {
      let txtValue = td.textContent || td.innerText;
      let date = txtValue.split(' ')[0].split('/');
      let t = dateToDays(date[2],date[0],date[1]);

      if (t < timeRange[0] || t > timeRange[1]) hide = true;
    }

    inputs.forEach((input, n) => { // Loop through columns with filters
      let field = document.getElementById('select'+n).value;
      let filter = input.value.toUpperCase();
      let td = rows[i].getElementsByTagName("td")[field];
      if (td) {
        let txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) === -1) hide = true;
      }
    });
    if (hide) rows[i].style.display = "none";
    else rows[i].style.display = "";
  }
}

function addFilterInput() {
  let dropdown = document.createElement('select');
  let n = document.getElementsByTagName('select').length;
  dropdown.setAttribute('id','select'+n);
  dropdown.setAttribute('class','Select');
  Array.prototype.slice.call( document.getElementsByTagName('th') ).forEach((th, i) => {
    let option = document.createElement('option');
    option.setAttribute('value',i);
    option.innerText = th.innerText;
    dropdown.appendChild(option);
  });

  let input = document.createElement('input');
  input.setAttribute('id','input'+n)
       .setAttribute('class','Input')
       .setAttribute('onkeyup',"filterLoop()")
       .setAttribute('type','text')
       .setAttribute('placeholder',"Filtrar por...");
  let div = document.getElementById('filters');
  div.appendChild(dropdown)
     .appendChild(input)
     .appendChild(document.createElement('br'));
}

// ----TIME FILTERS----- //
$( function() {
  $( "#slider-range" ).slider({
    range: true,
    min: 0,
    max: 365,
    values: [ 0, 365 ],
    slide: function( event, ui ) {
      timeRange = [ui.values[ 0 ], ui.values[ 1 ]];
      $( "#time-range" ).val( daysToDate1()[0] + " - " + daysToDate1()[1] );
      filterLoop();
    }
  });
  $( "#time-range" ).val(  daysToDate1()[0] + " - " + daysToDate1()[1] );
} ); // Time slider anonymous jQuery function

function updateSlider() {
  let startDay = dateToDays(dates[0][0],dates[0][1],dates[0][2]);
  let endDay = dateToDays(dates[1][0],dates[1][1],dates[1][2]);
  let range = endDay-startDay;
  $("#slider-range").slider('option','values',[startDay,endDay]);
  $("#slider-range").slider('option','min',startDay);
  $("#slider-range").slider('option','max',endDay);
  console.log($("#slider-range").slider('option','min'), $("#slider-range").slider('option','max'), $("#slider-range").slider('option','values'));
}

function dateToDays(year,month,day) {
  const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
  const firstDate = new Date(2020, 0, 0);
  // let firstDate = new Date(dates[0][0],dates[0][1],dates[0][2]);
  const secondDate = new Date(year, month-1, day); // month 0-index correction
  const diffDays = Math.round((secondDate - firstDate) / oneDay);
  return diffDays;
}

function getDateRange() {
  let rows = $("tr");
  let r = [1,rows.length-1];
  let dates = r.map(a => {
    let td = rows[a].getElementsByTagName("td")[0];
    let txtValue = td.textContent || td.innerText;
    let date = txtValue.split(' ')[0].split('/');
    return [1*date[2], 1*date[0], 1*date[1]];
  } )
  return dates;
}

function daysToDate1() {
  let rows = $("tr"), td, i = 0, target = '';
  let dates = [];
  for (i = 0; i < rows.length; i++) {
    td = rows[i].getElementsByTagName("td")[0];
    if (td && rows[i].style.display === target) {
      let txtValue = td.textContent || td.innerText;
      let date = txtValue.split(' ')[0].split('/');
      dates.push( new Date(1*date[2], 1*date[0], 1*date[1]));
      target === ''? target = 'none' : target = 'stop';
      if (target === 'stop') break;
    }
  }
  return dates;
}

//----EXPORT----//
// Quick and simple export target #table_id into a csv
function downloadTableAsCsv(table_id, separator = ',') {
    // Select rows from table_id
    var rows = document.querySelectorAll('#' + table_id + ' tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
            data = data.replace(/"/g, '""');
            // Push escaped string
            row.push('"' + data + '"');
        }
        csv.push(row.join(separator));
    }
    var csv_string = csv.join('\n');
    // Download it
    var filename = 'export_' + table_id + '_' + new Date().toLocaleDateString() + '.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename); // !!download attribute not working for Safari
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
