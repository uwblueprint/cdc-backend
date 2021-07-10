AFRAME.registerComponent("visual-pane", {
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
    const el = this.el;
    let imageEl = document.createElement("a-image");
    imageEl.setAttribute(
      "src",
      data.imageSrc + "?d=" + new Date().getTime() / 1000
    );

    let rawImageEl = document.createElement("img");
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

      el.appendChild(imageEl);

      if (data.hasOwnProperty("caption")) {
        let captionEl = document.createElement("a-text");
        captionEl.setAttribute("id", "text");
        captionEl.setAttribute("value", data.caption);
        captionEl.setAttribute("negate", "true");
        captionEl.setAttribute("scale", "2 2 1");
        captionEl.setAttribute(
          "font",
          "https://raw.githubusercontent.com/jaydhulia/aframe-fonts/master/fonts/poppins/Poppins-Medium.json"
        );
        captionEl.setAttribute("shader", "msdf");
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
          captionEl.setAttribute("position", {
            x: -4.9 + textHorizontalOffset,
            y: imageEl.getAttribute("height") / 1.6 + textVerticalOffset,
            z: 0.25,
          });
        } else {
          captionEl.setAttribute("position", {
            x: -4.9 + textHorizontalOffset,
            y: -(imageEl.getAttribute("height") / 1.6 + textVerticalOffset),
            z: 0.25,
          });
        }
        el.appendChild(captionEl);
      }
    };
    rawImageEl.crossOrigin = "anonymous";
    rawImageEl.src = data.imageSrc + "?d=" + new Date().getTime();
  },
  remove: function () {
    let el = this.el;
    while (el.firstChild) {
      el.removeChild(el.lastChild);
    }
  },
});
