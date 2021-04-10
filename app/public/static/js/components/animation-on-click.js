AFRAME.registerComponent("animation-on-click-run", {
  schema: {
    blackboardData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
  },
  dependencies: ["animation__onclick"],

  init: function () {
    const el = this.el;
    this.data.blackboardData.jsonData.id = el.id;

    const extraInfo = this.data.blackboardData;

    // initialize each interactive object to not solved state, except text-panes (which are just view objects)
    if (extraInfo.componentType === "text-pane") {
      el.sceneEl.emit("initializeObject", { id: el.id, solved: true });
    } else {
      el.sceneEl.emit("initializeObject", { id: el.id, solved: false });
    }

    this.el.addEventListener("animationbegin", function (e) {
      // do nothing for now, will be added later, if needed
    });

    this.el.addEventListener("animationcomplete", function (e) {
      if (e.detail.name === "animation__onclick") {
        // Call Dhruvin's function
        addEntityToBlackboard(extraInfo);
      }
    });
  },
});

// TODO: Add support for multiple entity creation
function addEntityToBlackboard(componentDataParsed) {
  var blackboardEl = document.querySelector("#blackboard");
  var entityEl = document.createElement("a-entity");
  entityEl.setAttribute(
    componentDataParsed.componentType,
    "jsonData",
    JSON.stringify(componentDataParsed.jsonData)
  );
  entityEl.setAttribute(
    "bind__" + componentDataParsed.componentType,
    "isSolved: solvedObjects"
  );

  entityEl.addEventListener("loaded", function (e) {
    if (e.target === entityEl) {
      var popupCameraEl = document.querySelector("#popup-camera");
      popupCameraEl.setAttribute("camera", "active", true);
    }
  });
  blackboardEl.appendChild(entityEl);
}
