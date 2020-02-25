$(function() {
    $('#upload-file-btn').click(function() {
        let form_data = new FormData($('#upload-file')[0]);
        let ins = document.getElementById('file').files.length;
        if(ins === 0) {
					$('#fl-message').html(
					    '<div class="alert alert-warning alert-dismissible" role="alert">' +
                        '        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
                        '        Не выбран ни один файл.</div>');
					return;
				}
        $.ajax({
            type: 'POST',
            url: '/convert-xls', // point to server-side URL
            dataType: 'html', // what to expect back from server
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(response) {
                $('#fl-message').html(
                    '<div class="alert alert-success alert-dismissible" role="alert">' +
                    '        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
                    '        Файл успешно сконвертирован.</div>');
            //         let json = jQuery.parseJSON(response);
            //         $('#fl-message').html(json.message);
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            // success: function(data) {
            //     console.log('Success!');
            //     if (data.redirect) {
                    // if( data.load_html) {
                    // data.redirect contains the string URL to redirect to
                    // window.location.href = data.redirect;

                    // window.location.replace(data.redirect);

                    // $("#conv-result").text(data.result);
                // } else {

                    // data.form contains the HTML for the replacement form
                    // $("#my_form").replaceWith(data.form);

                // }

            // },
        });
    });
});
