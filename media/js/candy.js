Candy = {
	//CART MANAGEMENT EVENTS
	'bindCartEvents': function(cartPreview, addButton, removeButton, clearButton, params) {
		addButton.click(function() { Candy.addToCart(cartPreview, $(this), params); return false; });
		removeButton.livequery('click', function() { Candy.removeFromCart($(this), params); return false; });
		clearButton.livequery('click', function() { Candy.clearCart($(this), cartPreview); return false; });
		cartPreview.parent().parent().submit(function() {Candy.updateCart($(this), cartPreview); return false; });
	},
	
	//EVENTS SPECIFIC TO ORDER MANAGEMENT
	'bindOrderEvents': function(confirmButton, cartPreview) {
		confirmButton.click(function() {
			Candy.updateCart(cartPreview.parent().parent(), cartPreview, '/shop/order'); return false;
		});
	},
	
	//AJAX: ADD ITEM TO CART AND RELOAD CART PREVIEW
	'addToCart': function(cartPreview, addButton, params) {
		addButton.hide().siblings('.ajax-loader').show();
		
		cartPreview.load(addButton.attr('href'), params, function(responseText, textStatus) {
			addButton.show().siblings('.ajax-loader').hide();
			
			if(textStatus == 'error') {
				alert('Ошибка соединения с сервером');
				return false;
			}
				
			itemId = addButton.attr('id').replace(/^b/i, 'i');
			
			alert('"'+$.trim($('#'+itemId+' .desc .title').html())+'" добавлен в корзину');
			
			cartPreview.parent().fadeOut();
			cartPreview.parent().fadeIn('slow');
		});
		
		return true;
	},
	
	//CLEAR CART AND LEAVE MESSAGE
	'clearCart': function(clearButton, cart) {
		clearButton.hide().siblings('.ajax-loader').show();
		
		$.getJSON(clearButton.attr('href'), function(data, textStatus) {
			
			clearButton.show().siblings('.ajax-loader').hide();
			
			if(textStatus != 'success') {
				alert('Ошибка соединения с сервером. Обновите страницу.');
				return false;
			}
			
			cart.children().remove().end().append('<li>Корзина пуста</li>');
		})
	},

	//REQUIRED FOR DELAYED "DATA UPDATED" FADE OUT
	'hideActionNote': function (form) {
		$('.action-note').fadeOut('slow');
	},
	
	//REMOVE ITEM FROM CART
	'removeFromCart': function(removeButton, params) {
		removeButton.hide().siblings('.ajax-loader').show();
		
		$.getJSON(removeButton.attr('href'), function(data, textStatus) {
			removeButton.show().siblings('.ajax-loader').hide();
			
			if(textStatus != 'success') {
				alert('Ошибка соединения с сервером. Обновите страницу.');
				return false;
			}
			
			removeButton.parent().parent().fadeOut('slow', function() {
				$(this).nextAll().each(function() { $(this).toggleClass('odd'); })
				
				if($(this).parent().children('tr').size() == 1)
					$(this).parent().append('<li>Корзина пуста</li>');
				
				$(this).remove();
			});
		});
		
		return false;
	},
	
	//UPDATE CART WITH NEW ITEMS QUANTITY AND COMMENTS
	'updateCart': function(form, cart, redirectURL) {
		
		var postData = {};
		
		$('input[type=submit]', form).hide().siblings('.ajax-loader').show();
		
		// собрать инфу о коментах и количесиве айтемов корзины
		$.each(cart.children('tr'), function() {
			
			id = $(this).attr('id').replace(/^i/i, '');
			
			if( ! id)
				return false;
			
			postData['q'+id] = $('.quantity input', this).val();
			postData['c'+id] = $('.comments textarea', this).val();
			
			return true;
		});
		
		// post-запрос на обновление данных корзины
		$.post(form.attr('action'), postData, function(data, textStatus) {
			if(textStatus != 'success') {
				alert('Ошибка соединения с сервером.');
				return false;
			} else if( ! data.success) {
				alert(data.message);
				return false;
			}
			
			if(redirectURL) window.location = redirectURL;
			
			$('#total').html(['<strong>ИТОГО</strong>:', data.price+' руб.'].join(' '));
			
			$('input[type=submit]', form).show().siblings('.ajax-loader').hide();
			
			// скрыть "Данные обновлены" через несколько секунд
			$('input[type=submit]', form).siblings('.action-note').fadeOut(function() {
				$(this).fadeIn('slow');
				setTimeout('Candy.hideActionNote();', 4000);
			});
		
			return true;
		}, 'json');
		
		return true;
	}
}
