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
        el.sceneEl.emit("dcc-success-close-popup", {
          seconds: 2,
          is_last_object: is_last_object,
        });
      } else {
        const statusLabel = el.getAttribute("super-keyboard").label;
        if (statusLabel !== "SUCCESS") {
          el.setAttribute("super-keyboard", {
            label: "ERROR",
            labelColor: "red",
          });
          removeError(el, data);
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
    const data = this.data.jsonData;

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
      keypad_text = data.hasOwnProperty("keypad_text")
        ? data.keypad_text
        : "Enter Password";
      keypad_text_color = data.hasOwnProperty("keypad_text_color")
        ? data.keypad_text_color
        : "white";
      el.setAttribute("super-keyboard", {
        label: keypad_text,
        labelColor: keypad_text_color,
      });
    }
  },
});

async function removeError(el, data) {
  setTimeout(function () {
    keypad_text = data.hasOwnProperty("keypad_text")
      ? data.keypad_text
      : "Enter Password";
    keypad_text_color = data.hasOwnProperty("keypad_text_color")
      ? data.keypad_text_color
      : "white";
    el.setAttribute("super-keyboard", {
      label: keypad_text,
      labelColor: keypad_text_color,
    });
  }, 1.5 * 1000);
}
