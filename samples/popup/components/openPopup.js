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
    const data = this.data.jsonData;
    const el = this.el;

    // Create geometry.
    this.geometry = new THREE.BoxBufferGeometry(
      data.width,
      data.height,
      data.depth
    );

    const isTransparent = data.hasOwnProperty("transparent")
      ? data.transparent
      : false;
    const objectOpacity = data.hasOwnProperty("opacity") ? data.opacity : 1.0;

    // Create material.
    this.material = new THREE.MeshStandardMaterial({
      color: data.color,
      transparent: isTransparent,
      opacity: objectOpacity,
    });

    // Create mesh.
    this.mesh = new THREE.Mesh(this.geometry, this.material);

    el.object3D.position.set(data.x, data.y, data.z);
    // Set mesh on entity.
    el.setObject3D("mesh", this.mesh);
    el.addEventListener("loaded", function (e) {
      if (e.target === el) {
        // Add event listener for closing (returning) on mouse click.
        el.addEventListener("click", function () {
          addEntityToBlackboard(JSON.stringify(data.blackboardData));
        });
      }
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
  entityEl.addEventListener("loaded", function (e) {
    if (e.target === entityEl) {
      var popupCameraEl = document.querySelector("#popup-camera");
      popupCameraEl.setAttribute("camera", "active", true);
    }
  });
  blackboardEl.appendChild(entityEl);
}
