AFRAME.registerComponent("tutorial-instructions", {
  multiple: true,

  init: function () {
    this.buttons = ["a", "w", "s", "d"];
    this.dir = ["left", "forward", "backward", "right"];
    const el = this.el;
    this.cur_idx = 0;
    this.keyDownHandle = this.keyDownHandle.bind(this);

    // Create textLabel
    this.textLabel = document.createElement("a-text");
    this.textLabel.setAttribute("id", "text-instructions");
    this.textLabel.setAttribute(
      "value",
      'Press "' +
        this.buttons[this.cur_idx] +
        '" to move ' +
        this.dir[this.cur_idx]
    );
    this.textLabel.setAttribute(
      "font",
      "https://raw.githubusercontent.com/jaydhulia/aframe-fonts/master/fonts/poppins/Poppins-Medium.json"
    );
    this.textLabel.setAttribute("shader", "msdf");
    this.textLabel.setAttribute("color", "white");
    this.textLabel.setAttribute("align", "center");
    this.textLabel.setAttribute("position", { x: 0, y: 0, z: -1 });
    this.textLabel.setAttribute("width", 1);

    el.appendChild(this.textLabel);
    window.addEventListener("keydown", this.keyDownHandle);
  },
  keyDownHandle: function (e) {
    const buttons = this.buttons;
    const dir = this.dir;
    if (e.key === buttons[this.cur_idx]) {
      // Correct key pressed, nice job!
      this.cur_idx++;
      if (this.cur_idx < buttons.length) {
        // still keys left
        this.textLabel.setAttribute(
          "value",
          'Press "' + buttons[this.cur_idx] + '" to move ' + dir[this.cur_idx]
        );
      } else {
        // remove event handler since this component is done
        window.removeEventListener("keydown", this.keyDownHandle);
        // keys done, proceed to next tutorial task
        const tutorial_keypress_transition_data = {
          data: [
            {
              text:
                "Great job! You can also pan around the room by clicking and dragging your mouse. During the escape room, you will have to interact with various objects to solve puzzles or get clues. To interact, click on the textbook (on teacher's desk) with your left mouse button. Give it a try!",
            },
          ],
          currPosition: 0,
        };
        tutorial_keypress_transition_data["isTransition"] = false;
        addTransition(tutorial_keypress_transition_data);
        this.textLabel.setAttribute(
          "value",
          "Click on the textbook (on teacher's desk)!"
        );
        const bookEl = document.getElementById("9-obj");
        bookEl.setAttribute("class", "link");
        bookEl.setAttribute("visible", "true");
      }
    }
  },
});
