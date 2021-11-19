# Sliker
`sliker` is a web slider/slideshow written in `jQuery`.

Demo here (GitHub Page) :
### <http://zenike.github.io/sliker/>

# Dependencies
- `jQuery`: compatible with all the versions of jQuery
- `Less`: this plugin css is written in less. Some less variables need to be defined in order to make it work.
- `FontAwesome`: the navigation arrows use FontAwesome icons by default. It is possible to not use it (by replacing the icons by your own files, as demonstrate further in this doc).

# Installation
1. get the files `sliker.less` and `sliker.js` in the root of the GitHUb project or install the package via npm.
2. include the `sliker.js` file in the end of the document. Before the `</body>` close tag.
3. Use `sliker.less` to generate a css file.

# Use
- create the basic html structure following this example
```html
<div id="slider_example" class="sliker">
	<div class="sliker__window">
		<ul class="sliker__track">
			<li class="sliker__item"><img src="./example.jpg"></li>
			<li class="sliker__item"><img src="./example.jpg"></li>
			<li class="sliker__item"><img src="./example.jpg"></li>
		</ul>
	</div>
</div>
```
- declare the slider via jQuery
```javascript
$('#slider_example').sliker({
'nbr_li': 1, // number of elements to pass at each slider move event
'vitesse_auto': 3000, // timer between two automatic movements
'vitesse': 0.5, // speed of a slide movement (same parameter for the automatic move and the click event move)
'auto': 0, // active (1) and use 'vitesse_auto' to control the timer, deactivate (0) or set to 'custom' (see the "Timer" section)
'type': 'none', // define the role of the slider when linked with another one. Values : 'visualiseur', 'menu', 'none'
'cible': 'none', // define the id of the linked slider if there is one (ex: '#slider_deux').
'isolement': 0, // if used (1), the slider will be isolated by a transparent black background when used
'pc_only': 0, // if used (1), the slider will be hidden on all the mobile devices
'loop': 0, // if used (1), the slider will repeat itself to create an infinite loop
'liquid': 1, // if used (1), each element (.sliker__item) will take the full width of the slider, in a responsive way
'drag': 0, // if used (1), allow the slider to be moved by click-and-drag
'creer_afficheur': 0, // if used (1), create dynamically a div on top of the slider with the zoomed picture in it
'fading_mode': 0, // if used (1), replace the defaut transition (rail mode) by a fading
'fading_type': 1, // only work when fading_mode is set to 1. When '1' : white fading. When '2' : cross-fading betwwen the pictures
'buffering_nbr': 1, // number of pictures preloaded (before and after the active picture). Require the use of 'data-src' in place of 'src' on the img tags
'fullscreen': 0, // if used (1), show a fullscreen button that allow the active picture to be zoomed in a popup
'bullets': 1, // if used (1), show the navigation bullets under the slider
'bullets_limit': 20, // only work when 'bullets' is set to 1. Limit the number of bullets to show before switching to the 'pages menu' display (ex: 7/22)
'bullets_limit_mobile': 8, // identical to 'bullets_limit' but apply only on mobile devices
'arrows': 2, // display or hide the navigation arrows. 0 = hidden, 1 = hidden on mobile, 2 = always show
});
```

# Customization

## Couleurs
Par défaut, le less de Slike chercher après la variable @theme et se sert de celle-ci pour coloriser ses éléments de navigation.
Il est donc nécessaire que cette variable existe.
Il est toutefois possible de modifier ses couleurs indépendement en utilisant en ciblant le slider en CSS et
en utilisant un mixin LESS :
```html
.sliker_colors(@color,@bg);
```
- @color pour la couleur de fond (au repos) des puces et fleches.
- @bg pour la couleur active (survol) des puces et fleches.

##### Exemple
```css
#slider_example{
.sliker_colors(red,white);
}
```

## Icones
Par défaut, Sliker utilise des icones font-awesome pour ses flèches de navigation et des span arrondis en CSS pour ses puces.
Ces éléments sont remplaçables facilement par d'autres icones (FontAwesome ou autre).

