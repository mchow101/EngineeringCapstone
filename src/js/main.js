var links = {
    "index": "index.html"
};

var page = document.URL.substring(document.URL.lastIndexOf('#') + 1);
if (page.length === 0 || document.URL.lastIndexOf('#') === -1) {
    page = "index";
}

var contents;
setpage(page);
function setpage(curpage) {
    page = curpage;
    getFile(links[page]);
}

function getFile(file) {
    $(document).ready(function () {

        $('#content').load(file);

    });
}