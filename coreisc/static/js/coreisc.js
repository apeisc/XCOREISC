var valid = $('#id_n_trans').val();
if(valid.length>1)
{
	$('.true').show();
}
$('#sendcheck').on('click',function(){
	var form = $('#id_n_trans').val();
	if(form.length>1)
	{
		$.ajax({ // create an AJAX call...
		  data: 'b='+form, // get the form data
		  url: '/checktrans/', // the file to call
		  beforeSend: function(response){
		    $('.process').html('Cargando..');
		  },
		  success: function(response) { // on success..
		  	if(response=='True')
		  	{
		  		$('.process').html('N° Disponible').addClass('alert-success').removeClass('alert-danger'); 
		  		$('#codediv').addClass('has-success').removeClass('has-error');
		      	$('.true').slideDown();
		  	}else{
		  		$('.process').html('Usted ya forma parte del XXI Coneisc. Te esperamos!').addClass('alert-danger').removeClass('alert-success');
		  		$('#codediv').addClass('has-error').removeClass('has-success');
		  		$('.true').slideUp();
		  	}
		      
		  }
		});
		return false;
	}
  });
$('#id_email').keyup(function(){
	var form = $(this).val();
	if(form.length>0)
	{
		$.ajax({ // create an AJAX call...
		  data: 'b='+form, // get the form data
		  url: '/checkemail/', // the file to call
		  beforeSend: function(response){
		    $('#checkemail').html('Cargando..');
		  },
		  success: function(response) { // on success..
		  	if(response=='True')
		  	{
		  		$('#checkemail').hide();
		  		$('#emaildiv').addClass('has-success').removeClass('has-error');
		  	}else{
		  		$('#checkemail').show().html('Email ya esta en uso').addClass('alert alert-danger');
		  		$('#emaildiv').addClass('has-error').removeClass('has-success');
		  	}
		      
		  }
		});
		return false;
	}else{
		$('#emaildiv').addClass('has-error').removeClass('has-success');
	}
  });
$('#id_username').keyup(function(){
	var form = $(this).val();
	if(form.length>0)
	{
		$.ajax({ // create an AJAX call...
		  data: 'b='+form, // get the form data
		  url: '/checkuser/', // the file to call
		  beforeSend: function(response){
		    $('#checkuser').html('Cargando..');
		  },
		  success: function(response) { // on success..
		  	if(response=='True')
		  	{
		  		$('#checkuser').hide();
		  		$('#userdiv').addClass('has-success').removeClass('has-error');
		  	}else{
		  		$('#checkuser').show().html('user ya esta en uso').addClass('alert alert-danger');
		  		$('#userdiv').addClass('has-error').removeClass('has-success');
		  	}
		      
		  }
		});
		return false;
	}else{
		$('#emaildiv').addClass('has-error').removeClass('has-success');
	}
  });
$('#id_dni').keyup(function(){
	var dni = $(this).val();
	if(dni.length>7 && dni.length<9)
	{
		$('#dnidiv').addClass('has-success').removeClass('has-error');
	}else{
		$('#dnidiv').addClass('has-error').removeClass('has-success');
	}
});
$('#id_first_name').keyup(function(){
	var dni = $(this).val();
	if(dni.length>2 && dni.length<30)
	{
		$('#namediv1').addClass('has-success').removeClass('has-error');
	}else{
		$('#namediv1').addClass('has-error').removeClass('has-success');
	}
});
$('#id_last_name').keyup(function(){
	var dni = $(this).val();
	if(dni.length>2 && dni.length<30)
	{
		$('#namediv2').addClass('has-success').removeClass('has-error');
	}else{
		$('#namediv2').addClass('has-error').removeClass('has-success');
	}
});
$('#id_telefono').keyup(function(){
	var dni = $(this).val();
	if(dni.length>5 && dni.length<15)
	{
		$('#movildiv').addClass('has-success').removeClass('has-error');
	}else{
		$('#movildiv').addClass('has-error').removeClass('has-success');
	}
});
$('#id_password1').keyup(function(){
	var valor = $(this).val();
	if(valor.length>5 && valor.length<21)
	{
		$('#checkpass').hide();
		$('#passdiv').addClass('has-success').removeClass('has-error');
	}else{
		$('#checkpass').show().html('Su clave esta fuera de rango').addClass('alert alert-danger');
		$('#passdiv').addClass('has-error').removeClass('has-success');
	}
});
$('#id_password2').keyup(function(){
	var data = $(this).val();
	var data2 = $('#id_password1').val();

	if(data.length>5 && data.length<21)
	{
		if (data!=data2) {
		$('#checkpass2').show().html('Su clave no coincide con la primera').addClass('alert alert-danger');
		$('#pass2div').addClass('has-error').removeClass('has-success')
		}else{
			$('#checkpass2').hide();
			$('#pass2div').addClass('has-success').removeClass('has-error');
		}
	}else{
		$('#checkpass2').show().html('Su clave esta fuera de rango').addClass('alert alert-danger');
		$('#pass2div').addClass('has-error').removeClass('has-success');
	}
});
$('#newUser').submit(function(){
	$.ajax({
	  data: $(this).serialize(),
	  type: $(this).attr('method'),
	  url: $(this).attr('action'),
	  beforeSend: function(response){
	    //$('span#charcount').html('Enviando...');
	  },
	  success: function(response) {
	      $('.true').html(response);
	  }
	});
	return false;
});


