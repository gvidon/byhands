Candy = {
	//CART MANAGEMENT EVENTS
	'bindCartEvents': function(cartPreview, addButton, removeButton, clearButton, params) {
		addButton.click(function() { Candy.addToCart(cartPreview, $(this), params); return false; });
		removeButton.livequery('click', function() { Candy.removeFromCart($(this), params); return false; });
		clearButton.livequery('click', function() { Candy.clearCart($(this), cartPreview); return false; });
		
		$('.quantity input, .comments textarea').change(function() { Candy.updateCart(
			$(this).siblings('.ajax-loader'), cartPreview.parent().parent(), cartPreview
		); return false; });
	},
	
	//EVENTS SPECIFIC TO ORDER MANAGEMENT
	'bindOrderEvents': function(confirmButton, cartPreview, isAuthorised) {
		confirmButton.click(function() {
			if(isAuthorised)
				window.location=orderURL;
			
			// предложить авторизацию для ускорения ввода данных о заказчике
			Candy.updateCart(
				$(this).siblings('.ajax-loader'),
				cartPreview.parent().parent(),
				cartPreview,
			
				function() { new Boxy(
					'<p style="width: 300px; font-size: 0.91em;">Вы уже совершали у нас заказы? Введите email и\
					пароль, который мы вам отправляли. Если нет - просто <a href="'+orderURL+'">продолжите</a></p>\
					\
					<form action="'+authURL+'?next='+orderURL+'" method="post" style="width: 220px; margin-left: 35px; margin-bottom: 40px;">\
						<div>\
							<label for="username"><strong>Email</strong></label><br/>\
							<input id="name" name="username" type="text" style="width: 220px;" />\
						</div>\
						\
						<div style="margin-top: 10px;">\
							<label for="password"><strong>Пароль</strong></label><br/>\
							<input id="password" name="password" type="password" style="width: 220px;" />\
						</div>\
						\
						<div align="right" style="margin: 15px -15px 20px 0;">\
							<span class="button">\
								<input type="submit" value="Войти">\
							</span>\
						</div>\
					</form>', {'modal': true, 'title': '&nbsp;', 'closeText': 'закрыть'}); }
			);
		
			return false;
		});
	},
	
	//AJAX: ADD ITEM TO CART AND RELOAD CART PREVIEW
	'addToCart': function(cartPreview, addButton, params) {
		addButton.hide().siblings('.ajax-loader').show();
		
		$.post(addButton.attr('href'), params, function(responseText, textStatus) {
			addButton.show().siblings('.ajax-loader').hide();
			
			if(textStatus == 'error') {
				alert('Ошибка соединения с сервером');
				return false;
			}
				
			itemId = addButton.attr('id').replace(/^b/i, 'i');
			
			Boxy.ask(
				'<p><strong>'+$.trim($('#'+itemId+' .desc .title').html())+'</strong> добавлен в\
				корзину. Теперь можно <a href="/shop/cart">оформить заказ</a>.</p>',
				['закрыть'],
				
				function() {
					cartPreview.parent().fadeOut('fast', function() {
						// заменить серенькую корзину на цветную
						cartPreview.siblings('a').children('img').attr('src',
							cartPreview.siblings('a').children('img').attr('src').replace('_empty', '_with_price')
						).css('margin-right', '-95px');
						
						cartPreview.html(responseText);
						cartPreview.parent().fadeIn('slow');
					});
					
				}, {modal: true}
			);
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
		
		//запрос на удаление
		$.getJSON(removeButton.attr('href'), function(data, textStatus) {
			removeButton.show().siblings('.ajax-loader').hide();
			
			if(textStatus != 'success') {
				alert('Ошибка соединения с сервером. Обновите страницу.');
				return false;
			}
			
			//обновить ИТОГО
			$('#total').html('<strong>ИТОГО</strong>: '+data.price+' руб');
			
			if( ! parseFloat(data.price))
				$('#make-order').hide();
						
			//медленно скрыть айтем
			removeButton.parent().parent().fadeOut('slow', function() {
				$(this).nextAll().each(function() { $(this).toggleClass('odd'); })
				
				if($(this).parent().children('tr').size() == 1)
					$(this).parent().append('Корзина пуста');
				
				$(this).remove();
			});
		});
		
		return false;
	},
	
	//UPDATE CART WITH NEW ITEMS QUANTITY AND COMMENTS
	'updateCart': function(ajaxLoader, form, cart, callback) {
		
		var postData = {};
		
		ajaxLoader.show();
		
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
			
			$('#total').html('<strong>ИТОГО</strong>: '+data.price+' руб.');
			
			ajaxLoader.hide();
			
			if(typeof callback == 'function')
				callback();
			
			return true;
		}, 'json');
		
		return true;
	}
}
