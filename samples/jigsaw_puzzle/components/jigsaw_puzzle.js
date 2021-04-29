AFRAME.registerComponent("jigsaw-puzzle", {
  schema: {
    jsonData: {
      parse: JSON.parse,
      stringify: JSON.stringify,
    },
  },

  multiple: true,

  init: function () {
    const data = this.data.jsonData;
    const puzzleDimension = data.hasOwnProperty("puzzleDimension")
      ? data.puzzleDimension
      : 3;
    const images = [];
    const xCoord = Array.from(Array(puzzleDimension).keys()).map(
      (x) => x - (puzzleDimension / 2 - 1 / 2)
    );
    const yCoord = xCoord.slice(0).reverse();

    let puzzlePieceWidth, puzzlePieceHeight;
    let rawImageEl = document.createElement("img");

    this.ordered_puzzle = document.createElement("a-entity");
    this.ordered_puzzle.setAttribute("id", "ordered-puzzle");

    const ordered_puzzle = this.ordered_puzzle;
    const el = this.el;

    rawImageEl.onload = function () {
      const ratio = rawImageEl.width / rawImageEl.height;
      const scaleBy = data.hasOwnProperty("scaleBy") ? data.scaleBy : 3;
      puzzlePieceWidth = scaleBy * ratio;
      puzzlePieceHeight = scaleBy;

      let coordPairs = yCoord.flatMap((y) =>
        xCoord.map((x) => [x * puzzlePieceWidth, y * puzzlePieceHeight])
      );
      let randomCoordPairs = coordPairs.slice(0);
      shuffleArray(randomCoordPairs);

      for (i = 0; i < data.images.length; ++i) {
        let imageData = {};
        imageData["imageSrc"] = data.images[i];
        imageData["width"] = puzzlePieceWidth;
        imageData["height"] = puzzlePieceHeight;
        imageData["xTarget"] = coordPairs[i][0];
        imageData["yTarget"] = coordPairs[i][1];
        imageData["x"] = randomCoordPairs[i][0];
        imageData["y"] = randomCoordPairs[i][1];

        images.push(imageData);
      }

      ordered_puzzle_json = {
        images: images,
        useTargets: true,
        randomizePos: false,
      };

      ordered_puzzle.setAttribute(
        "ordered-puzzle",
        "jsonData",
        JSON.stringify(ordered_puzzle_json)
      );
      el.appendChild(ordered_puzzle);
    };

    rawImageEl.src = data.images[0];
  },
});

function shuffleArray(array) {
  for (i = array.length - 1; i > 0; i--) {
    let j = Math.floor(Math.random() * (i + 1));
    let temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
}
