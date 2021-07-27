 google.charts.load('current', {'packages':['corechart']});

 google.charts.setOnLoadCallback(pie1);
 google.charts.setOnLoadCallback(pie2);
 google.charts.setOnLoadCallback(bar1);
 google.charts.setOnLoadCallback(bar2);

 function pie1() {

   var data = new google.visualization.DataTable();
   data.addColumn('string', 'Type');
   data.addColumn('number', 'Amount');
   data.addRows([
     ['Cash In', 1399284],
     ['Cash Out', 2237500],
     ['Debit', 41432],
     ['Payment', 2151495],
     ['Transfer', 532909]
   ]);

   var options = {title:'Amount of Each Type',
                  is3D: true,
                  width:450,
                  height:300};

   var chart = new google.visualization.PieChart(document.getElementById('pie1_chart_div'));
   chart.draw(data, options);
 }
 function pie2() {

    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Topping');
    data.addColumn('number', 'Transaction Amount');
    data.addRows([
      ['Cash In', 236367391912.46],
     ['Cash Out', 394412995224.49],
     ['Debit', 227199221.28],
     ['Payment', 28093371138.37],
     ['Transfer', 485291987263.16]
    ]);

    var options = {title:'Transaction Amount of Each Type',
                   is3D: true,
                   width:450,
                   height:300};
 
    var chart = new google.visualization.PieChart(document.getElementById('pie2_chart_div'));
    chart.draw(data, options);
  }

  function bar1() {
    var data = google.visualization.arrayToDataTable([
      ["", "Count", { role: "style" } ],
      ["Fraud", 8213, "skyblue"],
      ["Not Fraud", 6354407, "skyblue"]
    ]);

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
                     { calc: "stringify",
                       sourceColumn: 1,
                       type: "string",
                       role: "annotation" },
                     2]);

    var options = {
      title: "Ratio of Fraud to Not Fraud",
      width: 450,
      height: 300,
      bar: {groupWidth: "60%"},
      legend: { position: "none" },
    };
    var chart = new google.visualization.BarChart(document.getElementById("bar1_chart_div"));
    chart.draw(view, options);
  }

  function bar2() {
    var data = google.visualization.arrayToDataTable([
      ["", "Amount", { role: "style" } ],
      ["Fraud", 12056415427.84, "skyblue"],
      ["Not Fraud", 11132336529331.93, "skyblue"]
    ]);

    var view = new google.visualization.DataView(data);
    view.setColumns([0, 1,
                     { calc: "stringify",
                       sourceColumn: 1,
                       type: "string",
                       role: "annotation" },
                     2]);

    var options = {
      title: "Ratio of Fraud Amount to Not Fraud Amount",
      width: 450,
      height: 300,
      bar: {groupWidth: "60%"},
      legend: { position: "none" },
    };
    var chart = new google.visualization.BarChart(document.getElementById("bar2_chart_div"));
    chart.draw(view, options);
  }