$(document).ready(function () {
  // Función de filtrado para la búsqueda de comunidades
  function filterCommunities() {
    var value = $("#commSearch").val().toLowerCase();
    $("#communities-grid .card").each(function () {
      var cardTitle = $(this).find(".card-title").text().toLowerCase();
      if (cardTitle.indexOf(value) > -1) {
        if($(this).parent().hasClass("hidden-card")) {
          $(this).parent().removeClass("hidden-card");
        }
      } else {
        if(!$(this).parent().hasClass("hidden-card")) {
          $(this).parent().addClass("hidden-card");
        }
      }
    });
  }

  $("#commSearch").on("keyup", filterCommunities);
});