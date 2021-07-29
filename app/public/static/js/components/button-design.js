AFRAME.registerComponent("button-design", {
  init: function () {
    this.hovering = false;
    this.el.addEventListener("raycaster-intersected", (evt) => {
      this.hovering = true;
    });
    this.el.addEventListener("raycaster-intersected-cleared", (evt) => {
      this.hovering = false;
      this.el.children[0].setAttribute("color", "white");
    });
  },

  tick: function () {
    if (!this.hovering) {
      return;
    }
    this.el.children[0].setAttribute("color", "#6d6d6d");
  },
});
