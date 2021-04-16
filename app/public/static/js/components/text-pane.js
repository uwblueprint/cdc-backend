// Components related to text pane
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
    this.textLabel.setAttribute("negate", "true");
    this.textLabel.setAttribute("scale", {
      x: data.scaleX,
      y: data.scaleY,
      z: data.scaleZ,
    });
    this.textLabel.setAttribute("color", "black");
    this.textLabel.setAttribute("align", "center");
    this.el.appendChild(this.textLabel);
  },
});

AFRAME.registerComponent("text-pane", {
  schema: {
    jsonData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
    isSolved: { type: "map" },
  },

  multiple: true,

  init: function () {
    const data = this.data.jsonData;

    // Create textLabel
    this.textLabel = document.createElement("a-text");
    this.textLabel.setAttribute("id", "text");
    this.textLabel.setAttribute("value", data.text[data.currPosition]);
    this.textLabel.setAttribute("negate", "true");
    this.textLabel.setAttribute("scale", "2 2 1");
    this.textLabel.setAttribute("position", "-4.9 0 0.25");
    this.el.appendChild(this.textLabel);

    if (data.text.length > 1) {
      const leftNavProp =
        '{"width": "1.5", "height": "1.5", "depth": "0.005", "color": "white", "x": "-8", "y": "0", "z": "0.005", "scaleX": "2", "scaleY": "2", "scaleZ": "1", "text": "Prev"}';
      const rightNavProp =
        '{"width": "1.5", "height": "1.5", "depth": "0.005", "color": "white", "x": "8", "y": "0", "z": "0.005", "scaleX": "2", "scaleY": "2", "scaleZ": "1", "text": "Next"}';
      const textLabelConst = this.textLabel;

      // Create left nav button
      this.leftNav = document.createElement("a-entity");
      this.leftNav.setAttribute("id", "nav-button-left");
      this.leftNav.setAttribute("text-box", "jsonData", leftNavProp);
      this.leftNav.setAttribute("class", "link");
      this.el.appendChild(this.leftNav);

      // Create right nav button
      this.rightNav = document.createElement("a-entity");
      this.rightNav.setAttribute("id", "nav-button-right");
      this.rightNav.setAttribute("text-box", "jsonData", rightNavProp);
      this.rightNav.setAttribute("class", "link");
      this.el.appendChild(this.rightNav);

      const rightNavConst = this.rightNav;
      this.leftNav.addEventListener("click", function () {
        if (data.currPosition !== 0) {
          --data.currPosition;
          textLabelConst.setAttribute("value", data.text[data.currPosition]);
          rightNavConst.firstChild.setAttribute("value", "Next");
        }
      });

      this.rightNav.addEventListener("click", function () {
        if (data.currPosition === data.text.length - 2) {
          rightNavConst.firstChild.setAttribute("value", "Done");
        }

        if (data.currPosition !== data.text.length - 1) {
          ++data.currPosition;
          textLabelConst.setAttribute("value", data.text[data.currPosition]);
        } else {
          // TODO: later PR, clicking on done -> close blackboard, similar to keypad success message
        }
      });
    }
  },
});
