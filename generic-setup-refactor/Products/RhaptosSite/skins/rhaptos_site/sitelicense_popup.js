// create the lens addition popup application (single instance)
var SiteLicense = function(){
    // define some private variables
    var title, body, showBtn, dialogUpdater;

    var dialogheight = 300;
    var dialogwidth = 500;

    // return a public interface
    return {
        init : function(){
             var dialog = Ext.get("sitelicense_dlg");
             title = dialog.first().dom.innerHTML;
             body = dialog.last().removeClass('x-dlg-bd').dom;
             //detach the license
             dialog.dom.parentNode.removeChild(dialog.dom);

             showBtn = Ext.get('sitelicense_link');
             // attach to click event
             if (showBtn) {
                showBtn.on('click', this.showDialog, this, {stopEvent : true});
             }
        },
        showDialog : function(){
            var dialog = new Ext.Window({ 
                        title:title,
                        contentEl:body,
                        draggable:true,
                		autoHeight:false,
                		autoScroll:true,
                        closable:true,
                        collapsible:false,
                        width:dialogwidth,
                        height:dialogheight,
                        minWidth:300,
                        minHeight:250
                });

            dialog.show(showBtn.dom);
        }
    };
}();

// using onDocumentReady instead of window.onload initializes the application
// when the DOM is ready, without waiting for images and other resources to load
Ext.onReady(SiteLicense.init, SiteLicense, true);
