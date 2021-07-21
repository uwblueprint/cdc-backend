AFRAME.registerComponent("close-popup", {
  schema: {
    jsonData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
  },
  multiple: true,
  /**
   * Initial creation and setting of the mesh.
   */
  init: function () {
    const data = this.data.jsonData;
    const el = this.el;

    el.setAttribute("geometry", {
      primitive: "box",
      width: data.width,
      height: data.height,
      depth: data.depth,
    });
    el.setAttribute("material", {
      color: data.color,
      shader: "flat",
      transparent: true,
      opacity: data.opacity,
    });
    el.setAttribute("position", { x: data.x, y: data.y, z: data.z });

    // Add event listener for closing (returning) on mouse click.
    el.addEventListener("click", function () {
      if (!el.hasAttribute("tutorial-hints")) {
        closePopup(0, false, el);
      }
    });

    // Add event listener for closing on successful puzzle solve, after X seconds
    el.sceneEl.addEventListener("dcc-success-close-popup", function (e) {
      closePopup(e.detail.seconds, e.detail.is_last_object, el);
    });
  },
});

let sceneSolved = false;

async function closePopup(numSeconds, is_last_object, el) {
  if (!sceneSolved) {
    setTimeout(function () {
      const primaryCamera = document.querySelector("#primaryCamera");
      primaryCamera.setAttribute("camera", "active", true);
      wipeBlackboard();

      // emit event if it is last object, to indicate scene is solved
      if (is_last_object) {
        sceneSolved = true;
        el.setAttribute("visible", false);
        el.sceneEl.emit("dcc-success-scene-complete");
      }
    }, numSeconds * 1000);
  }
}

function wipeBlackboard() {
  let blackboardEl = document.querySelector("#blackboard");
  let blackboardTextEl = document.querySelector("#blackboardText");
  blackboardTextEl.setAttribute("text", "value", "");
  let blackboardParagraphEl = document.querySelector("#blackboardParagraph");
  blackboardParagraphEl.setAttribute("text", "value", "");
  while (blackboardEl.firstChild) {
    blackboardEl.removeChild(blackboardEl.lastChild);
  }
}
