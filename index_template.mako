## -*- coding: utf-8 -*-

<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" href="../../css/default.css" type="text/css" />

<style type='text/css'>
span {
  color:#FFFFFF;
}
</style>
<!--
<style type='text/css'>
th, td {
  padding: 3px !important;
}


/* Sortable tables */
table.sortable thead {
    background-color:#333;
    color:#666666;
    font-weight: bold;
    cursor: default;
}
th {
  font-size: 100%;
}
</style>
-->

<script src="../../js/sorttable.js"></script>


</head>
<body>

<script type="text/javascript">

function highlight(container,what,spanClass) {
    var content = container.innerHTML,
        pattern = new RegExp('(>[^<.]*)(' + what + ')([^<.]*)','g'),
        replaceWith = '$1<span ' + ( spanClass ? 'class="' + spanClass + '"' : '' ) + '">$2</span>$3',
        highlighted = content.replace(pattern,replaceWith);
    return (container.innerHTML = highlighted) !== content;
}

function filter2(phrase, _id){
	var words = phrase.value.toLowerCase().split(" ");
	var table = document.getElementById(_id);
	var ele;
	for (var r = 1; r < table.rows.length; r++){
		ele = table.rows[r].innerHTML.replace(/<[^>]+>/g,"");
	        var displayStyle = 'none';
	        for (var i = 0; i < words.length; i++) {
		    if (ele.toLowerCase().indexOf(words[i])>=0) {
			displayStyle = '';
			//highlight(ele,words[i],'myspan');
		    } else {
			displayStyle = 'none';
			break;
		    }
	        }
		table.rows[r].style.display = displayStyle;
	}
}



/*
var $rows = $('#table tr');
$('#filt').keyup(function() {
    var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();
    
    $rows.show().filter(function() {
        var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
        return !~text.indexOf(val);
    }).hide();
});
*/

</script>

<input id='filt' name='filt' onkeyup="filter2(this, 'table')"></br>

<table id='table' class='sortable CSSTableGenerator'>
    <caption>lazystudent</caption>
    
    % for row in data:
	% if loop.index is 0:
	  ${makehead(row)}
	%endif
        ${makerow(row)}
    % endfor
</table>


<%def  name="makehead(row)">
  
  <tr>
  
  % for name,val in row.items():    
      <th>${name}</th>
  % endfor
  
  </tr>
  
</%def>

    
    
<%def name="makerow(row)">
    
    <tr>
      
    % for name,val in row.items():
        <td class='${name}'> ${val}</td>
    % endfor
    </tr>
</%def>

</body>
</html>
