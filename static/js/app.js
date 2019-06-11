let generate_click = d3.select("#btn-2");

let counter = 0;
generate_click.on("click", function()
{
    if (counter === 0)
    {
        d3.json("/readability", function(data)
        {
            readability_score = data[0];

            d3.select("#collection")
            .append("div")
            .attr("class", "container")
            .attr("id", "thirdrow")
            .html('<h3>Over 783 records analyzed.</h3>  <div id="two"> <h3 class="display-4">Word Cloud</h3>' +
            '<h7 id="subhead">(Visualization of the most commonly used words.)</h7>' + 
            '<img src="static/images/wordcloud.png"' + 
            'alt="WordCloud">' +
            '<h3 class="display-4" id="readability">Readability:</h3>' +
            `<h4 class="display-4" id="readsub">${readability_score} - Difficult</h4>` +
            '<h7 id="subhead">(Average total score.)</h7></div></div>' + 
            '<!--<div class="col-sm-12" id="row1"><div class="jumbotron mt-3"><h1>Average Score:</h1>' +
            '<div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative" id="subbox-2">' +
            '<h1>92</h1> -->' + '</div></div></div>');
        });

        d3.json("/readability_scores", function(data)
        {
            scores = data.count;
            names = data.word;
            
            // Top 25 graph
            var data = 
            [
                {
                    x: names,
                    y: scores,
                    type: 'bar'
                }
            ];
            var layout = 
            {
                title: "Top 25 Words",
                font: {size: 18}
            };
            Plotly.newPlot('scatter', data, layout);

            // Fixes x-axis margin
            var maxLabelLength = d3.max(data, d => d.x.length);
            const letterWidth = 7;
            var layoutUpdate = {
                "margin.b": maxLabelLength * letterWidth
            };
            Plotly.relayout('scatter', layoutUpdate);
        });
    }
    counter += 1;
});

function init() 
{
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");

    // Use the list of sample names to populate the select options
    d3.json("/data", function(data)
    {
        data.forEach((sample) => {
        selector
        .append("option")
        .text(sample)
        .property("value", sample);
        });
    });
}

function optionChanged(newSample) 
{
    // Fetch new data each time a new sample is selected
    buildCharts(newSample);
}
  
// Initialize the dashboard
init();

let setSearch = true;
function buildCharts(sample)
{
    d3.json(`/terms-and-weights/${sample}`, function(data)
    {
        if (setSearch === false)
        {
            d3.select("#row2").remove();
            d3.select("#row3").remove();
        }
        setSearch = false;

        sample = sample.substring(0, sample.length - 4);

        d3.select("#firstrow")
        .append("div")
        .attr("class", "col-sm-12")
        .attr("id", "row2")
        .html(`<h4 class="display-4">${sample}</h4><h7 id="subhead">(Most used terms from greatest to least.)</h7>`)
        .append("div")
        .attr("class", "col-sm-12")
        .attr("id", "row3")
        .html('<table class="table"><thead><tr><th scope="col">#</th><th scope="col">Term</th><th scope="col">Weight</th>' +
        '</tr></thead><tbody></tbody></table>')

        for (let i = 0; i < data.term.length; i++)
        {
            d3.select("tbody")
            .append("tr")
            .html(`<th scope="row">${i+1}</th><td>${data.term[i]}</td><td>${data.weight[i]}</td>`)
            .enter()
        }

        // Asses Reading Scores and append to html


        // Flesch Reading Ease Score
        if (data.scores[0] < 30)
        {
            var difficulty = 'Very Confusing';
        }
        else if (data.scores[0] >= 30 && data.scores[0] < 50)
        {
            var difficulty = 'Difficult';
        }
        else if (data.scores[0] >= 50 && data.scores[0] < 60)
        {
            var difficulty = 'Fairly Difficult';
        }
        else if (data.scores[0] >= 60 && data.scores[0] < 70)
        {
            var difficulty = 'Standard';
        }
        else if (data.scores[0] >= 70 && data.scores[0] < 80)
        {
            var difficulty = 'Fairly Easy';
        }
        else if (data.scores[0] >= 80 && data.scores[0] < 90)
        {
            var difficulty = 'Easy';
        }
        else if (data.scores[0] >= 90 && data.scores[0] < 100)
        {
            var difficulty = 'Very Easy';
        }

        // Dale-Chall Readability Score
        if (data.scores[1] < 5.0)
        {
            var difficulty_2 = 'Average 4th-grade student or lower';
        }
        else if (data.scores[1] >= 5.0 && data.scores[1] < 6.0)
        {
            var difficulty_2 = 'Average 5th-grade or 6th-grade student';
        }
        else if (data.scores[1] >= 6.0 && data.scores[1] < 7.0)
        {
            var difficulty_2 = 'Average 7th-grade or 8th-grade student';
        }
        else if (data.scores[1] >= 7.0 && data.scores[1] < 8.0)
        {
            var difficulty_2 = 'Average 9th-grade or 10th-grade student';
        }
        else if (data.scores[1] >= 8.0 && data.scores[1] < 9.0)
        {
            var difficulty_2 = 'Average 11th-grade or 12th-grade student';
        }
        else if (data.scores[1] >= 9.0)
        {
            var difficulty_2 = 'average 13th-grade to 15th-grade (college) student';
        }

        d3.select("#firstrow")
        .append("div")
        .attr("class", "col-sm-12")
        .attr("id", "row3")
        .html(`<h4 class="display-4">Readability</h4><ul><li>Flesch Reading Ease Score: ${data.scores[0]} - ${difficulty}</li>` +
        `<li>Dale-Chall Readability Score: ${data.scores[1]} - Understood by ${difficulty_2}</li></ul>`)
    });
}

// Random Select
let random_click =  d3.select("#btn-3");

random_click.on("click", function()
    {
        let names_arr = [];

        d3.json("/data", function(data)
        {
            data.forEach((sample) => {
                names_arr.push(sample);
            });

            let i = Math.floor(Math.random() * 683);

            let newSample = names_arr[i];
            buildCharts(newSample);
        });
    }
);

// Checkbox - working outside
let checkbox_click = d3.select("#same-address");
checkbox_click.on("click", function()
{
    var set = false;
    d3.select("#midrow")
    .append("html")
    .html('<div class="spinner-border" role="status"><span class="sr-only">Loading...</span>');

    var input = 0;
    d3.json(`/analyze/${input}`, function(data)
    {
        d3.select("#midrow")
        .append("div")
        .attr("class", "col-sm-12")
        .html(`<h3>Job Postings:</h3><div class="addList"></div><h7 id="subhead">(Based on your inputs, these are listings that are suited for you.)</h7>`);
        addList(data);
        set =  true;
        if (set != false)
        {
            d3.select(".spinner-border").attr("style", "opacity: 0");   
        }
    });
    console.log(set);
});

function addList(d)
{
    for (let i = 0; i < d.length; i++)
    {
        text = d[i].replace(/[0-9]/g, '');

        d3.select(".addList")
        .append("p")
        .html(`${i+1}. ${text}`);
    }
}

// Change button colors
document.getElementById("btn-3").onmousemove = function(event) {myFunction(event)};
function myFunction(e) 
{
    d3.select(".btn-primary").style("background-color", `#dca42d`);
}
document.getElementById("btn-3").onmouseout = function(event) {myFunction2(event)};
function myFunction2(e) 
{
    d3.select(".btn-primary").style("background-color", `#182875`);
}