- pour remplacer les flèches, ajouter un attribut `data-arrow` à la base du slider et y spécifier la classe `FontAwesome` ou autre (set d'icone personnalisé). Il est nécessaire que ces nouvelles flèches aient deux variantes se terminant respectivement par `-left` et par `-right`. Indiquez le mot clé dans `data-arrow` sans la terminaison indiquant le sens (voir exemple ci dessous).

##### Exemple
```html
<div id="slider_example" class="sliker" data-arrow="fa fa-caret" >
	<div class="conteneur_strict">
		...
```

- Pour remplacer les puces, utiliser l'attribut `data-bullet` à la base du slider et y spécifier la classe FontAwesome ou autre (set d'icone personnalisé).

##### Exemple
```html
<div id="slider_example" class="sliker" data-bullet="fa fa-star" >
	<div class="conteneur_strict">
		...
```

## Timer
Sliker permet de configurer un mode de défilement automatique. Cette option se configure au moment de l'appel javascript en spécifiant la propriété `auto`. `auto` à 0 désactivera le défilement automatique alors que `auto`à 1 l'activera et utilisera la propriété `vitesse_auto` comme temps d'attente entre deux slides.
La dernière option est "custom". Si `auto` est paramétré sur "custom", chaque slide peut avoir son propre timer. Pour indiquer ces timings il suffit d'écrire une valeur temporelle, en minisecondes, dans un attribut data-timer sur chaque li du slider.
Important: en mode custom, chaque li doit posséder son propre data-timer, sans exception.

##### Exemple
```html
<div id="slider_example" class="sliker" data-arrow="fa fa-caret-left" >
	<div class="conteneur_strict">
		<ul class="grand_slider">
			<li data-timer="3000">
				...
```

## Variables LESS
Ces variables s'appliquent en css. Il faut cibler le slider dans le css normal (par son id par exemple) et lui appliquer un de ces mixins:

```html
.sliker_colors(@color,@bg);
```
- @color pour la couleur de fond (au repos) des puces et fleches.
- @bg pour la couleur active (survol) des puces et fleches.

```html
.sliker_bullets(@size,@round,@specific_span_width);
```
- @size pour la taille: hauteur et largeur de la puce ou font-size de l'icone.
- @round pour l'arrondi de la puce (ex:2px pour un carré légèrement arrondi) => inutile si la puce est une icone
- @specific_span_width : optionnel, spécifie une largeur différente de la hauteur => inutile si la puce est une icone

```html
.sliker_bullets_out(@spacing);
```
- @spacing pour modifier les marges (top et bot) des boutons.
- ce mixin sort les puces du slideret les positionnes après celui ci. Ecrire .sliker_bullets_out; sans option est donc tout à fait viable.

```html
.sliker_bullets_in(@spacing);
```
- position par defaut !
- @spacing pour modifier la marge des boutons (séparation du bas du slider).
- ce mixin rentre les puces dans le bas du slider, par dessus le contenu. Ecrire .sliker_bullets_in; sans option est viable et appliquera la marge par defaut.

```html
.sliker_arrows_out(@spacing);
```
- @spacing pour modifier l'espacement entre les fleches et le bord du slider (sans compter le padding autour de l'icone).
- ce mixin sort les fleches en dehors du slider. Ecrire .sliker_arrows_out; utilsera un spacing de 0px et les fleches seront contre le slider.

```html
.sliker_arrows_in(@spacing);
```
- position par defaut !
- @spacing pour modifier l'espacement entre les fleches et le bord du slider (sans compter le padding autour de l'icone).
- ce mixin rentre les fleches dans le slider. Ecrire .sliker_arrows_in; utilsera un spacing de 0px (par defaut) et les fleches seront contre le slider.

## Informations diverses
- départ sur un slide précis possible grace à la classe "selected" à mettre sur un "li".
- mettre la class "vam" (pour vertical align middle) sur la base du slider pour que les li soient alignés verticalement.
- mettre la classe "safeload" à la racine (.sliker) afin d'avoir un chargement moins saccadé dans le cas d'un slider élastique (une image).
