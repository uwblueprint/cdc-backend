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
    const puzzlePieceCache = [];
    const blackboard = document.querySelector("#blackboard");

    for (i = 0; i < numPuzzlePieces; i++) {
      if (data.useTargets) {
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
      }

      this.puzzlePiece = document.createElement("a-image");
      this.puzzlePiece.setAttribute("id", "puzzle-piece-image-" + i);
      this.puzzlePiece.setAttribute("src", data.images[i].imageSrc);
      this.puzzlePiece.setAttribute("width", data.images[i].width);
      this.puzzlePiece.setAttribute("height", data.images[i].height);

      // Randomizes the position of the puzzle piece on the blackboard
      this.puzzlePiece.setAttribute(
        "position",
        (Math.random() - 0.5) *
          (blackboard.getAttribute("geometry").width - data.images[i].width) +
          " " +
          (Math.random() - 0.5) *
            (blackboard.getAttribute("geometry").height -
              data.images[i].height) +
          " 0"
      );
      this.puzzlePiece.setAttribute("xTarget", data.images[i].xTarget);
      this.puzzlePiece.setAttribute("yTarget", data.images[i].yTarget);
      this.puzzlePiece.setAttribute("onTarget", false);
      this.puzzlePiece.setAttribute("class", "draggable link");
      if (data.useTargets) {
        this.puzzlePiece.addEventListener("dragend", function (event) {
          event.target.setAttribute("onTarget", isOnTarget(event.target));
          if (isPuzzleComplete(puzzlePieceCache)) {
            closePuzzle();
          }
        });
      }

      this.el.appendChild(this.puzzlePiece);
      puzzlePieceCache.push(this.puzzlePiece);
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
