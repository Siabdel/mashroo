var chart;
var legend;


function printPieChart3D(target, jsonData){
    //------------------------------------------------------
      console.log("on est dans Camanbert printPieChart3 ...! " + target);
    var chart = AmCharts.ready(function() {
    // PIE CHART
    chart = new AmCharts.AmPieChart();
    chart.dataProvider = jsonData;
    chart.titleField = "status";
    chart.valueField = "taches";
    chart.outlineColor = "";
    chart.outlineAlpha = 0.8;
    chart.outlineThickness = 2;
    // this makes the chart 3D
    chart.depth3D = 20;
    chart.angle = 30;

    // WRITE
    chart.write(target);
});
}

//
//
function loadDataPieChart3D(api_url) {
  ///var url = `/pro/api/tickets/${this.project_id}.json/`
  //var jsonData3 = '{"data": [{"status": "nouveau", "color": "#FF0F00", "taches": 2}, {"status": "nouveau", "color": "#FF0F00", "taches": 2}]}';
  // go ...
  // this.project_id = `${project_id}`
  var response = [];
  $.ajax({
    url: api_url,
    type :'GET',
    dataType : 'json',
    async: false,
    success : function(data, status){
      //this.jsonData  = JSON.stringify(data)
      ApijsonData  =  data ;
      response  =  data ;
      //console.log("load data ..." +  ApijsonData );
    },
    error: function(resultat, status, erreur){
      console.log("Erreur !!" + jsonData );
    }
    });
    return response;
  }
