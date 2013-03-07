jQuery(document).ready(function($) {
    if (typeof(console) === 'undefined') {
        var f = function () {};
        var console = { log: f, warn: f, error: f };
    }

    $('form#vote_up').on('submit', function(event) {
        // Prevent the form from submitting via normal request
        event.preventDefault();

        // Keep a reference to the form
        var $form = $(this);

        $.ajax({
            url: $form.attr('action'),

            method: 'POST',

            dataType: 'json',

            data: $form.serialize(),

            success: function (data, textStatus, jqXHR) {
                var question;
                if (typeof(data) === 'object') {
                    question = data;
                } else if (typeof(data) === 'string') {
                    question = JSON.parse(data);
                } else if (typeof(data) !== 'object') {
                    throw "data is not an object";
                }

                // Oops! another bug here.
                $form.find('.vote-count').text(question.up);
            },

            error: function (data, textStatus, jqXHR) {
                console.warn("Request failed with status: '" + textStatus + "'");
            }
        });
    });
});





