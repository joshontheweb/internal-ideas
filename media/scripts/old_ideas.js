check_length = function() {
    var max_length = 500; //set the max length of the form
    var numLeftEl = $('num_left');
    if (this.value.length > max_length) {
        this.value = this.value.substring(0, max_length);
    } else {
        numLeftEl.getChildren('span').set('text', max_length - this.value.length);
    }
}

readMoreEnter = function(){
    var enterMorph = this.get('morph');
    enterMorph.start({
        'background-color': '#748c99'
    })
}

readMoreLeave = function(){
    var leaveMorph = this.get('morph');
    var oldColor = this.get('oldColor');
    leaveMorph.start({
        'background-color': this.get('oldColor')
    });
}

inputFocus = function(){
	this.addClass('glow');
}

inputBlur = function(){
	this.removeClass('glow');
}

voteHoverEnter = function(){
    var el = this.getParent().getPrevious()
    alert(el.get('text'));
    var morphEl = new Fx.Morph(el, {'duration': 150});
    morphEl.start({
        'opacity': 1
    });
}

voteHoverEnter = function(){
    var el = this.getParent().getPrevious('p.hover_info');
    if (this.hasClass('down')){    
        el.set('text', 'Not so good');
    }
    else {
        el.set('text', 'Great idea!');
    }
    morphEl = new Fx.Morph(el, {'duration': 150, 'link': 'cancel'});        
    morphEl.start({
        'opacity': 1
    });
}

voteHoverLeave = function(){
    var el = this.getParent().getPrevious('p.hover_info');
    morphEl = new Fx.Morph(el, {'duration': 150, 'link': 'cancel'});        
    morphEl.start({
        'opacity': 0,
    });
}

var voteAjax = function(event) {
    var voteDiv = this.getParent('div.voting');
    var rankEl = voteDiv.getChildren('.rank');
    var html = "<h2>Why?</h2>";
        html += "<p>Your vote means so much more if you provide feedback.</p>"
        html += "<form action=''>";
        html += "<textarea></textarea>";
        html += "<input type='submit' value='Submit' />";
        html += "<input type='submit' value='No Thanks' />";    
        html += "</form>";
    event.stop();
    var scoreEl = rankEl.getElement('p');
    var form = this.getParent('form');
    var url = form.get('action');
    
    var request = new Request({
        url: url,
        method: 'post',
        onSuccess: function(response) {
            // alert(response);
            itemMeta = JSON.decode(response);
            if (itemMeta.success == false) {
                var loginRequest = new Request.HTML({
                    method: 'get',
                    url: "/accounts/login/",
                    onSuccess: function(responseTree, responseElements) {
                        // alert(responseTree.item(1));
                        var contentDiv = new Elements(responseElements).filter('div#content');
                        var html = '<h2>Please Login</h2>'+ contentDiv.get('html');
                        modalPopup(html);
                    },
                }).send();
            }
            else if (itemMeta.success == true) {
                scoreSet(scoreEl, itemMeta);
                modalPopup(html);
            }
        }
    }).send();
    
}

var textSwap = function(el, newText) {
    // el.fade('out').get('tween').chain(function() { el.set('text', newText) })
    el.set('text', newText);
}

var scoreSet = function(scoreEl, scoredObj) {
    scoreEl.set('text', scoredObj.score.score);
}

var modalPopup = function(html) {
    var container = $('main');
    var el = new Element('div', {
        'html': html,
        'id': 'vote_popup',
        'styles': {
            'opacity': 0,
        },
    });
    
    var backdrop = new Element('div', {
       'id': 'backdrop',
       'styles': {
           'opacity': 0,
        }, 
    });
    // this.getParent('div.voting');
    backdrop.inject(container, 'top').fade('0.4');
    el.inject(container, 'top').fade('in');
    
    // click events for popup
    var dismiss = $$("#backdrop", "#vote_popup input[type=submit]");
    dismiss.each(function(el){
        if (el.get('tag') == 'input') {
            var form = el.getParent('form');
            el.addEvents({
                'click': modalSubmit.bind(form),
            })
        }
        else {
            el.addEvents({
                'click': modalDismiss.bind(dismiss),
            })
        }
        el.addEvents({
            'click': modalSubmit.bind(form),
            // 'click': modalDismiss.bind(dismiss),
        })
    })
}

var modalDismiss = function(event) {
    // event.stop();
    var modal = $$('div#vote_popup', '#backdrop');
    if ($$('#vote_popup textarea').get('value') == '') {
        // $$('#vote_popup h2').set('text', 'Next Time');
        textSwap($$('#vote_popup h2'), 'Thank You');
    }
    else {
        // $$('#vote_popup h2').set('text', 'Thank You');
        textSwap($$('#vote_popup h2'), 'Thank You');
    }
    var fadeDestroy = function() {
        var el = this;
        this.fade('out').get('tween').chain(function(){ el.destroy() });
    }
    
    modal.each(function(el){
        fadeDestroy.delay(300, el);
    });
}

var modalSubmit = function(event) {
    event.stop();
    var url = this.get('action');
    var data = this.toQueryString();
    // alert(url);
    // alert(data);
    request = new Request({
        method: 'post',
        url: url,
        data: data,
    }).send();
    // window.location = "/";
    modalDismiss();
}

window.addEvent('domready', function() {
    
    // readmore color morph
	var readMore = $$('.readmore a');
	readMore.each(function(el){
	    el.set('morph', {'duration': 150});
	    el.set('oldColor', el.getStyle('background-color'));
    	el.addEvents({
    	    'mouseenter': readMoreEnter,
    	    'mouseleave': readMoreLeave,
    	})
    	
	});
	
	// textarea counter
    var ideaEl = $('idea_textarea');
    ideaEl.addEvents({
        'focus': inputFocus,
        'blur': inputBlur,
        'keydown': check_length,
        'keyup': check_length
    });
    
    // voting hover info
    $$('input.vote').each(function(el){
        el.addEvents({
            'click': voteAjax.bind(el),
            // 'mouseenter': voteHoverEnter,
            // 'mouseleave': voteHoverLeave,
        });
    });
});
