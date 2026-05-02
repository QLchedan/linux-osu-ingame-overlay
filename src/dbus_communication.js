const windows = workspace.windowList();
for (const window of windows) {
    if (window.normalWindow && (window.resourceClass=="osu!.exe" || window.resourceClass=="osu! osu!")) {
        console.info(window.active);
        console.info(window.x);
        console.info(window.y);
        console.info(window.width);
        console.info(window.height);
        console.info(workspace.workspaceWidth);
        console.info(workspace.workspaceHeight);
    }
}

// KWin Script used to read osu window status (and some other stuff)