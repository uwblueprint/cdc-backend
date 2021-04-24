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
      closePopup(0);
    });

    // Add event listener for closing on successful puzzle solve, after X seconds
    el.sceneEl.addEventListener("dcc-success-close-popup", function (e) {
      closePopup(e.detail.seconds);
    });
  },
});

async function closePopup(numSeconds) {
  setTimeout(function () {
    const primaryCamera = document.querySelector("#primaryCamera");
    primaryCamera.setAttribute("camera", "active", true);
    wipeBlackboard();
  }, numSeconds * 1000);
}

function wipeBlackboard() {
  let blackboardEl = document.querySelector("#blackboard");
  while (blackboardEl.firstChild) {
    blackboardEl.removeChild(blackboardEl.lastChild);
  }
}
