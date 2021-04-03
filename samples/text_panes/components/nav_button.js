AFRAME.registerComponent("nav_button", {
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
      var text_pane = document.querySelector("#text_pane");
      var is_updated = text_pane.update(data.direction);

      if (!is_updated) {
        remove();
      }
    });
  },

  remove: function () {
    const data = this.data.jsonData;
    const el = this.el;
    el.removeObject3D("mesh");

    if (data.jsonData) {
      el.removeEventListener();
    }
  },
});
