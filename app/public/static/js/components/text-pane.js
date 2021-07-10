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

    el.setAttribute("geometry", {
      primitive: "plane",
      width: data.width,
      height: data.height,
    });
    el.setAttribute("material", {
      color: data.color,
      shader: "flat",
      transparent: false,
    });
    el.setAttribute("position", { x: data.x, y: data.y, z: data.z });

    // Create textLabel
    this.textLabel = document.createElement("a-text");
    this.textLabel.setAttribute("id", "text-nav");
    this.textLabel.setAttribute("value", data.text);
    this.textLabel.setAttribute(
      "font",
      "https://raw.githubusercontent.com/jaydhulia/aframe-fonts/master/fonts/poppins/Poppins-Medium.json"
    );
    this.textLabel.setAttribute("shader", "msdf");
    this.textLabel.setAttribute("negate", "true");
    this.textLabel.setAttribute("scale", {
      x: data.scaleX,
      y: data.scaleY,
      z: data.scaleZ,
    });
    this.textLabel.setAttribute("color", "white");
    this.textLabel.setAttribute("align", "center");
    const xText = data.hasOwnProperty("xText") ? data.xText : 0;
    const yText = data.hasOwnProperty("yText") ? data.yText : 0;
    const zText = data.hasOwnProperty("zText") ? data.zText : 0;
    this.textLabel.setAttribute("position", { x: xText, y: yText, z: zText });

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
    const jsonData = this.data.jsonData;
    const el = this.el;

    this.textLabel = document.createElement("a-text");
    this.textLabel.setAttribute("id", "text");
    this.textLabel.setAttribute(
      "value",
      jsonData.data[jsonData.currPosition].text
    );
    this.textLabel.setAttribute(
      "font",
      "https://raw.githubusercontent.com/jaydhulia/aframe-fonts/master/fonts/poppins/Poppins-Medium.json"
    );
    this.textLabel.setAttribute("shader", "msdf");
    this.textLabel.setAttribute("negate", "true");
    this.textLabel.setAttribute("scale", "2 2 1");
    this.textLabel.setAttribute("position", "-4.9 0 0.25");
    el.appendChild(this.textLabel);
    const textLabelConst = this.textLabel;

    let initialVisualPane;
    if (jsonData.data[jsonData.currPosition].hasOwnProperty("imageSrc")) {
      initialVisualPane = createVisualPane(jsonData, el);
      this.textLabel.setAttribute("visible", false);
    }

    const leftNavProp = {
      width: "2",
      height: "1",
      depth: "0.005",
      color: "#1A1F26",
      x: "-7.75",
      y: "-6.75",
      z: "0.005",
      scaleX: "2",
      scaleY: "2",
      scaleZ: "1",
      text: "Prev",
    };

    const rightNavProp = {
      width: "2",
      height: "1",
      depth: "0.005",
      color: "#1A1F26",
      x: "7.75",
      y: "-6.75",
      z: "0.005",
      scaleX: "2",
      scaleY: "2",
      scaleZ: "1",
      text: jsonData.data.length === 1 ? "Got it!" : "Next",
    };

    // Create left nav button
    this.leftNav = document.createElement("a-entity");
    this.leftNav.setAttribute("id", "nav-button-left");
    this.leftNav.setAttribute(
      "text-box",
      "jsonData",
      JSON.stringify(leftNavProp)
    );
    this.leftNav.setAttribute("class", "link");
    this.el.appendChild(this.leftNav);

    // Create right nav button
    this.rightNav = document.createElement("a-entity");
    this.rightNav.setAttribute("id", "nav-button-right");
    this.rightNav.setAttribute(
      "text-box",
      "jsonData",
      JSON.stringify(rightNavProp)
    );
    this.rightNav.setAttribute("class", "link");
    this.el.appendChild(this.rightNav);

    let currVisualPane = initialVisualPane;

    const rightNavConst = this.rightNav;
    this.leftNav.addEventListener("click", function () {
      if (jsonData.currPosition !== 0) {
        --jsonData.currPosition;

        if (jsonData.data[jsonData.currPosition].hasOwnProperty("imageSrc")) {
          if (currVisualPane) {
            el.removeChild(currVisualPane);
          }

          textLabelConst.setAttribute("visible", false);
          let visualPane = createVisualPane(jsonData, el);
          currVisualPane = visualPane;
          el.appendChild(visualPane);
        } else {
          textLabelConst.setAttribute("visible", true);
          if (currVisualPane) {
            el.removeChild(currVisualPane);
            currVisualPane = null;
          }
          textLabelConst.setAttribute(
            "value",
            jsonData.data[jsonData.currPosition].text
          );
        }

        rightNavConst.firstChild.setAttribute("value", "Next");
      }
    });

    this.rightNav.addEventListener("click", function () {
      if (jsonData.currPosition === jsonData.data.length - 2) {
        rightNavConst.firstChild.setAttribute("value", "Got it!");
      }

      if (jsonData.currPosition !== jsonData.data.length - 1) {
        ++jsonData.currPosition;
        if (jsonData.data[jsonData.currPosition].hasOwnProperty("imageSrc")) {
          if (currVisualPane) {
            el.removeChild(currVisualPane);
          }
          textLabelConst.setAttribute("visible", false);

          let visualPane = createVisualPane(jsonData, el);
          currVisualPane = visualPane;
          el.appendChild(visualPane);
        } else {
          textLabelConst.setAttribute("visible", true);
          if (currVisualPane) {
            el.removeChild(currVisualPane);
            currVisualPane = null;
          }
          textLabelConst.setAttribute(
            "value",
            jsonData.data[jsonData.currPosition].text
          );
        }
      } else {
        if (jsonData.hasOwnProperty("isTransition") && jsonData.isTransition) {
          sceneComplete(0, jsonData.transitionURL);
        } else {
          el.sceneEl.emit("dcc-success-close-popup", {
            seconds: 0,
            is_last_object: false,
          });
        }
      }
    });
  },
});

function createVisualPane(jsonData, textPaneEl) {
  visualPaneJson = {
    imageSrc: jsonData.data[jsonData.currPosition].imageSrc,
    caption: jsonData.data[jsonData.currPosition].text,
  };

  let visualPane = document.createElement("a-entity");
  visualPane.setAttribute("id", "visual-pane");
  visualPane.setAttribute(
    "visual-pane",
    "jsonData",
    JSON.stringify(visualPaneJson)
  );
  textPaneEl.appendChild(visualPane);

  return visualPane;
}
