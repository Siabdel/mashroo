// appel js in html
 <li class="list-group-item"> <a href="javascript:javascript:ouvre_popup('sformule_calcul2')"> OF </a></li>
// afficher les tooltips = infos bull
$('[data-toggle="tooltip"]').tooltip();

$(document).ready(function(){
    // lancer barre
    var i = 0;
    var i_gf = 0;


  // suppression et cloture
  $('#confirm-delete, #confirm-cloture').on('show.bs.modal', function(e) {
      $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
  });
  //-------------------------------
  // lancement des target popup
  // generation ofs + calcul des besoins + Impression des ofs
  //-------------------------------
  $('#delete_group_ofs').on('show.bs.modal', function(e) {
    // on affiche barre progress si ok est saisir
    $(".clss_ok_genere").click(function(event){
      $(".clss_br_wait").show();
      var id_gd_barre = setInterval(gf_barre,  3000);
      var i;
    });
    //confirm("Confirmer la suppression !");
    //$("#id_delete_of").trigger("click");
    //location.reload();
    return false;
  });



  $('#genere-of, #calcul-cbn,  #id_print_ofs_sem').on('show.bs.modal', function(e) {
    // on affiche barre progress si ok est saisir
    $(".clss_ok_genere").click(function(event){
      $(".clss_br_wait").show();
      var id_gd_barre = setInterval(gf_barre,  3000);
      var i;
    });

    $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
  });

  // afficher le nombre total d'of.
   var nb_total = $("#id_sequence_length").text();

   $("#nb_of_sem").text(nb_total);

  // lancer la recherche of / anneee:semaine
  $("#id_submit_search").click(function(event){
    //$("#id_form_search").attr('action', 'gestion_ordre_fabrication?num_sem=24;ancond=18;dcondsce=24');
    // recupere les valeur du select
    var annee = $("#id_an_select" ).val().trim();
    var semaine = $("#id_sem_select" ).val().trim();
    var annee = annee[2] + annee[3]
    var v_search = $("#id_key_search" ).val().trim();

    url = "gestion_ordre_fabrication?list_key='';ancond=" + annee + ";dcondsce=" + semaine + ";key_search=" + v_search;
    //alert("on search!!" + url );

    $("#id_submit_search").attr("href", url);
    $("#id_form_search").submit();

    //event.preventDefault();
  });

  //--
  $("#id_new_of").click(function(event){
    // redirection vers new url
    url = "gestion_ordre_fabrication?list_key='C'"
    window.location.href = url;
  });

  $("#id_of_planifies").click(function(event){
    // redirection vers new url
    url = "gestion_ordre_fabrication?list_key='P'"
    window.location.href = url;
  });

  $("#id_encours_of").click(function(event){
    // redirection vers new url
    url = "gestion_ordre_fabrication?list_key='L'"
    window.location.href = url;
  });

  $("#id_clos_of").click(function(event){
    // redirection vers new url
    url = "gestion_ordre_fabrication?list_key='S'"
    window.location.href = url;
  });



  $(".clss_ok_genere").click(function(event) {
      /* Act on the event */

    $("#id_progressBar").show();
    var myVar = setInterval(myTimer, 1000);
  });

  // Planification groupées
  $("#id_plannifier_of, #id_delete_of, #id_deplannifier_of, #id_desactiver_of").click(function(event) {
    /** Act on the event **/
      if ( event.target.id === "id_plannifier_of"){
          console.log("on planifie les ofs !" + event.target.id );
          $("#form_check_grouper").attr('action', 'update_work_liste');
          $("input[name='form_action']").attr('value', 'plan');

        } else if( event.target.id === "id_deplannifier_of"){
          console.log("on déplanifie les ofs !" + event.target.id );
          $("#form_check_grouper").attr('action', 'update_work_liste');
          $("input[name='form_action']").attr('value', 'unplan');

        } else if( event.target.id === "id_delete_of"){
          if (confirm("Confirmer la suppression !")){
            console.log("on supprime les ofs en masse ! = " + event.target.id );
            $("#form_check_grouper").attr('action', 'update_work_liste');
            $("input[name='form_action']").attr('value', 'delete');
          }
        } else if( event.target.id === "id_desactiver_of"){
          if (confirm("Confirmer la désactivaion de ces ofs !")){
          console.log("on désactivaion de ces of en masse ! = " + event.target.id );
          $("#form_check_grouper").attr('action', 'update_work_liste');
          $("input[name='form_action']").attr('value', 'desactive');
          }
        } else return false;
      $("#form_check_grouper").submit();
  });

  // Planification groupées
  $("#id_delete_of__").click(function(event) {
    /* Act on the event */
    console.log("on planifie les ofs !");
    $("#form_check_grouper").attr('action', 'delete_work_liste');
    $("#form_check_grouper").submit();
  });

  function myTimer() {
      var d = new Date();
      id_barre = progress_bar("#myBar");
      $("#demo").html("Patientez ..." + d.toLocaleTimeString())   ;
      i++;
        if( i > 30){
          clearInterval(id_barre);
          i = 0;
        }
  }

  // fonction  move in progress_bar
  function progress_bar(id_barre) {
    var elem = $(id_barre);
    var width = 1;
    var id = setInterval(frame, 10);

    function frame() {
      if (width >= 100) {
        clearInterval(id);
        elem.css('width',  '0%');
      } else {
        width++;
        //$('#progress_bar').css('width', width + "%");
        elem.css('width',  width + '%');
      }
    }
    return id
  }

  function gf_barre() {
    i_gf++;
    console.log("on barre progress ...");
    if (i_gf >= 5) {
      clearInterval(id_gd_barre);
      console.log("on arrete ...");
    }
  }

});// fin document ready

