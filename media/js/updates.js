Updates = {
	'emailForm': function() {
		new Boxy($('#subscribe-form'), {'modal': true, 'title': '&nbsp;', 'closeText': 'закрыть'});
		return false;
	},
	
	'subscribe': function() {
		$('#subscribe-form .error').html('&nbsp;');
		$('div, div span, img', $('#subscribe-form')).toggle();
		
		$.post('/subscribe', { 'email': $('#email').val() }, function(data) {
			if(data.success) {
				$('img, p', $('#subscribe-form')).toggle();
				$('#email-updates').parent().fadeOut('slow');
				return true;
			}
			
			$('div, div span, img', $('#subscribe-form')).toggle();
			$('#subscribe-form .error').show().html(data.error);
		}, 'json');
		
		$('#subscribe-form .error').ajaxError(function() {
			$('div, div span, img', $('#subscribe-form')).toggle();
			$(this).show().html('Ошибка соединения. Попробуйте позже.');
		});
		
		return false;
	}
};
