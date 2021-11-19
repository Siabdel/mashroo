## Export data base athena projects sce

### Export data base athena projects sce Mars 2020

> Cette version integre le module Project Sce

---
<div class="pagebreak"> </div>



### export complet

```sh
./manage.py dumpdata  --indent 2  > db_athena.json
./manage.py dumpdata  --indent 2 --exclude ofschedule.DjangoOF  > db_all_athena2.json
./manage.py dumpdata  ofschedule --indent 2   > db_ofschedule_athena2.json
```

### export admin
```sh
./manage.py dumpdata admin --indent 2  > db_admin_athena.json
```

### export table user
```sh
./manage.py dumpdata auth.user --indent 2   > db_user_athena.json
```


### export table user
```sh
./manage.py dumpdata projects --indent 2 --exclude projects.Member   > db_projects_athena.json
```


<style>
h1 {
  text-align:center;
}

body {
      //font-family: Verdana, Helvetica, sans-serif;
      font-family: Times, Times New Roman, serif;
      font-size:12px;
      margin: 0px;
      padding: Opx
      }

p, table {
      color: #2A223A;
      font-family: Georgia, "Times New Roman", serif;
  }


ol li, ul li {
  color: #1111FF;
  text-style:bold;
  background-color:#FFFFF;
  border-color:#f6bf01;
  font-size: 13px;
  line-height:1.77;
}

.event-color-red{
  background-color:red;
  color:white;
  display:block;
  text-align: center;
}

.event-color-green{
  background-color:green;
  color:white;
  display:block;
  text-align: center;
}

.event-color-yellow{
  background-color:yellow;
  color:black;
  display:block;
  text-align: center;
}
////////////////
// STATUT COLOR
////////////////


.status-color-red{
  background-color:red;
  color:white;
  display:block;
  text-align: center;
}


.status-color-yellow{
  background-color:yellow;
  color:black;
  display:block;
  text-align: center;
}


.status-color-green{
  background-color:green;
  color:white;
  display:block;
  text-align: center;
}

.status-color-blue{
  background-color:blue;
  color:white;
  display:block;
  text-align: center;
}

.status-color-grey{
  background-color:grey;
  color: white;
  display:block;
  text-align: center;
}


.status-color-orange{
  background-color:#FFA500;
  color:white;
  display:block;
  text-align: center;
}


.status-color-apple{
  background-color:#8db600;
  color:white;
  display:block;
  text-align: center;
}


.pagebreak
{
	page-break-after: always;
}
</style>
