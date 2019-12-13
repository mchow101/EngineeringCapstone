'use strict';

const express = require('express');
const app = express();
const fs = require("fs");
const path = require('path');
app.use(express.static('src'));
const https = require('https');

//Pages
app.get('/', (req, res) => {
	getPage('/src/pages/index.html', function (a) {
		res.send(a);
	}, false);
});

app.get('/contact', (req, res) => {
	getPage('/src/pages/contact.html', function (a) {
		res.send(a);
	}, false);
});

app.get('/swarm', (req, res) => {
	getPage('/src/pages/swarm_robotics.html', function (a) {
		res.send(a);
	}, false);
});

//404
app.get('*', (req, res) => {
	getPage('/src/pages/404.html', function (a) {
		res.send(a);
	}, false);
});

//Page Functions
function getPage(dir, callback, addDefaultWrapper, lph) {
	fs.readFile(path.join(__dirname, dir), 'utf8', function (err, data) {
		if (err) { console.error(err); return; }

		function r(f, t) {
			while (data.indexOf('${' + f + '}') != -1) {
				data = data.replace('${' + f + '}', t);
			}
		}

		r('lph', (lph || ""));
		
		if (addDefaultWrapper) {
			addDefaultPage(data, function (parsedPage) {
				callback(parsedPage);
			});
		}
		else callback(data);
		
	});
/*
	function addDefaultPage(data, callback) {
		function ds(a) {
			var s = data.lastIndexOf(`<${a}>`);
			var e = data.lastIndexOf(`</${a}>`);
			if (s != -1 && e != -1) {
				var r = data.substring(s + a.length + 2, e);
				data = data.slice(0, s) + data.slice(e + a.length + 3);
				return r;
			}
			else return;
		}

		function dsm(a, lnb, lne) {
			var ret = "";
			var r = true;
			while (r) {
				var n = ds(a);
				if (n)
					ret += (lnb + n + lne);
				else
					r = false;
			}
			return ret;
		}

		var pageTitle = ds('title');
		if (pageTitle == "")
			pageTitle = "Engineering Capstone";
		else
			pageTitle = "Engineering Capstone - " + pageTitle;

		
		var css = dsm(`css`, `<link href="` + '${lph}' + `/resources/css/`, `.css" type="text/css" rel="stylesheet">`);
		css += dsm(`style`, `<style>`, `</style>`);

		var javascript = dsm(`script`);

		fs.readFile(path.join(__dirname, '/src/page.html'), 'utf8', function (err, pageData) {
			if (err) { next(err); return; }

			function r(f, t) {
				while (pageData.indexOf('${' + f + '}') != -1) {
					pageData = pageData.replace('${' + f + '}', t);
				}
			}

			function ah(t) {
				t = t.substring(11);
				while (pageData.indexOf('nav-link">' + t) != -1) {
					pageData = pageData.replace('">' + t, ' active">' + t);
				}
			}
			
			r('content', data);
			r('page-title', pageTitle);
			r('css', css);
			r('javascript', javascript);
			r('lph', (lph || ""));
			ah(pageTitle);
			callback(pageData);
		});
	}
	*/
} 

//Local Serving
if (module === require.main) {
	const server = app.listen(process.env.PORT || 5000, () => {
		const port = server.address().port;
		console.log(`Serving at localhost:${port}`);
	});
}
module.exports = app;