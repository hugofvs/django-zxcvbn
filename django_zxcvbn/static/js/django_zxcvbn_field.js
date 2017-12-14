/*
    Parses and displays password strength results from internal JSON endpoint which uses
    the zxcvbn fuzzy password lib: https://github.com/dropbox/python-zxcvbn
*/

function calcScore() {

    var password = $(this).val();
    var valid = false;

    // URIEncode request so special chars aren't handled as anchors or URL params.
    $.ajax({
        type : 'POST',
        data: JSON.stringify({password: password}),
        url: '/zxcvbn_validator/',
        contentType : 'application/json',
        complete: function(data) {

            valid = data.responseJSON['valid'];  // `valid` will be true or false, matching project settings
            min_length = parseInt(data.responseJSON['min_length']);  // Passed in from project settings
            min_strength = parseInt(data.responseJSON['min_strength']);  // Passed in from project settings
            results = data.responseJSON['results'];
            score = results['score'];

            /*
            How do we measure strength? We need nn/100 for the progress bar.
            Score and crack_time are too jumpy, so we use the relationship between
            current entropy and the project-wide minimum entropy setting for our scale.
            */

            strength = Math.floor(score * (100/min_strength));

            // Vars used in progress bar
            var stylestring = 'width: xx%'.replace('xx', strength);

            // Bootstrap classes for progress bar colors
            var status;
            var statusMessage;
            if (strength >= 80) {
                status = "success";
                statusMessage = "<strong class=\"text-success\">Strong.</strong> Awesome password.";
            } else if (strength >= 60 && strength < 80) {
                status = "info";
                statusMessage = "<strong class=\"text-info\">Good.</strong> Try making it a bit longer.";
            } else if (strength >= 40 && strength < 60) {
                status = "warning";
                statusMessage = "<strong class=\"text-warning\">Not there yet.</strong> You should add numbers or symbols.";
            } else if (strength < 40) {
                status = "danger";
                statusMessage = "<strong class=\"text-danger\">Bad.</strong> Too short, make it at least "+ min_length +" characters long.";
            }

            var progressBar = $('#zxcvbn-progress');
            if (!progressBar.hasClass('interacted-with')) {
                progressBar.addClass('interacted-with');
            }

            // Send hints and info to suggestions div, clearing first
            $('#zxcvbn-messages').empty();

            // Re-draw the progress bar
            barclass = 'progress-bar-'.concat(status); // For Bootstrap
            $('#zxcvbn-strength').attr('style', stylestring);
            $('#zxcvbn-strength').attr('aria-valuenow', strength);

            // So classes don't accumulate, remove them all and replace with new one
            $('#zxcvbn-strength').removeClass().addClass("progress-bar xx".replace('xx', barclass));

            // Append relevant message
            $('#zxcvbn-messages').append("<li>"+statusMessage+"</li>");

            // Clear suggestions if password field emptied
            if (password.length == 0) {
                $('#zxcvbn-messages').empty();
            }
        }
    });
}

//Place this plugin snippet into another file in your applicationb
(function ($) {
    $.toggleShowPassword = function (options) {
        var settings = $.extend({}, options);

        var control = $(settings.control);
        var control_icon = control.children('span');
        var field = $(settings.field);

        control.bind('click', function () {
            if (control.hasClass('masked')) {
                field.prop('type', 'text');
                control.removeClass('masked');
                control_icon.removeClass('glyphicon-eye-open');
                control_icon.addClass('glyphicon-eye-close');
            } else {
                field.prop('type', 'password');
                control.addClass('masked');
                control_icon.removeClass('glyphicon-eye-close');
                control_icon.addClass('glyphicon-eye-open');
            }
        })
    };
}(jQuery));

//Here how to call above plugin from everywhere in your application document body
$.toggleShowPassword({
    field: '#zxcvbn-password',
    control: '#zxcvbn-toggle-show'
});

function callFunctionDebounce(fn, delay) {
  var timer = null;
  return function () {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
}

var calcScoreDebounced = callFunctionDebounce(calcScore, 300);

// Recalculate after slight keypress delay
$('#zxcvbn-password').keyup(calcScoreDebounced);
