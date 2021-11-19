function printChart(target, jsonData){
    //------------------------------------------------------
    var ctx = document.getElementById(target).getContext('2d');

    /// format data
    for(i=0; i < 6; i++){
      if (jsonData[i] == undefined){
        jsonData[i] = 0;
        // console.log("api ok " +  i + " == " + data_in[i] );
      }
    }
    // init myChart
    var myChart = new Chart(ctx,
       {
        type: 'bar',
        data: {
          labels: ['todo', 'pause', 'doing', 'done', 'closed', 'canceled'],
          //labels: [  'NOUVEAU' , 'ENATTENTE', 'ENCOURS', 'RESOLUE',  'CLOTUREE' ,  'ANNULEE', ],
          datasets: [
            {
              label: '# Graph ticket',
              data: jsonData,
              backgroundColor: [  '#F7FF3C', '#FF7F00',  '#FFA500',  '#008000',  '#8db600', '#DCDCDC'],
              borderColor : ['#red', '#red','#red','#red','#red','#red'],
              borderWidth: 1,
            }
          ],
        }
  })
};
//
//
function loadData(v_url) {
  ///var url = `/pro/api/tickets/${this.project_id}.json/`
  // this.project_id = `${project_id}`
  $.ajax({
    url: v_url,
    type :'GET',
    dataType : 'json',
    async: false,
    success : function(data, status){
      //this.jsonData  = JSON.stringify(data)
      this.jsonData  =  data ;
      //console.log("load data ..." + this.jsonData  );
      //$('#id_aff').html(JSON.parse(data));
      return jsonData
    },
    complete : function(data){
      //
      jsonData  = this.jsonData
      //console.log("load data done ..." + this.jsonData );
      var it_works = true;
    },
    error: function(resultat, status, erreur){
      console.log("Erreur !!" + jsonData );
    }
    });
};
