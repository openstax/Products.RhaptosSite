
/********* Table sorter script *************/
// Table sorter script, thanks to Geir Bækholt for this.
// DOM table sorter originally made by Paul Sowden

/*
  Rhaptos overrides
    make initalizeTableSort() check the URL params for 'sort' and use that to init the sorted column.
*/

function compare(a,b)
{
    au = new String(a);
    bu = new String(b);

    if (au.charAt(4) != '-' && au.charAt(7) != '-')
    {
    var an = parseFloat(au)
    var bn = parseFloat(bu)
    }
    if (isNaN(an) || isNaN(bn))
        {as = au.toLowerCase()
         bs = bu.toLowerCase()
        if (as > bs)
            {return 1;}
        else
            {return -1;}
        }
    else {
    return an - bn;
    }
}
function getConcatenedTextContent(node) {
    var _result = "";
      if (node == null) {
            return _result;
      }
    var childrens = node.childNodes;
    var i = 0;
    while (i < childrens.length) {
        var child = childrens.item(i);
        switch (child.nodeType) {
            case 1: // ELEMENT_NODE
            case 5: // ENTITY_REFERENCE_NODE
                _result += getConcatenedTextContent(child);
                break;
            case 3: // TEXT_NODE
            case 2: // ATTRIBUTE_NODE
            case 4: // CDATA_SECTION_NODE
                _result += child.nodeValue;
                break;
            case 6: // ENTITY_NODE
            case 7: // PROCESSING_INSTRUCTION_NODE
            case 8: // COMMENT_NODE
            case 9: // DOCUMENT_NODE
            case 10: // DOCUMENT_TYPE_NODE
            case 11: // DOCUMENT_FRAGMENT_NODE
            case 12: // NOTATION_NODE
                // skip
                break;
        }
        i ++;
    }
    return _result;
}

function sort(e) {
    var el = window.event ? window.event.srcElement : e.currentTarget;

    // a pretty ugly sort function, but it works nonetheless
    var a = new Array();
    // check if the image or the th is clicked. Proceed to parent id it is the image
    // NOTE THAT nodeName IS UPPERCASE
    if (el.nodeName == 'IMG') el = el.parentNode;
    //var name = el.firstChild.nodeValue;
    // This is not very robust, it assumes there is an image as first node then text
    var name = el.childNodes.item(1).nodeValue;
    var dad = el.parentNode;
    var node;

    // kill all arrows
    for (var im = 0; (node = dad.getElementsByTagName("th").item(im)); im++) {
        // NOTE THAT nodeName IS IN UPPERCASE
        if (node.lastChild.nodeName == 'IMG')
        {
            lastindex = node.getElementsByTagName('img').length - 1;
            node.getElementsByTagName('img').item(lastindex).setAttribute('src',portal_url + '/arrowBlank.gif');
        }
    }

    for (var i = 0; (node = dad.getElementsByTagName("th").item(i)); i++) {
        var xre = new RegExp(/\bnosort\b/);
        // Make sure we are not messing with nosortable columns, then check second node.
        if (!xre.exec(node.className) && node.childNodes.item(1).nodeValue == name) 
        {
            //window.alert(node.childNodes.item(1).nodeValue;
            lastindex = node.getElementsByTagName('img').length -1;
            node.getElementsByTagName('img').item(lastindex).setAttribute('src',portal_url + '/arrowUp.gif');
            break;
        }
    }

    var tbody = dad.parentNode.parentNode.getElementsByTagName("tbody").item(0);
    for (var j = 0; (node = tbody.getElementsByTagName("tr").item(j)); j++) {

        // crude way to sort by surname and name after first choice
        a[j] = new Array();
        a[j][0] = getConcatenedTextContent(node.getElementsByTagName("td").item(i));
        a[j][1] = getConcatenedTextContent(node.getElementsByTagName("td").item(1));
        a[j][2] = getConcatenedTextContent(node.getElementsByTagName("td").item(0));        
        a[j][3] = node;
    }

    if (a.length > 1) {

        a.sort(compare);

        // not a perfect way to check, but hell, it suits me fine
        if (a[0][0] == getConcatenedTextContent(tbody.getElementsByTagName("tr").item(0).getElementsByTagName("td").item(i))
           && a[1][0] == getConcatenedTextContent(tbody.getElementsByTagName("tr").item(1).getElementsByTagName("td").item(i))) 
        {
            a.reverse();
            lastindex = el.getElementsByTagName('img').length - 1;
            el.getElementsByTagName('img').item(lastindex).setAttribute('src', portal_url + '/arrowDown.gif');
        }

    }

    for (var j = 0; j < a.length; j++) {
        a[j][3].className = ((j % 2) == 0) ? 'odd' : 'even';
        tbody.appendChild(a[j][3]);
    }
}

function initalizeTableSort(e) {
    // terminate if we hit a non-compliant DOM implementation
    if (!W3CDOM){return false};

    var tbls = document.getElementsByTagName('table');
    for (var t = 0; t < tbls.length; t++)
        {
        // elements of class="listing" can be sorted
        var re = new RegExp(/\blisting\b/)
        // elements of class="nosort" should not be sorted
        var xre = new RegExp(/\bnosort\b/)
        if (re.exec(tbls[t].className) && !xre.exec(tbls[t].className))
        {
            try {
                var thead = tbls[t].getElementsByTagName("thead").item(0);
                var node;
                // set up blank spaceholder gifs
                blankarrow = document.createElement('img');
                blankarrow.setAttribute('src', portal_url + '/arrowBlank.gif');
                blankarrow.setAttribute('height',6);
                blankarrow.setAttribute('width',9);
                // the first sortable column should get an arrow initially.
                initialsort = false;
                for (var i = 0; (node = thead.getElementsByTagName("th").item(i)); i++) {
                    // check that the columns does not have class="nosort"
                    if (!xre.exec(node.className)) {
                        node.insertBefore(blankarrow.cloneNode(1), node.firstChild);
                        node.style.cursor = 'pointer';
                        if (!initialsort) {
                            initialsort = true;
                            uparrow = document.createElement('img');
                            uparrow.setAttribute('src', portal_url + '/arrowUp.gif');
                            uparrow.setAttribute('height',6);
                            uparrow.setAttribute('width',9);
                            node.appendChild(uparrow);
                        } else {
                            node.appendChild(blankarrow.cloneNode(1));
                        }

                        if (node.addEventListener) node.addEventListener("click",sort,false);
                        else if (node.attachEvent) node.attachEvent("onclick",sort);
                    }
                }
                selectSortColumnFromUrl(tbls[t]);
            } catch(er) {}
        }
    }
}

