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

    // Create textLabel
    this.textLabel = document.createElement("a-text");
    this.textLabel.setAttribute("id", "text");
    this.textLabel.setAttribute("value", data.text[data.currPosition]);
    this.textLabel.setAttribute(
      "font",
      "https://raw.githubusercontent.com/jaydhulia/aframe-fonts/master/fonts/poppins/Poppins-Medium.json"
    );
    this.textLabel.setAttribute("shader", "msdf");
    this.textLabel.setAttribute("negate", "true");
    this.textLabel.setAttribute("scale", "2 2 1");
    this.textLabel.setAttribute("position", "-4.9 0 0.25");
    this.el.appendChild(this.textLabel);

    if (data.text.length > 1) {
      const leftNavProp =
        '{"width": "1.5", "height": "1.5", "depth": "0.005", "color": "white", "x": "-8", "y": "0", "z": "0.005", "text": "Prev"}';
      const rightNavProp =
        '{"width": "1.5", "height": "1.5", "depth": "0.005", "color": "white", "x": "8", "y": "0", "z": "0.005", "text": "Next"}';
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
          closeTextPane();
        }
      });
    }
  },
});

function closeTextPane() {
  var textPaneEl = document.querySelector("#text_pane");
  while (textPaneEl && textPaneEl.firstChild) {
    textPaneEl.removeChild(textPaneEl.lastChild);
  }
}
