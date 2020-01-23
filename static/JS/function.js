function loading(t){
    if(t == 1){
        $.messager.progress({
                        title:'处理中.',
                        msg:'请稍候...'
                    });
    }else{
        $.messager.progress('close');
    }
}
