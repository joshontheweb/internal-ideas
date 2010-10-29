var checkLength = function() { // Adjusts the counter and trims the text area to a max of 500 characters.
    var maxLength = 500; // Max char num for the form
    var textArea = $('#idea_textarea');
    var numLeft = $("#num_left > span");
    var charCount = textArea.val().length;

    if((maxLength - charCount) < 0) {
        textArea.val(textArea.val().substring(0, maxLength));
        numLeft.html(maxLength - charCount);
    }
    else {
        numLeft.html(maxLength - charCount);
    }
};


var setUpCounter = function() {
    // Set up the focus and blur events for the idea text area
    var ideaForm = $('#idea_textarea');
    ideaForm.focus(function(){
        interval = window.setInterval(checkLength, 100);
    });
    ideaForm.blur(function(){
        clearInterval(interval);
    });
};


var voteAjax = function(event){
    event.preventDefault();
    var voteForm = $(this).parent();
    var score = voteForm.parent().find('.rank > p');
    var url = voteForm.attr('action');
    
    $.ajax({
        url: url,
        type: 'post',
        success: function(response){
            data = JSON.parse(response);
            if (data.success == false) {
                // request failed
            }
            else if (data.success == true) {
                score.html(data.score.score);
            }
        },
    });
};


$(document).ready(function() {
    setUpCounter();

    // Bind the voting ajax call
    $('input.vote').click(voteAjax);
});