// Get URL Parameters Using Javascript, Published Aug 17, 2006
// http://www.netlobo.com/url_query_string_javascript.html
function getUrlParameter( name )
{
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}

function endsWith(strFull, strEnd) {
    var delta;
    delta = strFull.length - strEnd.length;
    return ( delta >= 0 && strFull.lastIndexOf(strEnd) == delta );
}

//
// previously we had assumed that the title column (with sort key 'sortable_title')
// was the only sort index used.  we added the below function to handle when this is
// not the case.
//
// the url contains the sort index used to generate the results, except when the sort
// key is the default, sortable_title. in the default case, there is no need to fix the table.
//
// the column header (html <th> node) now has an @id which ends with its sort key.  since
// initalizeTableSort() and sort() are built to handle multiple tables per page, the th @id
// may not simply be the sort key.  thus when there are multiple table the th @id must have a
// prefix before the sort key, tokeep the @ids unique.
//
function selectSortColumnFromUrl(nodeTable) {
    var strColumnId;
    var strSortOrder;
    var nodesTHead;
    var nodeTHead;
    var nodesTH;
    var nodeTH;
    var strId;
    var nodesImg;
    var nodeImg;
    var nodeLastImg;
    var strLastImageUrl;
    var iLast;
    var i;
    var j;
    var k;
    var nodeBlankArrow;
    var nodeArrow;

    strColumnId = getUrlParameter('sort');

    if ( strColumnId && strColumnId.length > 0 ) {
        strSortOrder = getUrlParameter('sort_order');
        if ( strSortOrder && strSortOrder.length == 0 ) strSortOrder = 'ascending';

        nodesTHead = nodeTable.getElementsByTagName("thead");
        if ( nodesTHead && nodesTHead.length && nodesTHead.length > 0 ) {
            nodeTHead = nodesTHead.item(0);
            if ( nodeTHead ) {
                nodesTH = nodeTHead.getElementsByTagName("th");
                if ( nodesTH && nodesTH.length && nodesTH.length > 0 ) {
                    for (i=0; i<nodesTH.length; i++) {
                        nodeTH = nodesTH[i];
                        strId = nodeTH.getAttribute('id');
                        if ( strId && endsWith(strId, strColumnId) ) {
                            //
                            // url parameter matches a table column id
                            // check to see if the correct column is marked
                            //
                            nodesImg = nodeTH.getElementsByTagName('img');
                            if ( nodesImg && nodesImg.length && nodesImg.length > 0 ) {
                                iLast = nodesImg.length - 1;
                                nodeLastImg = nodesImg.item(iLast);
                                strLastImageUrl = nodeLastImg.getAttribute('src');
                                // note portal_url is globally defined
                                if ( strLastImageUrl == portal_url +'/arrowBlank.gif' ) {
                                    //
                                    // arrow is blank but we want it not to be
                                    // mark this column as the sort coulmn and reset the rest
                                    //
                                    nodeBlankArrow = document.createElement('img');
                                    nodeBlankArrow.setAttribute('src', portal_url + '/arrowBlank.gif');
                                    nodeBlankArrow.setAttribute('height',6);
                                    nodeBlankArrow.setAttribute('width',9);
                                    for (j=0; j<nodesTH.length; j++) {
                                        nodeTH = nodesTH[j];
                                        nodesImg = nodeTH.getElementsByTagName('img');
                                        if ( i == j ) {
                                            for (k=0; k<nodesImg.length-1; k++) {
                                                nodeImg = nodesImg[k];
                                                nodeTH.insertBefore(nodeBlankArrow.cloneNode(1), nodeImg);
                                                nodeTH.removeChild(nodeImg);
                                            }
                                            nodeLastImg = nodesImg[k];
                                            nodeArrow = document.createElement('img');
                                            if ( strSortOrder == 'ascending' ) {
                                                nodeArrow.setAttribute('src', portal_url + '/arrowUp.gif');
                                            }
                                            else {
                                                nodeArrow.setAttribute('src', portal_url + '/arrowDown.gif');
                                            }
                                            nodeArrow.setAttribute('height',6);
                                            nodeArrow.setAttribute('width',9);
                                            nodeTH.insertBefore(nodeArrow, nodeLastImg);
                                            nodeTH.removeChild(nodeLastImg);
                                        }
                                        else {
                                            for (k=0; k<nodesImg.length; k++) {
                                                nodeImg = nodesImg[k];
                                                nodeTH.insertBefore(nodeBlankArrow.cloneNode(1), nodeImg);
                                                nodeTH.removeChild(nodeImg);
                                            }
                                        }
                                    }
                                }
                            }
                            //
                            // our work here is done
                            //
                            break;
                        }
                    }
                }
            }
        }
    }
}

// **** End table sort script ***
registerPloneFunction(initalizeTableSort)   

