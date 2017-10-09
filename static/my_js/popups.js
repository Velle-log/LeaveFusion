function alert(text){
   swal("Info !", text, "info");
}

function successAlert(text){
	swal("Success !", text, "success");
}

function errorAlert(text){
	swal("Error !", text, "error");
}

function successNotif(message){
	var but = $('#notification-success');
	but.attr('data-message', message);
	but.trigger('click');
}

function infoNotif(message){
	var but = $('#notification-info');
	but.attr('data-message', message);
	but.trigger('click');
}


// $('.accept').click(function(e){
//         // e.preventDefault();
//         data = $(this).attr('data');
//         // console.log('hey there'+data);
//         div = $('#leave-request-'+data);
//         body = $('#leave-request-body-'+data);
//         body.append(overlay(data));
//         over = $('#overlay-div-'+data);
//         // alert('#leave-request-'+data);
//         text = $('#remark-'+data);
//         $.ajax({
//             type: 'get',
//             url: '/leave/process-request/'+data,
//             data: {
//                 do: 'accept',
//                 remark: text.val(),
//             },
//             success: function(data){
//                 div.html(after_event('success', "Successfully accepted the request !"));
//             },
//             error: function(data, err){
//                 over.remove();
//                 alert('error');
//                 //TODO: add modal for error
//             },
//         });
//     });