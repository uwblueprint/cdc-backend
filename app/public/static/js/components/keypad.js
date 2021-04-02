AFRAME.registerComponent("keypad", {
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
    const password = data.password;
    const el = this.el;
    el.setAttribute(
      "super-keyboard",
      "imagePath:static/img/; multipleInputs:true; model: numpad; align: center; maxLength: 4; label: Enter Password; labelColor: black"
    );
    el.setAttribute("scale", { x: 20, y: 20, z: 20 });

    el.setAttribute("class", "link");
    console.log(el);

    el.addEventListener("superkeyboardinput", function (event) {
      if (event.detail.value === password) {
        console.log("pass");
        el.setAttribute(
          "super-keyboard",
          "label:SUCCESS; labelColor: green; multipleInputs:true"
        );
      } else {
        const statusLabel = el.getAttribute("super-keyboard").label;
        if (statusLabel !== "SUCCESS") {
          console.log("fail ");

          el.setAttribute("super-keyboard", "label:ERROR; labelColor: red");
          removeError(el);
        }
      }
    });

    // // Create geometry.
    // this.geometry = new THREE.BoxBufferGeometry(
    //   data.width,
    //   data.height,
    //   data.depth
    // );
    //
    // // Create material.
    // this.material = new THREE.MeshStandardMaterial({ color: data.color });
    //
    // // Create mesh.
    // this.mesh = new THREE.Mesh(this.geometry, this.material);
    //
    // el.object3D.position.set(data.x, data.y, data.z);
    // // Set mesh on entity.
    // el.setObject3D("mesh", this.mesh);
  },
});

async function removeError(el) {
  setTimeout(function () {
    el.setAttribute(
      "super-keyboard",
      "label:Enter Password; labelColor: black"
    );
  }, 1.5 * 1000);
}
