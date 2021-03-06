AFRAME.registerComponent("target-box", {
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
    this.geometry = new THREE.PlaneGeometry(data.width, data.height);

    // Create material.
    this.material = new THREE.MeshStandardMaterial({ color: data.color });

    // Create mesh.
    this.mesh = new THREE.Mesh(this.geometry, this.material);

    el.object3D.position.set(data.xTarget, data.yTarget, 0);
    // Set mesh on entity.
    el.setObject3D("mesh", this.mesh);
  },
});
