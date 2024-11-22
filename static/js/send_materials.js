
$(document).ready(function() {
    $('#material-input').on('input', function() {
        var materialname = $(this).val();
        if (materialname) {
            var url = '/administrator/recipe/add/' + materialname + '/'
            console.log(materialname);
            $.ajax({
               
                url:  url,
                type: 'GET',
                dataType: 'json',
              
                success: function(data) {
                    console.log('Material name inside AJAX success:', materialname);
                    console.log(data);
                
                    $('#materialselect').empty();
                    $('#materialselect').append('<option value="">選択してください</option>');
                    $.each(data, function(key, value) {
                       
                        $('#materialselect').append('<option data-id='+ value.name  +" value=" + value.material_id + ">" + value.name + '</option>');
                    });
                },
                error: function(xhr, status, error) {
                    console.log("AJAXエラー:", error);
                    console.log("ステータス:", status);
                    console.log("レスポンス:", xhr.responseText);
                }
            });
        } else {
            $('#materialname-input').empty();
            $('#materialname-input').append('<input type="text">入力してください</input>');
        }
    });
});