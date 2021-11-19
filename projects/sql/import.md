## Import data base athena projects sce
> Cette version integre le module Project Sce

---
<div class="pagebreak"> </div>


### import complet
```sh
loaddata command
```

This command can be use to load the fixtures(database dumps) into database

```sh
./manage.py loaddata user.json
```

> This command will add the user.json file content into the database
Restore fresh database
When you backup whole database by using dumpdata command, it will backup all the database tables

If you use this database dump to load the fresh database(in another django project), it can be causes IntegrityError (If you loaddata in same database it works fine)

To fix this problem, make sure to backup the database by excluding contenttypes and auth.permissions tables

```sh
./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```


> Now you can use loaddata command with a fresh database

```sh
./manage.py loaddata db.json
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
