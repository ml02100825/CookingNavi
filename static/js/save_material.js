
$(document).ready(function() {
    $('#materialbutton').click(function() {
        var material = $('#materialselect').val();
        var selectedOption = $('#materialselect option:selected');
        material =  parseInt(material, 10);
        console.log("マテリアル：",material)
        console.log(typeof material);
        var materialamount =  $('#materialamount').val();
        materialamount =  parseInt(materialamount, 10);
        var materialname = selectedOption.data('id');
        console.log(materialname);

        if (!isNaN(material) && material !== 0) {
            var url = '/administrator/recipe/add/' + material + '/' + materialamount + '/'
            console.log(material);
            $.ajax({
               
                url:  url,
                type: 'GET',
                dataType: 'json',
              
                success: function(data) {
                    console.log('Material name inside AJAX success:', material);
                    console.log(data);
                    console.log(data[material]);
                    $('#materials').append("<span id ="+ material +">" +materialname +"   " + materialamount +" グラム </span>" + " <button type='button' class='materialdelete'id ="+materialamount+ " name="+material+"  data-id="+  materialname   +">削除</button>");
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