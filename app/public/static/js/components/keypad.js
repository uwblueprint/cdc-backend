AFRAME.registerComponent("keypad", {
  schema: {
    jsonData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
    isSolved: { type: "map" },
  },
  multiple: true,
  /**
   * Initial creation and setting of the mesh.
   */
  init: function () {
    const data = this.data.jsonData;
    const password = data.password;
    const el = this.el;
    this.id = data.id;
    let is_last_object = false;
    if ("is_last_object" in data) {
      is_last_object = data.is_last_object;
    }

    el.setAttribute("super-keyboard", {
      imagePath: "/static/img/",
      multipleInputs: true,
      align: "center",
      model: data.model,
      maxLength: password.length,
    });
    el.setAttribute("scale", { x: 20, y: 20, z: 20 });
    el.setAttribute("position", { x: 0, y: 0, z: 0.5 });
    el.addEventListener("superkeyboardinput", function (event) {
      if (event.detail.value === password) {
        // emit event to update state
        el.sceneEl.emit("solvedObject", { id: data.id });
        // emit event to close popup (after 1 second for now)
        el.sceneEl.emit("dcc-success-close-popup", { seconds: 1 });
        // emit event if it is last object, to indicate scene is solved
        if (is_last_object) {
          el.sceneEl.emit("dcc-success-scene-complete");
        }
      } else {
        const statusLabel = el.getAttribute("super-keyboard").label;
        if (statusLabel !== "SUCCESS") {
          el.setAttribute("super-keyboard", {
            label: "ERROR",
            labelColor: "red",
          });
          removeError(el);
        }
      }
    });

    const solvedPuzzleText = {
      width: "0.5",
      height: "0.05",
      depth: "0.05",
      color: "green",
      x: "0",
      y: "-0.3",
      z: "0",
      scaleX: "0.25",
      scaleY: "0.25",
      scaleZ: "0.25",
      text: "Solved",
    };
    // Create solved puzzle text
    this.solvedPuzzleEntity = document.createElement("a-entity");
    this.solvedPuzzleEntity.setAttribute("id", "keypad-solved-" + this.id);
    this.solvedPuzzleEntity.setAttribute(
      "text-box",
      "jsonData",
      JSON.stringify(solvedPuzzleText)
    );
    // initially set to false visibility
    this.solvedPuzzleEntity.setAttribute("visible", "false");
    el.appendChild(this.solvedPuzzleEntity);
  },
  update: function () {
    this.puzzleIsSolved = this.data.isSolved[this.id];
    const el = this.el;

    if (typeof this.puzzleIsSolved === "undefined") {
      // not loaded yet, do nothing
    } else if (this.puzzleIsSolved === true) {
      // Already solved
      el.setAttribute("super-keyboard", {
        label: "SUCCESS",
        labelColor: "green",
        multipleInputs: true,
      });
      this.solvedPuzzleEntity.setAttribute("visible", "true");
    } else {
      // Not solved yet
      el.setAttribute("super-keyboard", {
        label: "Enter Password",
        labelColor: "black",
      });
    }
  },
});

async function removeError(el) {
  setTimeout(function () {
    el.setAttribute("super-keyboard", {
      label: "Enter Password",
      labelColor: "black",
    });
  }, 1.5 * 1000);
}
