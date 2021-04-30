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
    // Creates possible x coordinates centred at 0
    const xCoord = Array.from(Array(puzzleDimension).keys()).map(
      (x) => (x - (puzzleDimension / 2 - 1 / 2)) * 1.1
    );
    // Creates possible y coordinates centred at 0
    const yCoord = xCoord.slice(0).reverse();

    // Creates possible (x,y) coordinates
    let coordPairs = yCoord.flatMap((y) => xCoord.map((x) => [x, y]));
    // Randomize the starting position of the puzzle pieces
    let randomCoordPairs = coordPairs.slice(0);
    shuffleArray(randomCoordPairs);
    let images = [];

    for (i = 0; i < data.images.length; ++i) {
      let imageData = {};
      imageData["imageSrc"] = data.images[i];
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
      scaleBy: data.hasOwnProperty("scaleBy") ? data.scaleBy : 3,
    };

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
