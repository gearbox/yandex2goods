$(function() {
    $('#upload-file-btn').click(function() {
        let form_data = new FormData($('#upload-file')[0]);
        let ins = document.getElementById('file').files.length;
        if(ins === 0) {
					$('#status-message').html(
					    '<div class="alert alert-warning alert-dismissible" role="alert">' +
                        '        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' +
                        '        Не выбран ни один файл.</div>');
					return;
				}
        $.ajax({
            type: 'POST',
            url: '/convert-xls', // point to server-side URL
            dataType: 'json', // what to expect back from server
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(response) {
                $('#status-message').html(
                    '<div class="alert alert-' + response.type + ' alert-dismissible" role="alert">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span></button>' +
                    response.message + '</div>'
                );
                $.each(response, function (key, data) {
                    if (data === 'success') {
                        $('#conv-result').html('<h3>XML для Goods.ru:</h3>');
                        $('#download-links').append(
                            '<a href="' + response.link + '">Скачать ' + response.filename + '</a><br/>'
                        );
                        // $('#download-links a').each(
                            // function () {
                                // let links = this.attr('href');
                                // for (let i = 0, len = links.length; i < len; i++) {
                                //     if (location.href.search(this.attr('href')) !== $('a').attr('href')) {
                                //         $('#download-links').append(
                                //             '<a href="' + response.link + '">Скачать ' + response.filename + '</a><br/>'
                                //         );
                                //     }
                                // }
                            // })
                    }
                });
                console.log(response);
                },
            error: function(error) {
                $('#status-message').html(
                    '<div class="alert alert-' + error.responseText.type + ' alert-dismissible" role="alert">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                    '<span aria-hidden="true">&times;</span></button>' +
                    error.responseText.message + '</div>'
                );
                console.log(error);
            }
        });
    });
});
