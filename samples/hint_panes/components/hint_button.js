AFRAME.registerComponent("hint-button", {
  schema: {
    jsonData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
  },
  multiple: true,

  init: function () {
    const data = this.data.jsonData;

    let z = -0.5;
    let x = visibleWidthAtZDepth(z) / 2 - data.width;
    let y = -visibleHeightAtZDepth(z) / 2 + data.height;

    // Create hint button
    this.hintIcon = document.createElement("a-image");
    this.hintIcon.setAttribute("id", "hint-icon");
    this.hintIcon.setAttribute("src", data.newHintImg);
    this.hintIcon.setAttribute("width", data.width);
    this.hintIcon.setAttribute("height", data.height);
    this.hintIcon.object3D.position.set(x, y, z);
    this.el.appendChild(this.hintIcon);

    // Create hint label
    this.hintLabel = document.createElement("a-text");
    this.hintLabel.setAttribute("id", "hint-label");
    this.hintLabel.setAttribute("value", "New Hints!");
    this.hintLabel.setAttribute("color", "black");
    this.hintLabel.setAttribute("scale", { x: 0.07, y: 0.07, z: 0.07 });
    this.hintLabel.setAttribute("align", "center");
    this.hintLabel.object3D.position.set(x, y - (data.height * 2) / 3, z);
    this.el.appendChild(this.hintLabel);

    // Create openPopup
    this.openPopup = document.createElement("a-entity");
    this.openPopup.setAttribute("class", "link");
    // Text pane data in blackboardData is currently hardcoded, once we integrate with backend it should be removed.
    let openPopupJson = {
      width: data.width,
      height: data.height,
      depth: 0.001,
      x: x,
      y: y,
      z: z,
      color: "white",
      transparent: true,
      opacity: 0.0,
      blackboardData: {
        componentType: "text_pane",
        jsonData: {
          text: [
            "Hint 1: Have you checked the folded page in your textbook? There might be some useful info there...",
            "Hint 2: Filler text",
            "Hint 3: Filler text",
          ],
          currPosition: 0,
        },
      },
    };

    this.openPopup.setAttribute(
      "open-popup",
      "jsonData",
      JSON.stringify(openPopupJson)
    );

    const hintIcon = this.hintIcon;
    const hintLabel = this.hintLabel;
    const openPopup = this.openPopup;

    this.openPopup.addEventListener("click", function () {
      hintIcon.setAttribute("src", data.hintImg);
      hintLabel.setAttribute("value", "Hints");
    });
    this.el.appendChild(this.openPopup);

    // Update the location of the hint button on the screen depending on the screen size
    window.addEventListener("resize", function () {
      const z = -0.5;
      const x = visibleWidthAtZDepth(z) / 2 - data.width;
      const y = -visibleHeightAtZDepth(z) / 2 + data.height;

      hintIcon.object3D.position.set(x, y, z);
      // Y position is directly underneath the hint icon
      hintLabel.object3D.position.set(x, y - (data.height * 2) / 3, z);
      openPopup.object3D.position.set(x, y, z);
    });
  },
});

function visibleHeightAtZDepth(depth) {
  const camera = document.querySelector("#primaryCamera");

  // vertical field of view in radians
  const vFOV = (camera.getAttribute("fov") * Math.PI) / 180;

  // Using trigonometry to determine height, Math.abs ensures the result is always positive
  let height = 2 * Math.tan(vFOV / 2) * Math.abs(depth);

  return height;
}

function visibleWidthAtZDepth(depth) {
  const camera = document.querySelector("#primaryCamera").object3D;
  const height = visibleHeightAtZDepth(depth, camera);
  const aspect = window.innerWidth / window.innerHeight;
  let width = height * aspect;
  return width;
}
