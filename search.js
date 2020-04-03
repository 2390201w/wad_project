$('.search-text').on('input', function() {
	search();
	});

function search() {
	var List = $('.search-land ul');
	var params = {};
	var SEARCH_KEY = $('.search-text').val()
	params['action'] = 'get_search_key_list';
	params['market_iid'] = 1001;
	params['search_type'] = TYPE;
	params['search_key'] = nosymble(SEARCH_KEY);
	 
	epm.ajax(params, function(result) {
	console.log(result);
	console.log(TYPE)
	var html = '';
	List.html('');
	if(result.data.length > 0) {
	 $.each(result.data, function(index, value) {
	 goodName = value['goods_name'];
	 shopName = value['shop_name'];
	 itemName = (goodName) ? goodName : shopName;
	 html += '<li class="goods-list">' + itemName + '</li>'
	 });
	 $('.search-list').html(html);
	}
	else {
	 html = '<div class="no-goods">cannot find this game...</div>';
	 $('.search-list').html(html);
	}
	});
}

//delete some not important symble
function nosymble(str) {
	var reg;
	var illegal_list = ["/", "\\","[", "]","{", "}",
	"<", ">","＜", "＞","「", "」","：", "；
	","、", "•","^", "'", "\"","\r", "\r\n", "\\n", "\n"];
	for (var i = 0; i < illegal_list.length; i++) {
	if (str.indexOf(illegal_list[i]) >= 0) {
	if (illegal_list[i] == '\\' || illegal_list[i] == '[') {
	reg = new RegExp('\\' + illegal_list[i], "g");
	} else {
	reg = new RegExp(illegal_list[i], "g");
	}
	str = str.replace(reg, '');
	}
	}
	return str.trim();
   }