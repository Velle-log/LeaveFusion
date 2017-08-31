$(document).ready(function(){


    function overlay(data){
        var over = "<div class='overlay' id='overlay-div-"+data+"'><i class='fa fa-refresh fa-spin'></i></div>";
        return over
    }
    

    function after_event(result, intext){
        if(result == 'success')
            var symbol = "check";
        else
            var symbol = "info";
        var afterhtml = "<div class='col-md-8'><div class='alert alert-"+result+" alert-dismissible'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button><h4><i class='icon fa fa-"+symbol+"'></i> Alert!</h4>"+intext+"</div></div>";
        return afterhtml;
    }



    $('.accept').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        // console.log('hey there'+data);
        div = $('#leave-request-'+data);
        body = $('#leave-request-body-'+data);
        body.append(overlay(data));
        over = $('#overlay-div-'+data);
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
                div.html(after_event('success', "Successfully accepted the request !"));
            },
            error: function(data, err){
                over.remove();
                alert('error');
                //TODO: add modal for error
            },
        });
    });

    $('.reject').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        div = $('#leave-request-'+data);
        body = $('#leave-request-body-'+data);
        body.append(overlay(data));
        over = $('#overlay-div-'+data);
        text = $('#remark-'+data);
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'reject',
                remark: text.val(),
            },
            success: function(data){
                div.html(after_event('danger', "The Leave request has been rejected !"));
            },
            error: function(data, err){
                over.remove();
                alert('error');
                //TODO: add modal for error
            },
        });
    });

    $('.forward').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        div = $('#leave-request-'+data);
        body = $('#leave-request-body-'+data);
        body.append(overlay(data));
        over = $('#overlay-div-'+data);
        text = $('#remark-'+data);
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'forward',
                remark: text.val(),
            },
            success: function(data){
                div.html(after_event('success', "Successfully forwarded the request !"));
            },
            error: function(data, err){
                over.remove();
                alert('error');
                //TODO: add modal for error
            },
        });
    });

});
