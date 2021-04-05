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
    this.textLabel.setAttribute("position", "-3 0 0.25");
    this.el.appendChild(this.textLabel);

    // Create left nav button
    this.leftNav = document.createElement("a-entity");
    this.leftNav.setAttribute(
      "prism",
      "jsonData",
      '{"width": "1", "height": "1", "depth": "0.01", "color": "white", "x": "-8.25", "y": "0", "z": "0.005"}'
    );
    this.leftNav.addEventListener("click", function () {
      if (data.currPosition != 0) {
        --data.currPosition;
        document
          .querySelector("#text")
          .setAttribute("value", data.text[data.currPosition]);
      }
    });
    this.el.appendChild(this.leftNav);

    // Create right nav button
    this.rightNav = document.createElement("a-entity");
    this.rightNav.setAttribute(
      "prism",
      "jsonData",
      '{"width": "1", "height": "1", "depth": "0.01", "color": "white", "x": "8.25", "y": "0", "z": "0.005"}'
    );
    this.rightNav.addEventListener("click", function () {
      if (data.currPosition != data.text.length - 1) {
        ++data.currPosition;
        document
          .querySelector("#text")
          .setAttribute("value", data.text[data.currPosition]);
      }
    });
    this.el.appendChild(this.rightNav);
  },

  update: function () {
    console.log("updating");
    const data = this.data.jsonData;
    const el = this.el;
  },
});