//--------------------------
//---- checkAll
//--------------------------

function checkAll(event){

     var target = $(event.target) ;

     console.log(target);
     console.log($(event.currentTarget));
     console.log($(event.target));

     //alert( "est ce check ? " + target.is(':checked') );

     if( target.get(0).checked ){
        $('input:checkbox').not(target).not(':checked').prop('checked', true);
        //alert("id   check c'est super" + target.is(':checked'));
        obj =  $('input:checkbox').not(target).not(':checked');
        $.each( obj, function( key, value ) {
            //alert( key + ": " + value );
            console.log("list chekced ! " + key + "val=" + value.id);

          });
     } else {
       //alert("id not  check c'est super" + target.is(':checked'));
       console.log("list not chekced ! " + $('input:checkbox').not(target).not(':checked'));
       $('input:checkbox').not(target).prop('checked', false);
     }
}

<script type="text/javascript">
	$(document).ready(function(){
    // fenetre modal Confirmation
    // hide nb_of_sem
    $("#id_nb_of").hide();
    // Si of est soldé ou lancer on fige l'edition of

    if($("#id_statut").val() == 'S' || $("#id_statut").val() == 'L'){
      $("input").attr( "READONLY", true);
      $("input[type='submit']").prop( "DISABLED", true);
    }

    // url pour lancer la simulation produits à conommer
    $("id_produit_consommer").click( function(){
      //$("simulateur_01").click();
    })

    // si la valeur du realisee change on recalcul le restant
    var qte_restante = parseFloat($("#quantite_prevue").val()) - parseFloat($("#quantite_realisee").val()) ;
    var taux = (parseFloat($("#quantite_realisee").val()) / parseFloat($("#quantite_prevue").val())) * 100
    $("#quantite_restante").val(qte_restante);
    //$("#qte").isPlainObject('object');
    // si la valeur du realisee change on recalcul le restant
    $("#quantite_realisee").change(function(e){
      var qte_restante = parseFloat($("#quantite_prevue").val()) - parseFloat($("#quantite_realisee").val()) ;
      //alert(qte_restante);
      $("#quantite_restante").val(qte_restante);
      // change bar progress
      //$('div.progress-bar').text(taux);

    });

    // controler l'enregistrement
    $("#save_01").click(function(event){
      //alert("on enregistre !!");
      $("#condirm_maj").modal('show');
      event.preventDefault();

    });

    $("#save_02").click(function(event){
     $("#form_01").attr('action', 'modifier_of');
      $( "#form_01" ).submit();
      //alert("on enregistre !!");
      $("#quit_02").click();
      //window.history.go(-1)
      //event.preventDefault();
    });

  // confirmer la cloture d'of
  // afficher popup avec barre progress wait
  $('#confirm_DA').on('show.bs.modal', function(e) {
      // on affiche barre progress si ok est saisir
      $("#id_ok_wait").click(function(event){
        $("#id_br_wait").show();
      });

      $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
  });

  // afficher popup sans barre progress wait
  $('#confirm_cloture, #confirm_start').on('show.bs.modal', function(e) {
      $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
  });
  // confirmer le lancemet d'of
  // afficher popup
  $("#id_lancement").click(function(event){
    $("#id_modal_start").modal('show');
    event.preventDefault();
  });

  // confirmer la lancement d'of
  $("#save_04").click(function(event){
    //modifer la routine de action form
    $("#form_01").attr('action', 'lancement_of');
    // submiter l'of
    $("#form_01" ).submit();
    //alert("on cloture !!");
    $("#quit_04").click();
  });

});// fin document ready


</script>


//Fonction utilisée pour fermer la popup et enlever la classe selected sur le lien
function deselect(e) {
 $('.pop').slideFadeToggle(function()
 {
 e.removeClass('selected');
 });
}
$(function()
{
 //Fonction appelée lorsque l'on clique sur le lien Afficher la fenêtre
 $('#afficherPopup').on('click', function()
 {
 if($(this).hasClass('selected'))
 {
 deselect($(this));
 }
 else
 {
 $(this).addClass('selected');
 $('.pop').slideFadeToggle();
 }
 return false;
 });
 //Fonction appelée lorsque l'on clique sur le lien Fermer la fenêtre
 $('.close').on('click', function()
 {
 deselect($('#afficherPopup'));
 return false;
 });
});
//Fonction d'animation de la fenêtre. Elle permet d'afficher ou de masquer la fenêtre
$.fn.slideFadeToggle = function(easing, callback)
{
 return this.animate({ opacity: 'toggle', height: 'toggle' }, 'fast', easing, callback);
};

function ouvre_popup(page) {
       window.open(page,"nom_popup","menubar=no, status=no, scrollbars=no, menubar=no, width=200, height=100");
}

// fonction  move in progress_bar
function progress_bar() {
  var elem = $("#myBar");
  var width = 1;
  var id = setInterval(frame, 10);

  function frame() {
    if (width >= 100) {
      clearInterval(id);
			elem.css('width',  '0%');
    } else {
      width++;
			//$('#progress_bar').css('width', width + "%");
      elem.css('width',  width + '%');
    }
  }
return id;
}
