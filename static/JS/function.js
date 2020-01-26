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

//增加 datagrid 一条记录
//传入2个参数，ID句柄和数据
function addRow(dg, data) {
    $('#'+ dg).datagrid('insertRow', {
        index: 0,	// 索引从0开始
        row: data
    });
}

//更新 datagrid 选中的那条记录
//传入2个参数，ID句柄和数据
function updateRow(dg, data) {
    console.log('edit', data)
    let row = $('#' + dg).datagrid('getSelected');
    let rowIndex = $('#' + dg).datagrid('getRowIndex', row);
    $('#' + dg).datagrid('updateRow',{
        index: rowIndex,
        row: data
    });
}

//删除 datagrid 选中的记录(所有选中的记录)
//传入1个参数，ID
function deleteRow(dg) {
    let tmp_row = $('#' + dg).datagrid('getSelected');
    let rowIndex = $('#'+ dg).datagrid('getRowIndex', tmp_row);
    $('#'+ dg).datagrid('deleteRow', rowIndex);
}

//弹出指定的 dialog 并修改其标题
function showDialog(div, title) {
    $('#'+ div).dialog({
        title: title,
        cache: false,
        modal: true
    });
}

//清除某ID下面所有文本框
function clearInput(divid)
{
	$("#"+divid+" :input").not(":button, :submit, :reset, :hidden").val("").removeAttr("checked").remove("selected");
}