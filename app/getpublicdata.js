//Ricardo Rodiles
//preueba
//dfa
function getData() 
{
  getDataMedicines();
  getDataLaboratorio();
  getDataComentario();
  getDataFarmacia();
	
}
function getDataMedicines() {
  sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({
        url: "/gettweets",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
    tweets = response;
          //alert(response);
          tweets.forEach(function (tweet) 
          {
             var nombre = "<div class='col-md-3 col-sm-3 wow fadeInUp' " +
        " data-wow-delay='0.2s'> " +
                        "<img src='" + tweet.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + tweet.title + "</h3>" +
                        "<h5>" + tweet.description + "</h5>" +
                        "</div>" +
                        "</div>" 
                       $("#medicines").append(nombre);
                });
     
   }
        });          
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}
function getDataLaboratorio() 
{

  sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({
        url: "/getlaboratorios",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
    laboratorios = response;
          //alert(response);
          laboratorios.forEach(function (laboratorio) 
          {
             var nombre = "<div class='col-md-3 col-sm-3 wow fadeInUp' " +
        " data-wow-delay='0.2s'> " +
                        "<img src='" + laboratorio.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + laboratorio.title + "</h3>" +
                        "<h5>" + laboratorio.description + "</h5>" +
                        "</div>" +
                        "</div>" 
                       $("#laboratorios").append(nombre);
                });
     
   }
        });          
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}


function getDataFarmacia() 
{

  sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({
        url: "/getfarmacias",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
    laboratorios = response;
          //alert(response);
          laboratorios.forEach(function (laboratorio) 
          {
             var nombre = "<div class='col-md-3 col-sm-3 wow fadeInUp' " +
        " data-wow-delay='0.2s'> " +
                        "<img src='" + laboratorio.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + farmacia.title + "</h3>" +
                        "<h5>" + farmacia.description + "</h5>" +
                        "</div>" +
                        "</div>" 
                       $("#farmacias").append(nombre);
                });
     
   }
        });          
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}

function getDataComentario() 
{

  sessionStorage.empresa = "kubeet";

    jQuery.support.cors = true;
    try
    {                         
     $.ajax({
        url: "/getcomentarios",
        dataType: 'json',
        cache: false,
        contentType: false,
        processData: true,
        data: {empresa: sessionStorage.empresa},                         
        type: 'get',
        crossDomain: true,
        success: function(response) {
    comentarios = response;
          //alert(response);
          comentarios.forEach(function (comentario) 
          {
             var nombre = "<div class='col-md-3 col-sm-3 wow fadeInUp' " +
        " data-wow-delay='0.2s'> " +
                        "<img src='" + comentario.urlImage + "'" +
                        " class='img-responsive img-circle' alt='team img' heigth='150' width='150'" +
                        " >" +
                        " <div class='section-title wow bounceIn'> " +
                        "<h3>" + comentario.title + "</h3>" +
                        "<h5>" + comentario.description + "</h5>" +
                        "</div>" +
                        "</div>" 
                       $("#comentarios").append(nombre);
                });
     
   }
        });          
     
    }
 catch(e)
    {
      alert("error : " +  e);
     }
}