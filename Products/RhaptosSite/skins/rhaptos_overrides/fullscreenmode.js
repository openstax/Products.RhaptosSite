/*
Rhaptos changes:
  - added path parameter to toggleFullScreenMode() so that path cookies
    can be created
  - changed fullscreenModeLoad() and toggleFullScreenMode() so that pages 
    lacking an expansion icon will not expand on page load (with then no
    way to unexpand)
  - changed the expander tooltip, which is state dependent
  - added text to go with the expander widgit, which is state dependent
*/

function toggleFullScreenMode(path) {
    var body = cssQuery('body')[0];
    if(document.getElementById('icon-full_screen')) {
        var fsicon      = document.getElementById('icon-full_screen');
        var fsicon_link = document.getElementById('link-full_screen');
        var fsicon_text = document.getElementById('text-full_screen');
        if (hasClassName(body, 'fullscreen')) {
            // unset cookie
            removeClassName(body, 'fullscreen');
            createCookie('fullscreenMode', '', 365, path);
            if (fsicon) {
                fsicon.src = 'fullscreenexpand_icon.gif';
            }
            if (fsicon_link) {
                fsicon_link.setAttribute('title', 'Click this to expand the editing area. Click again to return to normal view.');
            }
            if (fsicon_text) {
                fsicon_text.innerHTML = "Hide sidebars";
            }
        } else {
            // set cookie
            addClassName(body, 'fullscreen');
            createCookie('fullscreenMode', '1', 365, path);
            if (fsicon) {
                fsicon.src = 'fullscreencollapse_icon.gif';
            }
            if (fsicon_link) {
                fsicon_link.setAttribute('title', 'Click this to return to normal view.');
            }
            if (fsicon_text) {
                fsicon_text.innerHTML = "Show sidebars";
            }
        }
    }
};

function fullscreenModeLoad() {
    if(document.getElementById('icon-full_screen')) {
        var fsicon           = document.getElementById('icon-full_screen');
        var fsicon_link      = document.getElementById('link-full_screen');
        var fsicon_text      = document.getElementById('text-full_screen');
        var fsicon_container = document.getElementById('container-full_screen');
        if (fsicon_container) {
            fsicon_container.style.display = '';
        }
        // based on cookie
        if (readCookie('fullscreenMode') == '1') {
            var body = cssQuery('body')[0];
            addClassName(body, 'fullscreen');
            if (fsicon) {
                fsicon.src = 'fullscreencollapse_icon.gif';
            }
            if (fsicon_link) {
                fsicon_link.setAttribute('title', 'Click this to return to normal view.');
            }
            if (fsicon_text) {
                fsicon_text.innerHTML = "Show sidebars";
            }
        }
    }
};
registerPloneFunction(fullscreenModeLoad);
