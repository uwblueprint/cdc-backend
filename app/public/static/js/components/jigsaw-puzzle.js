AFRAME.registerComponent("jigsaw-puzzle", {
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
    //TODO : UNDO THIS AND FIX IT UP
    el.setAttribute("scale", { x: 0.6, y: 0.6, z: 0.6 });
    el.setAttribute("position", "y", 1.5);
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

    //TODO : UNDO THIS TOO LATER
    ordered_puzzle_json = {
      id: this.id,
      images: images,
      useTargets: true,
      randomizePos: false,
      scaleBy: data.hasOwnProperty("scaleBy") ? 3 : 3,
      is_last_object: "is_last_object" in data ? data.is_last_object : false,
    };

    this.ordered_puzzle = document.createElement("a-entity");
    this.ordered_puzzle.setAttribute("id", "ordered-puzzle");
    this.ordered_puzzle.setAttribute(
      "ordered-puzzle",
      "jsonData",
      JSON.stringify(ordered_puzzle_json)
    );
    this.ordered_puzzle.setAttribute(
      "bind__ordered-puzzle",
      "isSolved: solvedObjects"
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
