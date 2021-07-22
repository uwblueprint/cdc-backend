AFRAME.registerComponent("animation-on-click-run", {
  schema: {
    blackboardData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
  },
  dependencies: ["animation__onclick"],

  init: function () {
    const el = this.el;
    this.data.blackboardData.jsonData.id = el.id;

    const extraInfo = this.data.blackboardData;

    // initialize each interactive object to not solved state, except text-panes (which are just view objects)
    if (extraInfo.componentType === "text-pane") {
      el.sceneEl.emit("initializeObject", { id: el.id, solved: true });
    } else {
      el.sceneEl.emit("initializeObject", { id: el.id, solved: false });
    }

    this.el.addEventListener("animationbegin", function (e) {
      // do nothing for now, will be added later, if needed
    });

    this.el.addEventListener("animationcomplete", function (e) {
      if (e.detail.name === "animation__onclick") {
        addEntityToBlackboard(extraInfo);
      } else if (e.detail.name === "animation__onclick_tutorial") {
        // Tutorial needs a special case
        const closeButtonEl = document.getElementById("returnButton");
        closeButtonEl.setAttribute("class", "link");
        closeButtonEl.setAttribute("visible", "true");
        addEntityToBlackboard(extraInfo);
      }
    });
  },
});

// TODO: Add support for multiple entity creation
function addEntityToBlackboard(componentDataParsed) {
  let blackboardEl = document.querySelector("#blackboard");
  let entityEl = document.createElement("a-entity");
  componentDataParsed.jsonData.isBlackboardParagraphDefined = componentDataParsed.hasOwnProperty(
    "blackboardParagraph"
  );
  componentDataParsed.jsonData.isBlackboardTextDefined = componentDataParsed.hasOwnProperty(
    "blackboardText"
  );
  entityEl.setAttribute(
    componentDataParsed.componentType,
    "jsonData",
    JSON.stringify(componentDataParsed.jsonData)
  );
  entityEl.setAttribute(
    "bind__" + componentDataParsed.componentType,
    "isSolved: solvedObjects"
  );

  entityEl.addEventListener("loaded", function (e) {
    if (e.target === entityEl) {
      let popupCameraEl = document.querySelector("#popup-camera");
      popupCameraEl.setAttribute("camera", "active", true);
      // Puzzle types that are draggable
      if (componentDataParsed.hasOwnProperty("blackboardText")) {
        let blackboardTextEl = document.querySelector("#blackboardText");
        const blackboardText = componentDataParsed.blackboardText;
        const blackboardTextColor = componentDataParsed.hasOwnProperty(
          "blackboardTextColor"
        )
          ? componentDataParsed.blackboardTextColor
          : "white";

        // Without this, the text might be too large or small. The values can be adjusted if needed.
        const blackboardTextWidth = blackboardTextEl.getAttribute("text").width;
        const textWrapCount = Math.max(
          Math.min(blackboardText.length, 60),
          blackboardTextWidth + 5
        );

        blackboardTextEl.setAttribute("text", {
          color: blackboardTextColor,
          width: blackboardTextWidth,
          wrapCount: textWrapCount,
          value: blackboardText,
          font:
            "https://raw.githubusercontent.com/jaydhulia/aframe-fonts/master/fonts/poppins/Poppins-Bold.json",
          shader: "msdf",
        });
      }

      if (componentDataParsed.hasOwnProperty("blackboardParagraph")) {
        let blackboardParagraphEl = document.querySelector(
          "#blackboardParagraph"
        );
        const blackboardParagraph = componentDataParsed.blackboardParagraph;
        const blackboardParagraphColor = componentDataParsed.hasOwnProperty(
          "blackboardParagraphColor"
        )
          ? componentDataParsed.blackboardParagraphColor
          : "white";

        // TODO: Do we want paragraph text to be resizable like the title text?
        blackboardParagraphEl.setAttribute("text", {
          color: blackboardParagraphColor,
          value: blackboardParagraph,
          font:
            "https://raw.githubusercontent.com/jaydhulia/aframe-fonts/master/fonts/poppins/Poppins-Medium.json",
          shader: "msdf",
        });
      }

      if (
        componentDataParsed.hasOwnProperty("draggable") &&
        componentDataParsed.draggable
      ) {
        popupCameraEl.setAttribute("drag-controls", "objects: .draggable");
      }
    }
  });
  blackboardEl.appendChild(entityEl);
}
