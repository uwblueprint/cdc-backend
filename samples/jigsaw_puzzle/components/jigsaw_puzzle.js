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
    const puzzleDimension = 3;
    const puzzlePieceWidth = 3;
    const puzzlePieceHeight = 3;
    const images = [];
    const coord = Array.from(Array(puzzleDimension).keys());
    const coordPairs = coord.flatMap((v) => coord.map((w) => [v, w]));

    let randomCoordPairs = coordPairs.slice(0);
    shuffleArray(randomCoordPairs);

    console.log(coordPairs);

    for (i = 0; i < data.images.length; ++i) {
      let imageData = {};
      imageData["imageSrc"] = data.images[i];
      imageData["width"] = puzzlePieceWidth;
      imageData["height"] = puzzlePieceHeight;
      imageData["xTarget"] = convertXCoordToBlackboardPos(
        coordPairs[i][0],
        puzzleDimension,
        puzzlePieceWidth
      );
      imageData["yTarget"] = convertYCoordToBlackboardPos(
        coordPairs[i][1],
        puzzleDimension,
        puzzlePieceHeight
      );
      imageData["x"] = convertXCoordToBlackboardPos(
        randomCoordPairs[i][0],
        puzzleDimension,
        puzzlePieceWidth
      );
      imageData["y"] = convertYCoordToBlackboardPos(
        randomCoordPairs[i][1],
        puzzleDimension,
        puzzlePieceHeight
      );
      console.log(
        "x: " +
          coordPairs[i][0] +
          ", y: " +
          coordPairs[i][1] +
          " => x: " +
          imageData["xTarget"] +
          ", y: " +
          imageData["yTarget"]
      );

      images.push(imageData);
    }

    ordered_puzzle_json = {
      images: images,
      useTargets: true,
      randomizePos: false,
    };

    console.log(ordered_puzzle_json);

    this.ordered_puzzle = document.createElement("a-entity");
    this.ordered_puzzle.setAttribute("id", "ordered-puzzle");
    this.ordered_puzzle.setAttribute(
      "ordered-puzzle",
      "jsonData",
      JSON.stringify(ordered_puzzle_json)
    );
    this.el.appendChild(this.ordered_puzzle);
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

function calculateOffset(dimension, length) {
  let offset;
  if (offset % 2 == 0) {
    offset = (dimension / 2 - 1) * length;
  } else {
    offset = Math.floor(dimension / 2) * length;
  }
  return offset;
}

function convertXCoordToBlackboardPos(coord, dimension, length) {
  return coord * length - calculateOffset(dimension, length);
}

function convertYCoordToBlackboardPos(coord, dimension, length) {
  return coord * -length + calculateOffset(dimension, length);
}
