$(document).ready(function() {
    // Interceptez la soumission du formulaire
    $('form').submit(function(event) {
        // Empêchez le comportement de soumission par défaut
        event.preventDefault();

        // Récupérez l'URL à partir de l'attribut data-url
        var url = $(this).find('button').data('url');

        // Récupérez les données du formulaire
        var formData = $(this).serialize();

        // Envoyez une requête AJAX au serveur
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                // Mettez à jour la carte avec les données de la réponse
                $('#map-container').html(response.map);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
