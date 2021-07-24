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
    let x = (visibleWidthAtZDepth(z) * 52) / 100 - data.width;
    let y = -visibleHeightAtZDepth(z) / 2 + data.height;

    // Create hint button
    this.hintIcon = document.createElement("a-image");
    this.hintIcon.setAttribute("id", "hint-icon");
    this.hintIcon.setAttribute("src", data.newHintImg);
    this.hintIcon.setAttribute("width", data.width);
    this.hintIcon.setAttribute("height", data.height);
    this.hintIcon.setAttribute("class", "link");
    this.hintIcon.object3D.position.set(x, y, z);

    const hintIcon = this.hintIcon;
    this.hintIcon.addEventListener("click", function () {
      hintIcon.setAttribute("src", data.hintImg);
    });
    this.el.appendChild(this.hintIcon);

    // Update the location of the hint button on the screen depending on the screen size
    window.addEventListener("resize", function () {
      const z = -0.5;
      const x = visibleWidthAtZDepth(z) / 2 - data.width;
      const y = -visibleHeightAtZDepth(z) / 2 + data.height;

      hintIcon.object3D.position.set(x, y, z);
    });
  },
});

function visibleHeightAtZDepth(depth) {
  const camera = document.querySelector("#primaryCamera");

  // vertical field of view in radians
  const vFOV = (camera.getAttribute("fov") * Math.PI) / 180;

  // Using trigonometry to determine height, Math.abs ensures the result is always positive
  return 2 * Math.tan(vFOV / 2) * Math.abs(depth);
}

function visibleWidthAtZDepth(depth) {
  const height = visibleHeightAtZDepth(depth);
  const aspect = window.innerWidth / window.innerHeight;
  return height * aspect;
}
