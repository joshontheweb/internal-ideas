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
        'background-color': '#748c99',
    })
}

readMoreLeave = function(){
    var leaveMorph = this.get('morph');
    var oldColor = this.get('oldColor');
    leaveMorph.start({
        'background-color': this.get('oldColor'),
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
        'opacity': 1,
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
        'opacity': 1,
    });
}

voteHoverLeave = function(){
    var el = this.getParent().getPrevious('p.hover_info');
    morphEl = new Fx.Morph(el, {'duration': 150, 'link': 'cancel'});        
    morphEl.start({
        'opacity': 0,
    });
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
        'keyup': check_length,
    });
    
    // voting hover info
    $$('input.vote').each(function(el){
        el.addEvents({
            'mouseenter': voteHoverEnter,
            'mouseleave': voteHoverLeave,
        });
    });
});
