//function add() {
	//return !$('#select1 option:selected').remove().appendTo('#select2');
//}
//function remove() {
	//return !$('#select2 option:selected').remove().appendTo('#select1');
//}
//$().ready(function() {
//$('#add').click(add);
//$('#select1').dblclick(add);
//$('#remove').click(remove);
//$('#select2').dblclick(remove);
//});

transfer: function(fromId, toId) {
	return !$('#'+fromId).children('option:selected').remove().appendTo($('#'+toId)); 
}
$().ready(function() {
$('#add').click(transfer('select1','select2'));
$('#select1').dblclick(transfer('select1','select2'));
$('#remove').click(transfer('select2','select1'));
$('#select2').dblclick(transfer('select2','select1'));
});
