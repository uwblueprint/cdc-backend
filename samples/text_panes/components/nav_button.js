AFRAME.registerComponent("nav-button", {
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
    console.log(data);
    // Create geometry.
    this.setAttribute(
      "geometry",
      "primitive: plane; height: auto; width: auto"
    );

    // Create material.
    this.setAttribute("material", "color: blue");

    // Create mesh.
    //    this.mesh = new THREE.Mesh(this.geometry, this.material);

    el.object3D.position.set(data.x, data.y, data.z);
    // Set mesh on entity.
    //    el.setObject3D("mesh", this.mesh);

    // Create textLabel
    //    this.textLabel = document.createElement("a-text");
    //    this.textLabel.setAttribute("id", "text-nav" + data.side);
    //    this.textLabel.setAttribute("value", data.text);
    //    this.textLabel.setAttribute("negate", "true");
    //    this.textLabel.setAttribute("scale", "2 2 1");
    //    this.textLabel.setAttribute("color", "black");
    //    this.textLabel.setAttribute("position", "-0.5 0 0.1");
    //    this.el.appendChild(this.textLabel);
  },

  update: function () {
    const data = this.data.jsonData;
    const el = this.el;
    console.log("updating nav button: " + data.text);
    this.textLabel.setAttribute("value", data.text);
    //    document
    //      .querySelector("#text-nav")
    //      .setAttribute("value", data.text);
  },
});
