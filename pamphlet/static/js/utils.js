function loadUserAvatar(img_element){
    var user_id = $(img_element).attr('value')
    $.ajax({
        type:'GET',
        url:"/api/get-user-avatar/"+user_id,
        success:function(data){
            //console.log(data)
            $(img_element).attr('src',data.url)
        },
        error:function(result){
            console.log(result.responseText)
        }
    })
}

function loadStatusAvatar(container){
    container.find('.avatar-icon').each(function(){
        loadUserAvatar(this)
    })
}

function display_data_on_container_by_template(data,contianer_id,template_id){
    data_dict ={result:data}
    console.log(data_dict)
    var tpl = $(`#${template_id}`).html()
    var template = Handlebars.compile(tpl)
    var html = template(data_dict)
    $(`#${contianer_id}`).html(html)
}