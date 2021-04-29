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
    let imageEl = document.createElement("a-image");
    imageEl.setAttribute("src", data.imageSrc);

    let rawImageEl = document.createElement("img");
    rawImageEl.src = data.imageSrc;
    rawImageEl.onload = function () {
      const ratio = rawImageEl.width / rawImageEl.height;
      const scaleBy = data.hasOwnProperty("scaleBy") ? data.scaleBy : 5;
      imageEl.setAttribute("width", scaleBy * ratio);
      imageEl.setAttribute("height", scaleBy);
      if (data.hasOwnProperty("position")) {
        el.setAttribute("position", {
          x: data.position[0],
          y: data.position[1],
          z: data.position[2],
        });
      } else {
        el.setAttribute("position", { x: 0, y: 0, z: 0 });
      }
      imageEl.setAttribute("class", "link");

      el.appendChild(imageEl);

      let textEl = document.createElement("a-text");
      textEl.setAttribute("id", "text");
      textEl.setAttribute("value", data.text);
      textEl.setAttribute("negate", "true");
      textEl.setAttribute("scale", "2 2 1");
      let textVerticalOffset = data.hasOwnProperty("textVerticalOffset")
        ? data.textVerticalOffset
        : 1;
      let textHorizontalOffset = data.hasOwnProperty("textHorizontalOffset")
        ? data.textHorizontalOffset
        : 0;
      if (
        data.hasOwnProperty("textPosition") &&
        data.textPosition === "above"
      ) {
        textEl.setAttribute("position", {
          x: -4.9 + textHorizontalOffset,
          y: imageEl.getAttribute("height") / 2 + textVerticalOffset,
          z: 0.25,
        });
      } else {
        textEl.setAttribute("position", {
          x: -4.9 + textHorizontalOffset,
          y: -(imageEl.getAttribute("height") / 2 + textVerticalOffset),
          z: 0.25,
        });
      }
      el.appendChild(textEl);
    };
  },
  remove: function () {
    let visual_pane = document.querySelector("[visual-pane]");
    while (visual_pane.firstChild) {
      visual_pane.removeChild(visual_pane.lastChild);
    }
  },
});
