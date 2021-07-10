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

    el.setAttribute("geometry", {
      primitive: "plane",
      width: data.width,
      height: data.height,
    });
    el.setAttribute("material", {
      color: data.color,
      shader: "flat",
      transparent: false,
    });
    el.setAttribute("position", { x: data.xTarget, y: data.yTarget, z: 0 });
  },
});
