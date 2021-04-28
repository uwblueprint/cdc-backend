AFRAME.registerComponent("visual-pane", {
  schema: {
    jsonData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
  },

  multiple: true,

  init: function () {
    const data = this.data.jsonData;
    const el = this.el;

    this.imageEl = document.createElement("a-image");
    this.imageEl.setAttribute("src", data.imageSrc);

    const rawImageEl = document.querySelector(data.imageSrc);
    const ratio = rawImageEl.width / rawImageEl.height;
    const scaleBy = data.hasOwnProperty("scaleBy") ? data.scaleBy : 5;
    this.imageEl.setAttribute("width", scaleBy * ratio);
    this.imageEl.setAttribute("height", scaleBy);
    // Randomizes the position of the puzzle piece on the blackboard
    if (data.hasOwnProperty("position")) {
      el.setAttribute("position", {
        x: data.position[0],
        y: data.position[1],
        z: data.position[2],
      });
    } else {
      el.setAttribute("position", { x: 0, y: 0, z: 0 });
    }
    this.imageEl.setAttribute("class", "link");

    this.el.appendChild(this.imageEl);

    this.textEl = document.createElement("a-text");
    this.textEl.setAttribute("id", "text");
    this.textEl.setAttribute("value", data.text);
    this.textEl.setAttribute("negate", "true");
    this.textEl.setAttribute("scale", "2 2 1");
    let textVerticalOffset = 1;
    let textHorizontalOffset = 0;
    if (data.hasOwnProperty("textVerticalOffset")) {
      textVerticalOffset = data.textVerticalOffset;
    }
    if (data.hasOwnProperty("textHorizontalOffset")) {
      textHorizontalOffset = data.textHorizontalOffset;
    }
    if (data.hasOwnProperty("textPosition") && data.textPosition === "above") {
      this.textEl.setAttribute("position", {
        x: -4.9 + textHorizontalOffset,
        y: this.imageEl.getAttribute("height") / 2 + textVerticalOffset,
        z: 0.25,
      });
    } else {
      this.textEl.setAttribute("position", {
        x: -4.9 + textHorizontalOffset,
        y: -(this.imageEl.getAttribute("height") / 2 + textVerticalOffset),
        z: 0.25,
      });
    }
    this.el.appendChild(this.textEl);
  },
  remove: function () {
    let visual_pane = document.querySelector("[visual-pane]");
    while (visual_pane.firstChild) {
      visual_pane.removeChild(visual_pane.lastChild);
    }
  },
});
