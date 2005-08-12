var roundedCornersOnLoad = function () {
    swapDOM("visual_version", SPAN(null, MochiKit.Visual.VERSION));
    roundClass("h1", null);
    roundClass("h2", null, {corners: "bottom"});
    syntaxHighlight();
};

var swapContents = function (dest, req) {
    replaceChildNodes(dest, req.responseText);
};

var finishSyntaxHighlight = function () {
    dp.sh.HighlightAll("code");
    removeElementClass("codeview", "invisible");
};

var syntaxHighlight = function () {
    var elems = getElementsByTagAndClassName("textarea", null, "codeview");
    var dl = new Deferred();
    var deferredCount = 0;
    var checkDeferredList = function () {
        deferredCount -= 1;
        if (!deferredCount) {
            dl.callback();
        }
    };
    for (var i = 0; i < elems.length; i++) {
        var elem = elems[i];
        if (elem.name != "code") {
            continue;
        }
        var url = strip(scrapeText(elem))
        var d = doSimpleXMLHttpRequest(url).addCallback(
            partial(swapContents, elem)
        );
        deferredCount += 1;
        d.addCallback(checkDeferredList);
    }
    dl.addCallback(finishSyntaxHighlight);
};
