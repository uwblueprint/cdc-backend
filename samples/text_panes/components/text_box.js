AFRAME.registerComponent("text-box", {
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

    el.object3D.position.set(data.x, data.y, data.z);
    // Set mesh on entity.
    el.setObject3D("mesh", this.mesh);

    // Create textLabel
    this.textLabel = document.createElement("a-text");
    this.textLabel.setAttribute("id", "text-nav");
    this.textLabel.setAttribute("value", data.text);
    this.textLabel.setAttribute(
      "font",
      "https://raw.githubusercontent.com/etiennepinchon/aframe-fonts/master/fonts/poppins/Poppins-Bold.json"
    );
    this.textLabel.setAttribute("shader", "msdf");
    this.textLabel.setAttribute("negate", "true");
    this.textLabel.setAttribute("scale", "2 2 1");
    this.textLabel.setAttribute("color", "black");
    this.textLabel.setAttribute("align", "center");
    this.el.appendChild(this.textLabel);
  },
});
