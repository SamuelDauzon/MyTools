
// ----------------------------------------------------------------
// Bookmarklet : navigate +1 answers/question

javascript:(function(){
if (typeof findPos === "undefined") {
function findPos(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        do {
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    return [curtop];
    }
}
}
if (typeof so_qa_elements ==="undefined") {
    so_qa_elements = document.querySelectorAll(".fc-theme-primary");
    so_qa_cursor = 0;
}
if (so_qa_cursor >= so_qa_elements.length) {
    so_qa_cursor = 0;
}
so_qa_element = so_qa_elements[so_qa_cursor];
so_qa_cursor++;
so_qa_position = findPos(so_qa_element);
so_qa_position -= 70;
if (so_qa_position<1) {
    so_qa_position = 1;
}
window.scroll(0, so_qa_position);
})();


// Oneline

javascript:(function(){if (typeof findPos === "undefined") {function findPos(obj) {    var curtop = 0;    if (obj.offsetParent) {        do {            curtop += obj.offsetTop;        } while (obj = obj.offsetParent);    return [curtop];    }}}if (typeof so_qa_elements ==="undefined") {    so_qa_elements = document.querySelectorAll(".fc-theme-primary");    so_qa_cursor = 0;}if (so_qa_cursor >= so_qa_elements.length) {    so_qa_cursor = 0;}so_qa_element = so_qa_elements[so_qa_cursor];so_qa_cursor++;so_qa_position = findPos(so_qa_element);so_qa_position -= 70;if (so_qa_position<1) {    so_qa_position = 1;}window.scroll(0, so_qa_position);})();


// ----------------------------------------------------------------
// Bookmarklet : top list with date answers + navigate them


javascript:(function(){
if (typeof findPos === "undefined") {
function findPos(obj) {
    var curtop = 0;
    if (obj.offsetParent) {
        do {
            curtop += obj.offsetTop;
        } while (obj = obj.offsetParent);
    return [curtop];
    }
}
function collectionHas(a, b) {
    for(var i = 0, len = a.length; i < len; i ++) {
        if(a[i] == b) return true;
    }
    return false;
}
function findParentBySelector(elm, selector) {
    var all = document.querySelectorAll(selector);
    var cur = elm.parentNode;
    while(cur && !collectionHas(all, cur)) {
        cur = cur.parentNode;
    }
    return cur;
}
}
if (typeof so_qa_elements ==="undefined") {
    so_qa_elements_dom = document.querySelectorAll(".js-vote-count");
    so_qa_elements = [];
    for (so_qa_element of so_qa_elements_dom) {
        so_qa_answer = findParentBySelector(so_qa_element, ".answer");
        user_actiontime = "";
        if (so_qa_answer) {
            user_actiontime = so_qa_answer.querySelector(".user-action-time span").getAttribute("title");
        }
        so_qa_elements.push({
            "element": so_qa_element,
            "score": parseInt(so_qa_element.innerHTML.trim(), 10),
            "user_actiontime": user_actiontime,
            "question": false
        });
    }
    so_qa_elements[0].question = true;
    so_qa_elements[0].user_actiontime = "QUESTION";
    so_qa_elements.sort(function(a, b) {
        return a.score < b.score
    });
    so_qa_question = document.querySelector("#question");
    so_qa_question.insertAdjacentHTML("beforeend", `<h2 id="so_qa_resume">RESUME</h2>`);
    for (so_qa_element of so_qa_elements) {
        so_qa_question.insertAdjacentHTML("beforeend", `<br /><strong>`+so_qa_element.score+` : `+so_qa_element.user_actiontime+`</strong>`);
    }
    so_qa_cursor = 0;
    so_qa_position = findPos(document.querySelector("#so_qa_resume"));
    so_qa_position -= 70;
    window.scroll(0, so_qa_position);
}
else {
    if (so_qa_cursor >= so_qa_elements.length) {
        so_qa_cursor = 0;
    }
    so_qa_element = so_qa_elements[so_qa_cursor];
    so_qa_cursor++;
    so_qa_position = findPos(so_qa_element.element);
    so_qa_position -= 70;
    if (so_qa_position<1) {
        so_qa_position = 1;
    }
    window.scroll(0, so_qa_position);
}
})();



javascript:(function(){if (typeof findPos === "undefined") {function findPos(obj) {    var curtop = 0;    if (obj.offsetParent) {        do {            curtop += obj.offsetTop;        } while (obj = obj.offsetParent);    return [curtop];    }}function collectionHas(a, b) {    for(var i = 0, len = a.length; i < len; i ++) {        if(a[i] == b) return true;    }    return false;}function findParentBySelector(elm, selector) {    var all = document.querySelectorAll(selector);    var cur = elm.parentNode;    while(cur && !collectionHas(all, cur)) {        cur = cur.parentNode;    }    return cur;}}if (typeof so_qa_elements ==="undefined") {    so_qa_elements_dom = document.querySelectorAll(".js-vote-count");    so_qa_elements = [];    for (so_qa_element of so_qa_elements_dom) {        so_qa_answer = findParentBySelector(so_qa_element, ".answer");        user_actiontime = "";        if (so_qa_answer) {            user_actiontime = so_qa_answer.querySelector(".user-action-time span").getAttribute("title");        }        so_qa_elements.push({            "element": so_qa_element,            "score": parseInt(so_qa_element.innerHTML.trim(), 10),            "user_actiontime": user_actiontime,            "question": false        });    }    so_qa_elements[0].question = true;    so_qa_elements[0].user_actiontime = "QUESTION";    so_qa_elements.sort(function(a, b) {        return a.score < b.score    });    so_qa_question = document.querySelector("#question");    so_qa_question.insertAdjacentHTML("beforeend", `<h2 id="so_qa_resume">RESUME</h2>`);    for (so_qa_element of so_qa_elements) {        so_qa_question.insertAdjacentHTML("beforeend", `<br /><strong>`+so_qa_element.score+` : `+so_qa_element.user_actiontime+`</strong>`);    }    so_qa_cursor = 0;    so_qa_position = findPos(document.querySelector("#so_qa_resume"));    so_qa_position -= 70;    window.scroll(0, so_qa_position);}else {    if (so_qa_cursor >= so_qa_elements.length) {        so_qa_cursor = 0;    }    so_qa_element = so_qa_elements[so_qa_cursor];    so_qa_cursor++;    so_qa_position = findPos(so_qa_element.element);    so_qa_position -= 70;    if (so_qa_position<1) {        so_qa_position = 1;    }    window.scroll(0, so_qa_position);}})();


