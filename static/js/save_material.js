
$(document).ready(function() {
    $('#materialbutton').click(function() {
        var material = $('#materialselect').val();
        material =  parseInt(material, 10);
        console.log("マテリアル：",material)
        console.log(typeof material);
        if (!isNaN(material) && material !== 0) {
            var url = '/administrator/recipe/add/' + material + '/'
            console.log(material);
            $.ajax({
               
                url:  url,
                type: 'GET',
                dataType: 'json',
              
                success: function(data) {
                    console.log('Material name inside AJAX success:', material);
                    console.log(data[0]['name']);
                    $('#materials').append("<span id ="+ data[0]['material_id']+">"+data[0]['name']+"</span>" + " <button type='button' class='materialdelete' name="+data[0]['material_id']+">削除</button>");
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