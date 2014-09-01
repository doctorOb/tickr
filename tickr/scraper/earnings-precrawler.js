var page = require('webpage').create();
var fs = require('fs');
var url = "http://apps.cnbc.com/view.asp?uid=stocks/financials&view=balanceSheet&symbol=GLW"

page.open(url, function (status) {

	
	var yearly = page.evaluate(function(){
		return document.getElementById('containerYr').innerText;
	});

	var quaterly = page.evaluate(function(){
		return document.getElementById('containerQtr').innerText;
	})

	console.log(disclaimer);
	fs.write("earnings/GLW - yr.txt", yearly, 'w');
	fs.write("earnings/GLW - qtr.txt", quaterly, 'w');
	phantom.exit()
});