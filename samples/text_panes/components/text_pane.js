var currPos = 0;

AFRAME.registerComponent("text_pane", {
  schema: {
    text: {
      default: ["hello from text_pane"],
      parse: function (value) {
        return value.split(",");
      },
    },
  },

  multiple: true,

  init: function () {
    var textEl = document.querySelector("#text");
    textEl.setAttribute("value", this.data.text[currPos]);
    console.log(this.data.text[currPos]);
  },

  update: function (direction) {
    if (currPos == 0 || currPos == text.length - 1) {
      currPos += direction;
      return true;
    }
    return false;
  },

  retrieve_text: function () {
    return this.data.text[currPos];
  },
});
