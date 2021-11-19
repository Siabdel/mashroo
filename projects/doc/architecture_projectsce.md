![flux](images/logo.png)

## <center> Architecture Project Sce </center>
#### <center> Jump start vue.js </center>

---
![projet](images/vuejs.png)

## Comosants project report

| component name | filename | path | template_name | filename | path | comment |
| --- | --- | --- | --- | --- | --- | --- |
| project_report_cpn | app.js | /static/vuejs/project/chart/ | rapport_template | project_rapport_component | template/project/chart/ | stat actions prj |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |


## Project 3D chart

| titre | description |
| --- | --- |
| template | "businessce/project_3D_chart.html" |
| js | businesssce/static/js/my_3Dchart_data |
| url | url(r'^print/chart3D/$', businessviews.print_chart_3D,  name='print_chart_3d') |
|  |  |


 =
 var jsonData2 = {'data' : [ {
     "status": "nouveau",
     "taches": 4025,
     "color": "#FF0F00"
   }, {
     "country": "China",
     "visits": 1882,
     "color": "#FF6600"
   }, {
     "country": "Japan",
     "visits": 1809,
     "color": "#FF9E01"
   }, {
     "country": "Germany",
     "visits": 1322,
     "color": "#FCD202"
   }, {
     "country": "UK",
     "visits": 1122,
     "color": "#F8FF01"
   }]
 };


<style>
body {
      font-family: Verdana, Helvetica, sans-serif;
      //font-family: Times, Times New Roman, serif;
      font-size:12px;
      }

table {
      color: #1123A3;
      //font-family: Georgia, "Times New Roman", serif;
      font-family: Trebuchet MS, sans-serif;
      font-size: 8px;
  }


ol li, ul li {
  color:blue;
  text-style:bold;
  background-color:#fcfcfc;
  border-color:#f6bf01;
  font-size:14px;
  line-height:1.75;
}

.pagebreak
{
	page-break-after: always;
}
</style>
