Account = {
	//LOGIN FORM
	'loginForm': function(loginURL, recoverURL) {
		new Boxy(
			'<form action="'+loginURL+'" method="post" style="width: 270px; margin-bottom: 20px;">\
				<div>\
					<label for="username"><strong>Email или логин</strong></label><br/>\
					<input id="name" name="username" type="text" style="width: 270px;" />\
				</div>\
				\
				<div style="margin-top: 10px;">\
					<label for="password"><strong>Пароль</strong></label><br/>\
					<input id="password" name="password" type="password" style="width: 270px;" />\
				</div>\
				\
				<a href="'+recoverURL+'" style="float: left; margin-top: 10px;">забыли пароль?</a>\
				\
				<div align="right" style="margin: 15px -15px 20px 0;">\
					<span class="button"><input type="submit" value="Войти"></span>\
				</div>\
			</form>', {'modal': true, 'title': '&nbsp;', 'closeText': 'закрыть'});
		
		return false;
	}
};
