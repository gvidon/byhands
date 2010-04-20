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
					'<div id="continue-box"><h2>Это ваш первый заказ?</h2>\
					<p> Просто нажмите кнопку "Дальше" , чтобы перейти на следующий шаг.\
					 \
						<div id="buttons">\
							<form action="/order" method="get"><span class="button">\
								<input type="submit" value="Дальше">\
							</span></form>\
						</div>\
					</div>\
					<div id="auth-box"><h2>Уже что-то заказывали?</h2>\
					 <p>Мы присылали вам письмо с паролем и просьбой активировать аккаунт.\
					\
					<p><form action="'+authURL+'?next='+orderURL+'" method="post">\
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
						<div>\
							<span class="button">\
								<input type="submit" value="Войти">\
							</span>\
						</div>\
					</form></div>', {'modal': true, 'title': '&nbsp;', 'closeText': 'закрыть'}); }
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
			
			// показывать окно с "оформить заказ" отлько в первый раз
			if(cartPreview.siblings('a').children('img').attr('src').match(/_empty/))
				Boxy.ask(
					'<p><strong>'+$.trim($('#'+itemId+' .desc .title').html())+'</strong> добавлен в\
					корзину. Теперь можно <a href="/cart">оформить заказ</a>.</p>',
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
			else {
				cartPreview.parent().fadeOut('fast', function() {
					cartPreview.html(responseText);
					cartPreview.parent().fadeIn('slow');
				});
			}
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
