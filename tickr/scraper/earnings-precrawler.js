var page = require('webpage').create();
var fs = require('fs');
var url = "http://apps.cnbc.com/view.asp?uid=stocks/financials&view=balanceSheet&symbol=GLW"

page.open(url, function (status) {
	fs.write("../data/earnings/GLW.html", page.content, 'w');
	phantom.exit()
});