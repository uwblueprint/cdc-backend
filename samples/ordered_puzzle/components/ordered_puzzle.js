AFRAME.registerComponent("ordered-puzzle", {
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
    const numPuzzlePieces = data.images.length;
    const blackboard = document.querySelector("#blackboard");
    this.puzzlePieceCache = [];

    if (data.useTargets) {
      // Create text label which indicates to users that they have successfully completed the puzzle
      this.solvedText = document.createElement("a-text");
      this.solvedText.setAttribute("id", "text");
      this.solvedText.setAttribute("value", "Solved!");
      this.solvedText.setAttribute("color", "green");
      this.solvedText.setAttribute("scale", "4 4 2");
      this.solvedText.setAttribute("align", "center");
      this.solvedText.setAttribute("visible", false);
      this.solvedText.setAttribute("position", {
        x: 0,
        y:
          -blackboard.getAttribute("geometry").height / 2 +
          this.solvedText.getAttribute("scale").y,
        z: 0.1,
      });
      this.el.appendChild(this.solvedText);
    }

    const solvedTextLabel = this.solvedText;
    const puzzlePieceCache = this.puzzlePieceCache;

    for (i = 0; i < numPuzzlePieces; i++) {
      this.puzzlePiece = document.createElement("a-image");
      this.puzzlePiece.setAttribute("id", "puzzle-piece-image-" + i);
      this.puzzlePiece.setAttribute("src", data.images[i].imageSrc);
      puzzlePieceCache.push(this.puzzlePiece);

      let rawImageEl = document.createElement("img");
      rawImageEl.setAttribute("index", i);

      rawImageEl.onload = function (event) {
        const index = event.target.getAttribute("index");
        const puzzlePiece = puzzlePieceCache[index];

        // Calculate the puzzle piece width and height based on image ratio
        const ratio = rawImageEl.width / rawImageEl.height;
        const scaleBy = data.hasOwnProperty("scaleBy") ? data.scaleBy : 3;
        let puzzlePieceWidth = scaleBy * ratio;
        let puzzlePieceHeight = scaleBy;
        puzzlePiece.setAttribute("width", puzzlePieceWidth);
        puzzlePiece.setAttribute("height", puzzlePieceHeight);
        puzzlePiece.setAttribute("class", "draggable link");

        if (data.randomizePos) {
          // Randomizes the position of the puzzle piece on the blackboard
          puzzlePiece.setAttribute("position", {
            x:
              (Math.random() - 0.5) *
              (blackboard.getAttribute("geometry").width - puzzlePieceWidth),
            y:
              (Math.random() - 0.5) *
              (blackboard.getAttribute("geometry").height - puzzlePieceHeight),
            z: 0,
          });
        } else {
          puzzlePiece.setAttribute("position", {
            x: data.images[index].x * puzzlePieceWidth,
            y: data.images[index].y * puzzlePieceHeight,
            z: 0,
          });
        }

        if (data.useTargets) {
          // Create target
          let textBoxProp = JSON.parse(JSON.stringify(data.images[index]));
          textBoxProp.color = "yellow";
          textBoxProp.width = puzzlePieceWidth;
          textBoxProp.height = puzzlePieceHeight;
          textBoxProp.xTarget = textBoxProp.xTarget * puzzlePieceWidth;
          textBoxProp.yTarget = textBoxProp.yTarget * puzzlePieceHeight;

          let target = document.createElement("a-entity");
          target.setAttribute("id", "puzzle-target-" + index);
          target.setAttribute(
            "target-box",
            "jsonData",
            JSON.stringify(textBoxProp)
          );
          el.appendChild(target);

          // Set image's target location
          puzzlePiece.setAttribute(
            "xTarget",
            data.images[index].xTarget * puzzlePieceWidth
          );
          puzzlePiece.setAttribute(
            "yTarget",
            data.images[index].yTarget * puzzlePieceHeight
          );
          puzzlePiece.setAttribute("onTarget", false);

          puzzlePiece.addEventListener("dragend", function (event) {
            event.target.setAttribute("onTarget", isOnTarget(event.target));
            if (isPuzzleComplete(puzzlePieceCache)) {
              solvedTextLabel.setAttribute("visible", "true");
            }
          });
        }

        el.appendChild(puzzlePiece);
      };
      rawImageEl.src = data.images[i].imageSrc;
    }

    if (data.useTargets) {
      // Once window is loaded, calculated if current puzzle pieces are on their target.
      window.addEventListener("load", function () {
        puzzlePieceCache.forEach((puzzlePiece) => {
          puzzlePiece.setAttribute("onTarget", isOnTarget(puzzlePiece));
        });
      });
    }
  },
});

function isOnTarget(puzzlePiece) {
  const delta = puzzlePiece.object3D.children[0].position;
  const originalPos = puzzlePiece.getAttribute("position");
  const targetPos = {
    x: puzzlePiece.getAttribute("xTarget"),
    y: puzzlePiece.getAttribute("yTarget"),
  };
  const accuracyReq = 1;
  return (
    Math.abs(originalPos["x"] + delta["x"] - targetPos["x"]) <= accuracyReq &&
    Math.abs(originalPos["y"] + delta["y"] - targetPos["y"]) <= accuracyReq
  );
}

function isPuzzleComplete(puzzlePieceCache) {
  for (var i = 0; i < puzzlePieceCache.length; i++) {
    if (puzzlePieceCache[i].getAttribute("onTarget") === "false") {
      return false;
    }
  }
  return true;
}

function closePuzzle() {
  var ordered_puzzle = document.querySelector("#ordered-puzzle");
  while (ordered_puzzle.firstChild) {
    ordered_puzzle.removeChild(ordered_puzzle.lastChild);
  }
}
