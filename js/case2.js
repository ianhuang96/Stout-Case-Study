google.load('visualization', '1', {packages: ['controls']});
google.setOnLoadCallback(drawChart);

function drawChart () {
    
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Year');
    data.addColumn('number', 'Total revenue for the current year');
    data.addColumn('number', 'New Customer Revenue');
    data.addColumn('number', 'Existing customer growth');
    data.addColumn('number', 'Revenue lost from attrition');
    data.addColumn('number', 'Existing Customer Revenue Current Year');
    data.addColumn('number', 'Existing Customer Revenue Prior Year');
    data.addColumn('number', 'Total Customers Current Year');
    data.addColumn('number', 'Total Customers Previous Year');
    data.addColumn('number', 'New Customers');
    data.addColumn('number', 'Lost Customers');

          
    data.addRows([
        ["2015", 29036749.19, null, null, null, null, null, 231294, null, null, null],
        ["2016", 25730943.59, 18245491.01, 20335.46, 21571632.07, 7485452.58, 7465117.12, 204646, 231294, 145062, 171710],
        ["2017", 31417495.03, 28776235.04, 20611.34, 23110294.94, 2641259.99, 2620648.65, 249987, 204646, 229028, 183687]
    ]);


    var columnsTable = new google.visualization.DataTable();
    columnsTable.addColumn('number', 'colIndex');
    columnsTable.addColumn('string', 'colLabel');
    var initState= {selectedValues: []};
    // put the columns into this data table (skip column 0)
    for (var i = 1; i < data.getNumberOfColumns(); i++) {
        columnsTable.addRow([i, data.getColumnLabel(i)]);
        // you can comment out this next line if you want to have a default selection other than the whole list
        initState.selectedValues.push(data.getColumnLabel(i));
    }
    // you can set individual columns to be the default columns (instead of populating via the loop above) like this:
    // initState.selectedValues.push(data.getColumnLabel(4));
    
    var chart = new google.visualization.ChartWrapper({
        chartType: 'LineChart',
        containerId: 'chart_div',
        dataTable: data,
        options: {
            title: '',
            width: 650,
            height: 420
        }
    });
    
    var columnFilter = new google.visualization.ControlWrapper({
        controlType: 'CategoryFilter',
        containerId: 'colFilter_div',
        dataTable: columnsTable,
        options: {
            filterColumnLabel: 'colLabel',
            ui: {
                label: 'Attribute',
                allowTyping: true,
                allowMultiple: false,
                allowNone: false,
                selectedValuesLayout: 'below'
            }
        },
        'state': {'selectedValues': ['Total revenue for the current year']}
    });
    
    function setChartView () {
        var state = columnFilter.getState();
        var row;
        var view = {
            columns: [0]
        };
        for (var i = 0; i < state.selectedValues.length; i++) {
            row = columnsTable.getFilteredRows([{column: 1, value: state.selectedValues[i]}])[0];
            view.columns.push(columnsTable.getValue(row, 0));
        }
        // sort the indices into their original order
        view.columns.sort(function (a, b) {
            return (a - b);
        });
        chart.setView(view);
        chart.draw();
    }
    google.visualization.events.addListener(columnFilter, 'statechange', setChartView);
    
    setChartView();
    columnFilter.draw();
}

