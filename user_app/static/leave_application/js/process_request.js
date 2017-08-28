$(document).ready(function(){
    $('#accept').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        // console.log('hey there'+data);
        div = $('#leave-request-'+data);
        // alert('#leave-request-'+data);
        text = $('#remark-'+data);
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'accept',
                remark: text.val(),
            },
            success: function(data){
                div.html(data.message);
            },
            error: function(data, err){
                alert('error');
                //TODO: add modal for error
            },
        });
    });

    $('#reject').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        div = $('#leave-request-'+data);
        text = $('#remark-'+data);
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'reject',
                remark: text.val(),
            },
            success: function(data){
                div.html(data.message);
            },
            error: function(data, err){
                alert('error');
                //TODO: add modal for error
            },
        });
    });

    $('#forward').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        div = $('#leave-request-'+data);
        text = $('#remark-'+data);
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'forward',
                remark: text.val(),
            },
            success: function(data){
                div.html(data.message);
            },
            error: function(data, err){
                alert('error');
                //TODO: add modal for error
            },
        });
    });

});
