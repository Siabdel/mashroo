
function printChart3D(target, jsonData){
    //------------------------------------------------------
    console.log("on est dans printChart ...! ");
    var chart = AmCharts.makeChart(target, {
      "type" : "serial",
      "startDuration": 2,
       "dataProvider":jsonData,

      "graphs": [{
        "balloonText": "[[category]]: <b>[[value]]</b>",
        "colorField": "color",
        "fillAlphas": 0.85,
        "lineAlpha": 0.1,
        "type": "column",
        "topRadius": 1,
        "valueField": "taches"
      }],

      "depth3D": 40,
      "angle": 30,
      "chartCursor": {
        "categoryBalloonEnabled": false,
        "cursorAlpha": 0,
        "zoomable": false
      },

      "graphs": [{
       "balloonText": "[[category]]: <b>[[value]]</b>",
       "colorField": "color",
       "fillAlphas": 0.85,
       "lineAlpha": 0.1,
       "type": "column",
       "topRadius": 1,
       "valueField": "taches"
     }],
     "depth3D": 40,
     "angle": 30,
     "chartCursor": {
       "categoryBalloonEnabled": false,
       "cursorAlpha": 0,
       "zoomable": false
     },
     "categoryField": "status",
     "categoryAxis": {
       "gridPosition": "start",
       "axisAlpha": 0,
       "gridAlpha": 0

     },
     "exportConfig": {
       "menuTop": "20px",
       "menuRight": "20px",
       "menuItems": [{
         "icon": '/lib/3/images/export.png',
         "format": 'png'
       }]
     }
    }, 0);

    jQuery('.chart-input').off().on('input change', function() {
      var property = jQuery(this).data('property');
      var target = chart;
      chart.startDuration = 0;

      if (property == 'topRadius') {
        target = chart.graphs[0];
      }

      target[property] = this.value;
      chart.validateNow();
    });

    return true
}
//
//
function loadDataChart3D(api_url) {
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
