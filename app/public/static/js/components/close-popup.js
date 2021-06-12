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

    // Create geometry.
    this.geometry = new THREE.BoxBufferGeometry(
      data.width,
      data.height,
      data.depth
    );

    // Create material.
    this.material = new THREE.MeshStandardMaterial({ color: data.color });

    // Create mesh.
    this.mesh = new THREE.Mesh(this.geometry, this.material);

    el.object3D.position.set(data.x, data.y, data.z);
    // Set mesh on entity.
    el.setObject3D("mesh", this.mesh);

    // Add event listener for closing (returning) on mouse click.
    el.addEventListener("click", function () {
      closePopup(0, false, el);
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
      primaryCamera.setAttribute("look-controls", "enabled", true);
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
  let blackbaordTextEl = document.querySelector("#blackboardText");
  blackbaordTextEl.setAttribute("text", "value", "");
  while (blackboardEl.firstChild) {
    blackboardEl.removeChild(blackboardEl.lastChild);
  }
}
