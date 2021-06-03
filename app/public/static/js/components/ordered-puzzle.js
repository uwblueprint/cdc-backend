AFRAME.registerComponent("ordered-puzzle", {
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
    this.id = data.id;
    this.useTargets = data.useTargets;
    const is_last_object =
      "is_last_object" in data ? data.is_last_object : false;

    const numPuzzlePieces = data.images.length;
    const blackboard = document.querySelector("#blackboard");
    this.puzzlePieceCache = [];

    if (data.useTargets) {
      // Create text label which indicates to users that they have successfully completed the puzzle
      const solvedPuzzleText = {
        width: "5",
        height: "1",
        depth: "1",
        color: "green",
        x: "0",
        y: "-5.75",
        z: "0",
        scaleX: "4",
        scaleY: "4",
        scaleZ: "2",
        text: "Solved",
      };
      // Create solved puzzle text
      this.solvedPuzzleEntity = document.createElement("a-entity");
      this.solvedPuzzleEntity.setAttribute(
        "id",
        "ordered-puzzle-solved-" + this.id
      );
      this.solvedPuzzleEntity.setAttribute(
        "text-box",
        "jsonData",
        JSON.stringify(solvedPuzzleText)
      );
      // initially set to false visibility
      this.solvedPuzzleEntity.setAttribute("visible", "false");
      el.appendChild(this.solvedPuzzleEntity);
    } else {
      // if there is no targets then this puzzle is already solved
      // emit event to update state
      el.sceneEl.emit("solvedObject", { id: data.id });
    }

    const puzzlePieceCache = this.puzzlePieceCache;
    const scaleBy = data.hasOwnProperty("scaleBy") ? data.scaleBy : 3;

    for (i = 0; i < numPuzzlePieces; i++) {
      this.puzzlePiece = document.createElement("a-image");
      this.puzzlePiece.setAttribute("id", "puzzle-piece-image-" + i);
      this.puzzlePiece.setAttribute(
        "src",
        data.images[i].imageSrc + "?d=" + new Date().getTime() / 1000
      );
      puzzlePieceCache.push(this.puzzlePiece);

      let rawImageEl = document.createElement("img");
      rawImageEl.setAttribute("index", i);

      rawImageEl.onload = function (event) {
        const index = event.target.getAttribute("index");
        const puzzlePiece = puzzlePieceCache[index];

        // Calculate the puzzle piece width and height based on image ratio
        const ratio = rawImageEl.width / rawImageEl.height;
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
            event.target.setAttribute(
              "onTarget",
              isOnTarget(event.target, scaleBy)
            );
            if (isPuzzleComplete(puzzlePieceCache)) {
              // emit event to update state
              el.sceneEl.emit("solvedObject", { id: data.id });
              // emit event to close popup (after 1 second for now) - TODO: disabled for now
              // need designer input on whether we should autoclose this
              // el.sceneEl.emit("dcc-success-close-popup", { seconds: 1 });
              // emit event if it is last object, to indicate scene is solved
              if (is_last_object) {
                el.sceneEl.emit("dcc-success-close-popup", {
                  seconds: 2,
                  is_last_object: is_last_object,
                });
              }
            }
          });

          puzzlePiece.addEventListener("loaded", function () {
            puzzlePiece.setAttribute(
              "onTarget",
              isOnTarget(puzzlePiece, scaleBy)
            );
          });
        }

        el.appendChild(puzzlePiece);
      };
      rawImageEl.crossOrigin = "anonymous";
      rawImageEl.src = data.images[i].imageSrc + "?d=" + new Date().getTime();
    }
  },
  update: function () {
    this.puzzleIsSolved = this.data.isSolved[this.id];

    if (typeof this.puzzleIsSolved === "undefined") {
      // not loaded yet, do nothing
    } else if (this.puzzleIsSolved === true && this.useTargets) {
      // Already solved
      this.solvedPuzzleEntity.setAttribute("visible", "true");
    } else {
      // not solved yet, do nothing for now
    }
  },
});

function isOnTarget(puzzlePiece, scaleBy) {
  const delta = puzzlePiece.object3D.children[0].position;
  const originalPos = puzzlePiece.getAttribute("position");
  const targetPos = {
    x: puzzlePiece.getAttribute("xTarget"),
    y: puzzlePiece.getAttribute("yTarget"),
  };
  const accuracyReq = scaleBy / 3;
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
