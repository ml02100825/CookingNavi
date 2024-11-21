
$(document).ready(function() {
    $('#materials').on('click','.materialdelete',function() {
        var material = $(this).attr('name');
        var $button = $(this); 
        material =  parseInt(material, 10);
        console.log("delete",material)
        console.log(typeof material);
        if (!isNaN(material) && material !== 0) {
            var url = '/administrator/recipe/add/' + material + '/'
            console.log(material);
            $.ajax({
               
                url:  url,
                type: 'get',
                dataType: 'json',
              
                success: function(data) {
                    console.log('Material name inside AJAX success:', material);
                    console.log(data[0]['name']);
                    // 対応する <span> 要素を削除
                     $('#materials').find('#' + material).remove();

                     // クリックされた <button> 要素を削除
                    $button.remove();               },
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