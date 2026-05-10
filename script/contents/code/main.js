function adjust_overlay(is_active, geometry) {
    callDBus("com.qlcd.OverlayService", "/", "com.qlcd.OverlayService.ipc", "adjust_window", is_active, geometry.x, geometry.y, geometry.width, geometry.height)
}

function connect_window(window){
    adjust_overlay(window.active, window.clientGeometry)
    window.clientGeometryChanged.connect(function(old_geometry) {
        adjust_overlay(window.active, window.clientGeometry);
    });
}

workspace.windowAdded.connect(function(window) {
    if (window.resourceName === "osu!.exe" || window.resourceName === "osu!") {
        adjust_overlay(window.active, window.clientGeometry);
    }
});

workspace.windowActivated.connect(function(window) {
    console.info("detected window change");
    if (window.resourceName === "osu!.exe" || window.resourceName === "osu!") {
        adjust_overlay(window.active, window.clientGeometry);
    }
    else {
        adjust_overlay(0, window.clientGeometry);
    }
});

for (let window of workspace.windowList()) {
    if (window.resourceName === "osu!.exe" || window.resourceName === "osu!") {
        connect_window(window);
    }
}
// KWin Script used to read osu window status (and some other stuff)