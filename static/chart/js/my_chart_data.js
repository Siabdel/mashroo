function printChart(target, jsonData){
    //------------------------------------------------------
    var ctx = document.getElementById(target).getContext('2d');

    /// format data
    for(i=0; i < jsonData.length; i++){
      if (jsonData[i] == undefined){
        jsonData[i] = 0;
      }
    }// for
    //
    // init myChart
    var myChart = new Chart(ctx,
       {
        type: 'bar',
        data: {
          labels: ['todo', 'pause', 'doing', 'done', 'closed', 'canceled'],
          //labels: [  'NOUVEAU' , 'ENATTENTE', 'ENCOURS', 'RESOLUE',  'CLOTUREE' ,  'ANNULEE', ],
          datasets: [
            {
              label : '# Graph ticket',

              data : jsonData, // [23, 4, 9, 11, 10]

              backgroundColor: [  '#F7FF3C', '#FF7F00',  '#FFA500',  '#008000',  '#8db600', '#DCDCDC'],
              borderColor : ['#red', '#red','#red','#red','#red','#red'],
              borderWidth: 1,
            }
          ],
        }
      });

      //
      console.log("dans print chart " + jsonData.length)

};
//
//
function loadDataChart(v_url) {
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
      return this.jsonData
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
