$(function() {
    $('#upload-file-btn').click(function() {
        let form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/convert-xls',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                console.log('Success!');
                if (data.redirect) {
                    // if( data.load_html) {
                    // data.redirect contains the string URL to redirect to
                    // window.location.href = data.redirect;

                    window.location.replace(data.redirect);
                // } else {

                    // data.form contains the HTML for the replacement form
                    // $("#my_form").replaceWith(data.form);

                }
            },
        });
    });
});
