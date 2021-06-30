AFRAME.registerComponent("interactable", {
  schema: {
    axis: {
      type: "string",
      default: "x",
    },
    value: {
      type: "number",
      default: 1,
    },
  },
  init: function () {
    let el = this.el;
    let model = el.object3D;

    el.addEventListener("model-loaded", function (e) {
      let box = new THREE.Box3().setFromObject(model);
      let size = box.getSize();
      const old_scale = el.getAttribute("scale");
      const old_scale_x = old_scale.x;
      const old_scale_y = old_scale.y;
      const old_scale_z = old_scale.z;
      const x = size.x;
      const y = size.y;
      const z = size.z;
      let scaling_factor = Math.max(x, y, z);
      scaling_factor = (scaling_factor + 0.05) / scaling_factor;
      const new_scale_x = old_scale_x * scaling_factor;
      const new_scale_y = old_scale_y * scaling_factor;
      const new_scale_z = old_scale_z * scaling_factor;

      el.setAttribute(
        "animation__mouseenter",
        `property: scale; to: ${new_scale_x} ${new_scale_y} ${new_scale_z}; dur: 100; startEvents: mouseenter`
      );
      el.setAttribute(
        "animation__mouseleave",
        `property: scale; to: ${old_scale_x} ${old_scale_y} ${old_scale_z}; dur: 100; startEvents: mouseleave`
      );
    });
  },
});
