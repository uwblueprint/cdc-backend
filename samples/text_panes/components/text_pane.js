AFRAME.registerComponent("text_pane", {
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
        '{"width": "1.5", "height": "1.5", "depth": "0.01", "color": "white", "x": "-8", "y": "0", "z": "0.005"}';
      const rightNavProp =
        '{"width": "1.5", "height": "1.5", "depth": "0.01", "color": "white", "x": "8", "y": "0", "z": "0.005"}';

      // Create left nav textLabel
      this.buttonLabelLeft = document.createElement("a-text");
      this.buttonLabelLeft.setAttribute("id", "text-nav-left");
      this.buttonLabelLeft.setAttribute("value", "Prev");
      this.buttonLabelLeft.setAttribute("negate", "true");
      this.buttonLabelLeft.setAttribute("scale", "2 2 1");
      this.buttonLabelLeft.setAttribute("color", "black");
      this.buttonLabelLeft.setAttribute("position", "-8.5 0 0.01");
      this.el.appendChild(this.buttonLabelLeft);

      // Create left nav button
      this.leftNav = document.createElement("a-entity");
      this.leftNav.setAttribute("id", "nav-button-left");
      this.leftNav.setAttribute("prism", "jsonData", leftNavProp);
      this.leftNav.addEventListener("click", function () {
        if (data.currPosition != 0) {
          --data.currPosition;
          document
            .querySelector("#text")
            .setAttribute("value", data.text[data.currPosition]);
          document
            .querySelector("#text-nav-right")
            .setAttribute("jsonData", rightNavProp);
        }
      });
      this.el.appendChild(this.leftNav);

      // Create right nav textLabel
      this.buttonLabelRight = document.createElement("a-text");
      this.buttonLabelRight.setAttribute("id", "text-nav-right");
      this.buttonLabelRight.setAttribute("value", "Next");
      this.buttonLabelRight.setAttribute("negate", "true");
      this.buttonLabelRight.setAttribute("scale", "2 2 1");
      this.buttonLabelRight.setAttribute("color", "black");
      this.buttonLabelRight.setAttribute("position", "7.5 0 0.01");
      this.el.appendChild(this.buttonLabelRight);

      // Create right nav button
      this.rightNav = document.createElement("a-entity");
      this.rightNav.setAttribute("id", "nav-button-right");
      this.rightNav.setAttribute("prism", "jsonData", rightNavProp);
      this.rightNav.addEventListener("click", function () {
        if (data.currPosition == data.text.length - 2) {
          document
            .querySelector("#text-nav-right")
            .setAttribute("value", "Done");
        }

        if (data.currPosition != data.text.length - 1) {
          ++data.currPosition;
          document
            .querySelector("#text")
            .setAttribute("value", data.text[data.currPosition]);
        } else {
          closeTextPane();
        }
      });
      this.el.appendChild(this.rightNav);
    }
  },
});

function closeTextPane() {
  var textPaneEl = document.querySelector("#text_pane");
  while (textPaneEl.firstChild) {
    textPaneEl.removeChild(textPaneEl.lastChild);
  }
}
