AFRAME.registerComponent("keypad", {
  schema: {
    jsonData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
    isSolved: { type: "map" },
    score: { type: "number" },
  },
  multiple: true,
  /**
   * Initial creation and setting of the mesh.
   */
  init: function () {
    const data = this.data.jsonData;
    const password = data.password;
    const el = this.el;
    console.log("init:");
    console.log(this.data.isSolved);
    el.setAttribute(
      "super-keyboard",
      "imagePath:/static/img/; multipleInputs:true; model: numpad; align: center; maxLength: 4; label: Enter Password; labelColor: black"
    );
    el.setAttribute("scale", { x: 20, y: 20, z: 20 });
    el.setAttribute("position", { x: 0, y: 0, z: 0.5 });

    el.setAttribute("class", "link");

    el.addEventListener("superkeyboardinput", function (event) {
      if (event.detail.value === password) {
        el.setAttribute(
          "super-keyboard",
          "label:SUCCESS; labelColor: green; multipleInputs:true"
        );
        el.sceneEl.emit("solvedObject", { id: data.id });
      } else {
        const statusLabel = el.getAttribute("super-keyboard").label;
        if (statusLabel !== "SUCCESS") {
          el.setAttribute("super-keyboard", "label:ERROR; labelColor: red");
          removeError(el);
        }
      }
    });
  },
  update: function () {
    console.log("update:");
    console.log(this.data.isSolved);
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
