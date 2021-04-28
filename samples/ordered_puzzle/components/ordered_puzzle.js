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

    for (i = 0; i < numPuzzlePieces; i++) {
      this.puzzlePiece = document.createElement("a-image");
      this.puzzlePiece.setAttribute("id", "puzzle-piece-image-" + i);
      this.puzzlePiece.setAttribute("src", data.images[i].imageSrc);
      this.puzzlePiece.setAttribute("width", data.images[i].width);
      this.puzzlePiece.setAttribute("height", data.images[i].height);
      this.puzzlePiece.setAttribute("class", "draggable link");

      if (data.randomizePos) {
        // Randomizes the position of the puzzle piece on the blackboard
        this.puzzlePiece.setAttribute("position", {
          x:
            (Math.random() - 0.5) *
            (blackboard.getAttribute("geometry").width - data.images[i].width),
          y:
            (Math.random() - 0.5) *
            (blackboard.getAttribute("geometry").height -
              data.images[i].height),
          z: 0,
        });
      } else {
        this.puzzlePiece.setAttribute("position", {
          x: data.images[i].x,
          y: data.images[i].y,
          z: 0,
        });
      }

      if (data.useTargets) {
        // Create target
        var textBoxProp = data.images[i];
        textBoxProp.color = "yellow";

        this.target = document.createElement("a-entity");
        this.target.setAttribute("id", "puzzle-target-" + i);
        this.target.setAttribute(
          "target-box",
          "jsonData",
          JSON.stringify(textBoxProp)
        );
        this.el.appendChild(this.target);

        // Set image's target location
        this.puzzlePiece.setAttribute("xTarget", data.images[i].xTarget);
        this.puzzlePiece.setAttribute("yTarget", data.images[i].yTarget);
        this.puzzlePiece.setAttribute("onTarget", false);
        const solvedTextLabel = this.solvedText;
        this.puzzlePiece.addEventListener("dragend", function (event) {
          event.target.setAttribute("onTarget", isOnTarget(event.target));
          if (isPuzzleComplete(puzzlePieceCache)) {
            solvedTextLabel.setAttribute("visible", "true");
          }
        });
      }

      this.el.appendChild(this.puzzlePiece);

      this.puzzlePieceCache.push(this.puzzlePiece);
    }

    const puzzlePieceCache = this.puzzlePieceCache;

    window.addEventListener("load", function () {
      puzzlePieceCache.forEach((puzzlePiece) => {
        puzzlePiece.setAttribute("onTarget", isOnTarget(puzzlePiece));
      });
    });
  },
});

function isOnTarget(puzzlePiece) {
  const delta =
    puzzlePiece.object3D.children.length != 0
      ? puzzlePiece.object3D.children[0].position
      : { x: 0, y: 0, z: 0 };
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
