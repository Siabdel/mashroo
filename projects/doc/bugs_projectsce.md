![flux](images/logo.png)

## <center> Bugs ProjectSCE  </center>
#### <center> 15 Juin 2020 </center>

---


![projet](images/mens_project.jpg)



>  install projetsce sur la VM Odysee

---
<div class="pagebreak"> </div>


### 1. Liste des bugs Juin 2020

> Suite a des tests effectueé par Christine delphin
>

| date             | Déscription                                                                                                                         | Solution                                                                                                                                                                                                                                                                                          | Statut |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 17 Juin 2020     | toutjours pas de possibilité de changer la photo du projet                                                                          | depuis la migration sur la VM Odysee , le système de fonctionnalités qui permet gérer les médias images (jpeg, png ), vidéo (avi, mpeg4)  est en panne il reste quelques packages invalides sur lesquels je travail pour les porter sur la nouvelle version du système  Debian 10 de la VM Odysee | OK    |
| 17 Juin 2020     | TODO -> je ne sais pas comment supprimer les lignes                                                                                 | pour supprimer une ligne c'est simple ,  tu clique sur la ligne concerné , une croix s"active a droite de la ligne  pour supprimer cet enregistrement                                                                                                                                             | Ok     |
| 17 Juin 2020     | Est-il possible dans la liste des tache d'avoir une bulle avec le nom du projet quand tu mets ta souris sur le code projet ? Merci, |                                                                                                                                                                                                                                                                                                   | Ok     |
|                  |                                                                                                                                     |                                                                                                                                                                                                                                                                                                   |        |
| 22 Juin 2020     | Pour clôturer une tache à partir de la liste des tâches -> ne fonctionne pas. Obliger d'aller la modifier et la cloturer            |                                                                                                                                                                                                                                                                                                   |        |
| 22 Juin 2020     | TODO -> je ne sais pas comment supprimer les lignes.                                                                                |                                                                                                                                                                                                                                                                                                   |OK    |
| 22 Juin 2020     | Page not FOUND ! http://dysee:90/pro/projects/tickets/2236/                                                                         |    page fantôme car pas de enregistrement correspondant                                                                                                                                                                                                                                                                                               |   ??     |
| 22 Juin 2020     | pour recévoir un email à la création de la tache ou projet  une assignation de tache / rappels ...                                                                                                                               |                                                                                                                                                                                                                                                                                                   |        |
| 29 Juin 2020     | simplification saisie project /ticket , synchroniser le titre avec le champ description par defaut en ajout et en modifier          | modifer form.save(commit=False) avec self.description = self.titre  si elle est vide                                                                                                                                                                                                              | ok     |
| 29 jui 2020      | Correction bloc saisie multimedia images , vidéo et document                                                                        |                                                                                                                                                                                                                                                                                                   |   OK     |
| 29 juin 2020     | Corrections todo : suppresion /modif                                                                                                | suppression ok                                                                                                                                                                                                                                                                                    |        |
| 07 Juillet 2020  | suppresion des taches dans ecran "mes taches"                                                                                       |                                                                                                                                                                                                                                                                                                   | ko     |
|                  |                                                                                                                                     |                                                                                                                                                                                                                                                                                                   |        |





##

```sh

$ sudo apt-get update
$ sudo apt-get install curl

```

Est-il possible dans la liste des tache d'avoir une bulle avec le nom du projet quand tu mets ta souris sur le code projet ? Merci,

TODO -> je ne sais pas comment supprimer les lignes.

---
<div class="pagebreak"> </div>


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
      color: #00E;
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

atom-text-editor::shadow .table.gfm {
    font-family: monospace;
}

atom-text-editor .syntax--table.syntax--gfm {
    font-family: monospace;
}
</style>
