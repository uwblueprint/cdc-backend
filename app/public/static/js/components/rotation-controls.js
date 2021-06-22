AFRAME.registerComponent("rotation-controls", {
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
    let { TransformControls } = THREE;
    let { el } = this;
    let self = this;
    let obj = el.object3D;
    let sceneEl = el.sceneEl;
    let scene = sceneEl.object3D;
    let renderer = sceneEl.renderer;
    let camera, controls;
    let childId = data.id;

    let childEl = document.getElementById(childId);
    el.setAttribute("gltf-model", childEl.getAttribute("src"));

    el.setAttribute("rotation", childEl.getAttribute("rotation"));

    // TODO: Is scaling needed?
    if (data.hasOwnProperty("position")) {
      el.setAttribute("position", {
        x: data.position[0],
        y: data.position[1],
        z: data.position[2],
      });
    } else {
      el.setAttribute("position", { x: 0, y: 2, z: 0.5 });
    }
    if (data.hasOwnProperty("scale")) {
      el.setAttribute("scale", {
        x: data.scale[0],
        y: data.scale[1],
        z: data.scale[2],
      });
    } else {
      el.setAttribute("scale", childEl.getAttribute("scale"));
    }

    el.addEventListener("loaded", function (e) {
      if (e.target === el) {
        let cameraEl = document.querySelector("[camera]");

        let controlsSetup = function () {
          camera = sceneEl.camera;
          renderer.setPixelRatio(window.devicePixelRatio);
          renderer.setSize(window.innerWidth, window.innerHeight);
          document.body.appendChild(renderer.domElement);

          controls = new TransformControls(camera, renderer.domElement);
          controls.addEventListener("change", render);
          controls.addEventListener("dragging-changed", function (event) {
            cameraEl.setAttribute(
              "look-controls",
              "enabled",
              `${!event.value}`
            );
          });
          controls.attach(obj);
          scene.add(controls);

          window.addEventListener("resize", onWindowResize);

          controls.setMode("rotate");
          Object.assign(self, {
            camera,
            controls,
          });
        };

        if (sceneEl.camera === undefined) {
          sceneEl.addEventListener("camera-set-active", controlsSetup, {
            once: true,
          });
        } else {
          controlsSetup();
        }
      }
    });

    function onWindowResize() {
      const aspect = window.innerWidth / window.innerHeight;

      camera.aspect = aspect;
      camera.updateProjectionMatrix();

      renderer.setSize(window.innerWidth, window.innerHeight);

      render();
    }

    function render() {
      renderer.render(scene, camera);
    }
  },
  remove: function () {
    this.controls.dispose();
  },
});
