AFRAME.registerComponent("rotation-controls", {
  init: function () {
    let { TransformControls } = THREE;
    let { el } = this;
    let self = this;
    let obj = el.object3D;
    let sceneEl = el.sceneEl;
    let scene = sceneEl.object3D;
    let renderer = sceneEl.renderer;
    let camera, controls;

    let cameraEl = document.querySelector("[camera]");

    let controlsSetup = function () {
      camera = sceneEl.camera;
      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.setSize(window.innerWidth, window.innerHeight);
      document.body.appendChild(renderer.domElement);

      controls = new TransformControls(camera, renderer.domElement);
      controls.addEventListener("change", render);
      controls.addEventListener("dragging-changed", function (event) {
        cameraEl.setAttribute("look-controls", "enabled", `${!event.value}`);
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
