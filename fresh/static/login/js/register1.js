$(function(){
	var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
	var user_name_val= false;
		pwd_val = false;
		cpwd_val = false;
		email_val = false;
		isChecked = false;
	var pwdval = ''
	$('#user_name').blur(function(){
		user_name_val = validate_user()
	});

	$('#pwd').blur(function(){
		pwd_val = validate_pwd();
	});

	$('#cpwd').blur(function(){
		cpwd_val = validate_pwd2();
	});
	$('#email').blur(function(){
		email_val = validate_email()
	});

	isChecked = $('#allow').prop('checked');
	$('#allow').click(function(){
		isChecked = $(this).prop('checked');
		if(isChecked){
			$('.error_tip2').css({'display':'none'})
		}else{
			$('.error_tip2').css({'display':'block'}).html('请勾选同意')
		}
	});

	function validate_user() {
		var _this = $('#user_name');
		var val = _this.val();
		pwdval = val;
		if(val == '' || val.length<5 || val.length>20){
			_this.next('.error_tip').css({'display':'block'}).html('请输入5-20个字符的用户名')
			return false
		}else{
			$.get('/login/register_exist/?name='+val, function(data){
				if(data.count == 1){
					_this.next('.error_tip').css({'display':'block'}).html('用户名以存在');
					return false
				}else{
					_this.next('.error_tip').css({'display':'none'});
					return true
				}
			});

		}
	}
	function validate_pwd() {
		var _this = $('#pwd');
		var val = _this.val();
		pwdval = val;
		if(val == '' || val.length<8 || val.length>20){
			_this.next('.error_tip').css({'display':'block'}).html('请输入5-20个字符的用户名')
			return false
		}else{
			_this.next('.error_tip').css({'display':'none'});
			return true
		}
	}
	function validate_pwd2() {
		var _this = $('#cpwd');
		var val = _this.val();
		if(pwdval==val){
			_this.next('.error_tip').css({'display':'none'});
			cpwd_val = true
		}else{
			_this.next('.error_tip').css({'display':'block'}).html('两次密码不一致');
			cpwd_val = false
		}
	}
	function validate_email() {
		var _this = $('#email');
		var val = _this.val();
		if(re.test(val)){
			_this.next('.error_tip').css({'display':'none'});
			email_val = true
		}else{
			_this.next('.error_tip').css({'display':'block'}).html('你输入的邮箱格式不正确');
			email_val = false
		}
	}


	$("#reg_form").submit(function () {
		console.log(user_name_val);
		console.log(pwd_val);
		console.log(cpwd_val);
		console.log(email_val);
		console.log(isChecked);
		validate_user();
		validate_pwd();
		validate_pwd2();
		validate_email();

		if(user_name_val == true && pwd_val==true && cpwd_val==true && email_val==true && isChecked==true){
			// console.log(true)
			return true
		}else{
			// console.log(false)
			return false
		}
	})


})