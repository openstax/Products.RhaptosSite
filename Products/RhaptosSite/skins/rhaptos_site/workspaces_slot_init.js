//// workspaces_slot_init.js - initialize dynamic behaviors of workspaces_slot
// initializes twisties, so that they only appear when JS runs

// like RhaptosContent's toggler.js... but not entirely satisfactory. I'd rather
// have it set up so that with no JS you get expanded-always and no arrows, less duplication of code,
// and probably also no server-side rendering. But that's a different effort. TODO.

function workspaces_slot_init() {
  var eltinfo = twistyRead();
  if (!eltinfo.cnx_by_location) { setupTwisty('cnx_by_location'); }
  if (!eltinfo.cnx_by_type) { setupTwisty('cnx_by_type'); }
}
registerPloneFunction(workspaces_slot_init);

function setupTwisty(id) {
  var eltcontents = document.getElementById(id + '_contents');
  // don't fail if missing elements, in case this gets called too broadly
  if (eltcontents) {
    // default to open; template starts with relevant stuff open and untwistable
    document.getElementById(id + '_expand').style.display = 'inline';
    document.getElementById(id + '_collapse').style.display = 'none';
    eltcontents.style.display = 'block';
    twistyWrite(id, eltcontents.style.display);
  }
}