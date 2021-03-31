AFRAME.registerComponent("animation-on-click-run", {
  schema: {
    extraInformation: { type: "string" },
  },
  dependencies: ["animation__onclick"],

  init: function () {
    var extraInfo = this.data.extraInformation;
    this.el.addEventListener("animationbegin", function (e) {
      // do nothing for now, will be added later, if needed
    });

    this.el.addEventListener("animationcomplete", function (e) {
      if (e.detail.name === "animation__onclick") {
        // Call Dhruvin's function
        alert("Object with ID " + extraInfo + " clicked");
      }
    });
  },
});
