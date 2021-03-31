AFRAME.registerComponent("open-popup", {
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
    console.log("RANNNNNNNNNNNNNNN");
    console.log("RANNNNNNNNNNNNNNN");
    console.log("RANNNNNNNNNNNNNNN");
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
      addEntityToBlackboard(JSON.stringify(data.blackboardData));
      var popupCameraEl = document.querySelector("#popup-camera");
      popupCameraEl.setAttribute("camera", "active", true);
    });
  },
});

// TODO: Add support for multiple entity creation
function addEntityToBlackboard(componentData) {
  var componentDataParsed = JSON.parse(componentData);
  var blackboardEl = document.querySelector("#blackboard");
  var entityEl = document.createElement("a-entity");
  entityEl.setAttribute(
    componentDataParsed.componentType,
    "jsonData",
    JSON.stringify(componentDataParsed.jsonData)
  );
  blackboardEl.appendChild(entityEl);
}
