var count_input_imgs=0;
var img_tags = ['img_1','img_2','img_3','img_4']
changeInputImageLabel()    
console.log(document.querySelector('#file-upload-label'))

console.log(document.querySelector("#file-upload-input"))
$('.file-upload-input').on('change',function(e){
    
    console.log('show img')

    input = e.currentTarget
    src = URL.createObjectURL(input.files[0])
    // img = document.createElement('img')
    // img.setAttribute('src',src)
    // img.setAttribute('class','img-box')
    console.log(src)
    data = {img:src,tag:getCurrentImageLabel()}
    var tpl = $("#single-input-img-box").html()
    var template = Handlebars.compile(tpl)
    var html = template(data)
    if(count_input_imgs <2){
        $('#image-preview-left-column').append(html)
        $('#image-preview-left-column').addClass("full-row-container")
    }else{
        $('#image-preview-left-column').removeClass("full-row-container")

        $('#image-preview-right-column').append(html)
    }
    count_input_imgs+=1
    console.log("add image:"+count_input_imgs)

    $(".delete-image-btn").unbind().on('click',function(e){
        btn = e.currentTarget
        console.log('dbtn click')
        tag = $(btn).closest('.img-box').attr('value')
        $("#"+tag).val("")
        returnTag(tag)
        $(btn).closest('.img-box').remove()
        count_input_imgs-=1
        console.log("delete image:"+count_input_imgs)

        adjust_preview_image_layout()
        if(count_input_imgs==0){
            hidePreviewContainer()
        }
    })
    changeInputImageLabel()
    showPreviewContainer()
})
function showPreviewContainer(){
    $("#image-preview-container").addClass("show-container")
    
}
function hidePreviewContainer(){
    $("#image-preview-container").removeClass("show-container")
}
function adjust_preview_image_layout(){
    console.log('adjust layout')
    var left_container=$('#image-preview-left-column')
    var right_container = $('#image-preview-right-column')
    if(count_input_imgs <=2 ){
        if(right_container.children().length >0){
            right_container.children().each(function(){
                console.log($(this))
                $(this).clone(true).appendTo(left_container)
                $(this).remove()
                console.log("move ++")
            })
        }

        $('#image-preview-left-column').addClass("full-row-container")

    }else{
        $('#image-preview-left-column').removeClass("full-row-container")
    }
}
function returnTag(tag){
    img_tags.push(tag)
}
function changeInputImageLabel(){
    $("#file-upload-label").attr('for',img_tags.pop())
}

function getCurrentImageLabel(){
    return $("#file-upload-label").attr('for')
}