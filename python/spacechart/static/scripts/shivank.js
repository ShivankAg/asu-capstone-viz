let global_data;

document.addEventListener('DOMContentLoaded', function () {
    line_svg = d3.select('#shivankLineChart');
    line_width = +line_svg.style('width').replace('px','');
    line_height = +line_svg.style('height').replace('px','');
    margin = { top: 50, bottom: 50, right: 50, left: 50};
    innerWidth = line_width - margin.left - margin.right;
    innerHeight = line_height - margin.top - margin.bottom;
 
    // This will load your two CSV files and store them into two arrays.
    Promise.all([d3.csv('data/ParsedSpaceDucksData.csv')])
         .then(function (values) {
             console.log('loaded data');
             data = values[0];
 
             global_data = data;

            
 
             // Data wrangling
             global_data.map(d => {
                 d.Altitude = +d['Altitude'];
                //  d.Date = parseDate(d['created_at']);
                //  let region = global_region_data.find(obj => obj.name === d.Country)
                //  if (region) //some countries not in region list, we gonna ignore these
                //  {
                //     d.Region = region['World bank region'];
                //  }
                //  d.Birth = +d["Data.Health.Birth Rate"];
                //  d.Death = +d["Data.Health.Death Rate"];
                //  d.Fertility = +d["Data.Health.Fertility Rate"];
                //  d.Life_Expectancy_Female = +d["Data.Health.Life Expectancy at Birth, Female"];
                //  d.Life_Expectancy_Male = +d["Data.Health.Life Expectancy at Birth, Male"];
                //  d.Life_Expectancy_Total = +d["Data.Health.Life Expectancy at Birth, Total"];
                //  d.Population_Growth = +d["Data.Health.Population Growth"];
                //  d.Total_Population = +d["Data.Health.Total Population"];
                //  d.Mobile_Cell = +d["Data.Infrastructure.Mobile Cellular Subscriptions per 100 People"];
                //  d.Telephone_Lines = +d["Data.Infrastructure.Telephone Lines per 100 People"];
                //  d.Agricultural = +d["Data.Rural Development.Agricultural Land"];
             })
            //  //filter out data that doesn't have region (means country has different name than in csv so we can ignore)
            //  global_development_data = global_development_data.filter((obj) => obj.hasOwnProperty('Region'))
            //  console.log(global_development_data)
            //  console.log(global_region_data)

            

            drawLineChart()

         });
 });

 function drawLineChart()
 {
    console.log('creating line chart')
    const parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S.%L");
    global_data.forEach(d => {
        d.created_at = Date.parse(d.created_at);
      });
    console.log(global_data)

    const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.created_at))
    .range([0, innerWidth]);

    const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.Altitude)])
    .range([innerHeight, 0]);

    const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale);

    const g = line_svg.append('g') //shift the data a bit so it doesn't go off the svg
        .attr('transform', 'translate('+margin.left+', '+margin.top+')');;
    g.append('g').call(yAxis)
    g.append('g').call(xAxis)
        .attr('transform',`translate(0,${innerHeight})`);
    const line = d3.line()
        .x(d => xScale(d.created_at))
        .y(d => yScale(d.Altitude));
    
      // Draw line
      g.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 2);


 }