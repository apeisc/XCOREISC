$('#following').mouseenter(
	function(){
		$(this).html('<strong>No asistir&eacute;</strong> <span class="glyphicon glyphicon-remove"></span>');
		$(this).removeClass('btn-primary').addClass('btn-danger');
	});
 $('#following').mouseleave(
	function(){
		$(this).html('<strong>Asistir&eacute; <span class="glyphicon glyphicon-ok"></span></strong>');
		$(this).removeClass('btn-danger').addClass('btn-primary');
	});