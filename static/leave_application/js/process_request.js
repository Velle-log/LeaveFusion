$(document).ready(function(){


    function overlay(data){
        var over = "<div class='ui active inverted dimmer' id = 'overlay-div-"+data+"'><div class='ui text loader'>Loading</div></div>";
        return over
    }


    function after_event(result, intext){
        if(result == 'success')
            var symbol = "check";
        else
            var symbol = "info";
        var afterhtml = "<div class='col-md-8'><div class='alert alert-"+result+" alert-dismissible'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button><h4><i class='icon fa fa-"+symbol+"'></i> Success !</h4><p>"+intext+"</p></div></div>";
        return afterhtml;
    }



    $('.accept').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        // console.log('hey there'+data);
        div = $('#leave-request-'+data);
        body = $('#leave-request-body-'+data);
        title = $('#leave-request-title-'+data);
        body.append(overlay(data));
        over = $('#overlay-div-'+data);
        // alert('#leave-request-'+data);
        text = $('#remark-'+data);
        req_count = $('#processed-count');
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'accept',
                remark: text.val(),
            },
            success: function(data){
                div.slideToggle();
                title.slideToggle();
                req_count.html((parseInt(req_count.html())-1));
                successNotif("Successfully accepted the request !");
            },
            error: function(data, err){
                over.remove();
                alert("An Error occured while processing request !");
                // infoNotif("An Error occured while processing request !");
                //TODO: add modal for error
            },
        });
    });
    // ERROR

    $('.reject').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        // console.log('hey there'+data);
        div = $('#leave-request-'+data);
        body = $('#leave-request-body-'+data);
        title = $('#leave-request-title-'+data);
        body.append(overlay(data));
        over = $('#overlay-div-'+data);
        // alert('#leave-request-'+data);
        text = $('#remark-'+data);
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'reject',
                remark: text.val(),
            },
            success: function(data){
                div.slideToggle();
                title.slideToggle();
                successNotif("Successfully rejected the request !");
            },
            error: function(data, err){
                over.remove();
                alert("An Error occured while processing request !");
                // infoNotif("An Error occured while processing request !");
                //TODO: add modal for error
            },
        });
    });

    $('.forward').click(function(e){
        // e.preventDefault();
        data = $(this).attr('data');
        // console.log('hey there'+data);
        div = $('#leave-request-'+data);
        body = $('#leave-request-body-'+data);
        title = $('#leave-request-title-'+data);
        body.append(overlay(data));
        over = $('#overlay-div-'+data);
        // alert('#leave-request-'+data);
        text = $('#remark-'+data);
        req_count = $('#processed-count');
        $.ajax({
            type: 'get',
            url: '/leave/process-request/'+data,
            data: {
                do: 'forward',
                remark: text.val(),
            },
            success: function(data){
                div.slideToggle();
                title.slideToggle();
                req_count.html((parseInt(req_count.html())-1));
                successNotif("Successfully forwarded the request !");
            },
            error: function(data, err){
                over.remove();
                alert("An Error occured while processing request !");
                // infoNotif("An Error occured while processing request !");
                //TODO: add modal for error
            },
        });
    });

});
