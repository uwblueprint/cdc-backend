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

    for (i = 0; i < numPuzzlePieces; i++) {
      var textBoxProp =
        '{"width": "' +
        data.images[i].width +
        '", "height": "' +
        data.images[i].height +
        '", "color": "yellow", "x": "' +
        data.images[i].xTarget +
        '", "y": "' +
        data.images[i].yTarget +
        '", "z": "0", "text": "' +
        i +
        '"}';

      this.target = document.createElement("a-entity");
      this.target.setAttribute("id", "puzzle-target");
      this.target.setAttribute("target-box", "jsonData", textBoxProp);
      this.el.appendChild(this.target);

      this.puzzlePiece = document.createElement("a-image");
      this.puzzlePiece.setAttribute("id", "puzzle-piece-image");
      this.puzzlePiece.setAttribute("src", data.images[i].imageSrc);
      this.puzzlePiece.setAttribute("width", data.images[i].width);
      this.puzzlePiece.setAttribute("height", data.images[i].height);
      this.puzzlePiece.setAttribute(
        "position",
        data.images[i].x + " " + data.images[i].y + " 0"
      );
      this.puzzlePiece.setAttribute("xTarget", data.images[i].xTarget);
      this.puzzlePiece.setAttribute("yTarget", data.images[i].yTarget);
      this.puzzlePiece.setAttribute("onTarget", false);
      this.puzzlePiece.setAttribute("class", "draggable");
      this.puzzlePiece.addEventListener("dragend", onDragEnd);
      this.el.appendChild(this.puzzlePiece);
    }
  },
});

function onDragEnd(event) {
  event.target.setAttribute("onTarget", isOnTarget(event.target));
  if (isPuzzleComplete()) {
    closePuzzle();
  }
}

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

function isPuzzleComplete() {
  var puzzlePieces = document.querySelectorAll("a-image.draggable");
  //var puzzlePieces = document.querySelector("#ordered-puzzle").children;
  console.log(puzzlePieces);
  for (var i = 0; i < puzzlePieces.length; i++) {
    if (puzzlePieces[i].getAttribute("onTarget") === "false") {
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
