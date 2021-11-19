# Synthaxe json en python & JavaScript


### 1. Définition

> C'est un micro framework Python
> pratique pour un developpement rapide de API python
>



### 2. structure d'une application Flask

```py
myproject/
   ├──app/
   |  ├── __init__.py
   |  ├── models.py
   |  ├── templates/
   |  └── views.py
   ├── tests/
   ├── run.py
   ├── requirements.txt
   └── config.py

```


### 1. exemple  app FLASK

$ printenv FLASK_APP
/Users/me/code/project/run.py

```py

#! coding:utf-8
from flask import Flask
from flask import request #Import flask requests
from flask import render_template as render #Import flask render templates
import json, urllib #import api modules


app = Flask("__name__")

from app import request


@app.route("/")
@app.route("/home")
def hello():
    return '<h1>Hello World!</h1>'

@app.route("/login")
def logon():
    user = request.args.get('username')
    passwd = request.args.get('paddword')
    #
    # validate
    return render("ok")

if '__name__' == '__main__' :

    app.run()

```

### 3. Templates


```html
<!DOCTYPE html>
<html lang="fr">
<head>

</head>

<body>
    <h1> Identificatiez -vous </h1>
    <form action="." method="POST">
        <input type="text" name="username" placeholder="Entrez votre identifiant ">
        <input type="password" name="password" placeholder="Entrez votre mot de passe ">
        <input type="submit" name="my-form" value="Ok">
    </form>
</body>
</html>
```

#### filtres jinja2

| filtre name | description |
| --- | --- |
| safe | Renders the value without applying escaping |
| capitalize | Converts the first character of the value to uppercase and the rest to lowercase |
| lower | Converts the value to lowercase characters |
| upper | Converts the value to uppercase characters |
| title | Capitalizes each word in the value |
|trim   | Removes leading and trailing whitespace from the value |
|striptags  | Removes any HTML tags from the value before renderi  |



---
<div class="pagebreak"> </div>


### Mise en œuvre en Flask

implémenter dans différentes vues, (et donc d’avoir plusieurs routes ayant la même URL, mais des verbes différents) :

```py

@app.route("/bidules/", methods=['GET'])
def bidules_list():
    # ...

@app.route("/bidules/", methods=['POST'])
def bidules_new():
    # ...

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


.pagebreak
{
	page-break-after: always;
}
</style>
