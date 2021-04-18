THREE.TransformControls = function (camera, domElement) {
  if (domElement === undefined) {
    console.warn(
      'THREE.TransformControls: The second parameter "domElement" is now mandatory.'
    );
    domElement = document;
  }

  THREE.Object3D.call(this);

  this.visible = false;
  this.domElement = domElement;

  var _plane = new THREE.TransformControlsPlane();
  this.add(_plane);

  var scope = this;

  // Define properties with getters/setter
  // Setting the defined property will automatically trigger change event
  // Defined properties are passed down to gizmo and plane

  defineProperty("camera", camera);
  defineProperty("object", undefined);
  defineProperty("enabled", true);
  defineProperty("axis", null);
  defineProperty("mode", "translate");
  defineProperty("translationSnap", null);
  defineProperty("rotationSnap", null);
  defineProperty("scaleSnap", null);
  defineProperty("space", "world");
  defineProperty("size", 1);
  defineProperty("dragging", false);
  defineProperty("showX", true);
  defineProperty("showY", true);
  defineProperty("showZ", true);

  var changeEvent = { type: "change" };
  var mouseDownEvent = { type: "mouseDown" };
  var mouseUpEvent = { type: "mouseUp", mode: scope.mode };
  var objectChangeEvent = { type: "objectChange" };

  // Reusable utility variables

  var raycaster = new THREE.Raycaster();

  function intersectObjectWithRay(object, raycaster, includeInvisible) {
    var allIntersections = raycaster.intersectObject(object, true);

    for (var i = 0; i < allIntersections.length; i++) {
      if (allIntersections[i].object.visible || includeInvisible) {
        return allIntersections[i];
      }
    }

    return false;
  }

  var _tempVector = new THREE.Vector3();
  var _tempQuaternion = new THREE.Quaternion();

  var pointStart = new THREE.Vector3();
  var pointEnd = new THREE.Vector3();
  var offset = new THREE.Vector3();
  var rotationAxis = new THREE.Vector3();
  var rotationAngle = 0;

  var cameraPosition = new THREE.Vector3();
  var cameraQuaternion = new THREE.Quaternion();
  var cameraScale = new THREE.Vector3();

  var parentPosition = new THREE.Vector3();
  var parentQuaternion = new THREE.Quaternion();
  var parentQuaternionInv = new THREE.Quaternion();
  var parentScale = new THREE.Vector3();

  var worldPositionStart = new THREE.Vector3();
  var worldQuaternionStart = new THREE.Quaternion();
  var worldScaleStart = new THREE.Vector3();

  var worldPosition = new THREE.Vector3();
  var worldQuaternion = new THREE.Quaternion();
  var worldQuaternionInv = new THREE.Quaternion();
  var worldScale = new THREE.Vector3();

  var eye = new THREE.Vector3();

  var quaternionStart = new THREE.Quaternion();

  // TODO: remove properties unused in plane and gizmo

  defineProperty("worldPosition", worldPosition);
  defineProperty("worldPositionStart", worldPositionStart);
  defineProperty("worldQuaternion", worldQuaternion);
  defineProperty("worldQuaternionStart", worldQuaternionStart);
  defineProperty("cameraPosition", cameraPosition);
  defineProperty("cameraQuaternion", cameraQuaternion);
  defineProperty("pointStart", pointStart);
  defineProperty("pointEnd", pointEnd);
  defineProperty("rotationAxis", rotationAxis);
  defineProperty("rotationAngle", rotationAngle);
  defineProperty("eye", eye);

  {
    domElement.addEventListener("pointerdown", onPointerDown, false);
    domElement.addEventListener("pointermove", onPointerHover, false);
    scope.domElement.ownerDocument.addEventListener(
      "pointerup",
      onPointerUp,
      false
    );
  }

  this.dispose = function () {
    domElement.removeEventListener("pointerdown", onPointerDown);
    domElement.removeEventListener("pointermove", onPointerHover);
    scope.domElement.ownerDocument.removeEventListener(
      "pointermove",
      onPointerMove
    );
    scope.domElement.ownerDocument.removeEventListener(
      "pointerup",
      onPointerUp
    );

    this.traverse(function (child) {
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
    });
    this.detach();
  };

  // Set current object
  this.attach = function (object) {
    this.object = object;
    this.visible = true;

    return this;
  };

  // Detatch from object
  this.detach = function () {
    this.object = undefined;
    this.visible = false;
    this.axis = null;

    return this;
  };

  // Defined getter, setter and store for a property
  function defineProperty(propName, defaultValue) {
    var propValue = defaultValue;

    Object.defineProperty(scope, propName, {
      get: function () {
        return propValue !== undefined ? propValue : defaultValue;
      },

      set: function (value) {
        if (propValue !== value) {
          propValue = value;
          _plane[propName] = value;

          scope.dispatchEvent({ type: propName + "-changed", value: value });
          scope.dispatchEvent(changeEvent);
        }
      },
    });

    scope[propName] = defaultValue;
    _plane[propName] = defaultValue;
  }

  // updateMatrixWorld  updates key transformation variables
  this.updateMatrixWorld = function () {
    if (this.object !== undefined) {
      this.object.updateMatrixWorld();

      if (this.object.parent === null) {
        console.error(
          "TransformControls: The attached 3D object must be a part of the scene graph."
        );
      } else {
        this.object.parent.matrixWorld.decompose(
          parentPosition,
          parentQuaternion,
          parentScale
        );
      }

      this.object.matrixWorld.decompose(
        worldPosition,
        worldQuaternion,
        worldScale
      );

      parentQuaternionInv.copy(parentQuaternion).invert();
      worldQuaternionInv.copy(worldQuaternion).invert();
    }

    this.camera.updateMatrixWorld();
    this.camera.matrixWorld.decompose(
      cameraPosition,
      cameraQuaternion,
      cameraScale
    );

    eye.copy(cameraPosition).sub(worldPosition).normalize();

    THREE.Object3D.prototype.updateMatrixWorld.call(this);
  };

  this.pointerHover = function (pointer) {
    if (this.object === undefined || this.dragging === true) return;

    raycaster.setFromCamera(pointer, this.camera);

    var intersect = intersectObjectWithRay(this.object, raycaster);
    // var intersect = intersectObjectWithRay(_gizmo.picker[this.mode], raycaster);
    if (intersect) {
      this.axis = "XYZE";
    } else {
      this.axis = null;
    }
  };

  this.pointerDown = function (pointer) {
    if (
      this.object === undefined ||
      this.dragging === true ||
      pointer.button !== 0
    )
      return;

    if (this.axis !== null) {
      raycaster.setFromCamera(pointer, this.camera);

      var planeIntersect = intersectObjectWithRay(_plane, raycaster, true);

      if (planeIntersect) {
        if (this.mode === "rotate") {
          var snap = this.rotationSnap;

          if (this.axis === "X" && snap)
            this.object.rotation.x =
              Math.round(this.object.rotation.x / snap) * snap;
          if (this.axis === "Y" && snap)
            this.object.rotation.y =
              Math.round(this.object.rotation.y / snap) * snap;
          if (this.axis === "Z" && snap)
            this.object.rotation.z =
              Math.round(this.object.rotation.z / snap) * snap;
        }

        this.object.updateMatrixWorld();
        this.object.parent.updateMatrixWorld();

        quaternionStart.copy(this.object.quaternion);

        this.object.matrixWorld.decompose(
          worldPositionStart,
          worldQuaternionStart,
          worldScaleStart
        );

        pointStart.copy(planeIntersect.point).sub(worldPositionStart);
      }

      this.dragging = true;
      mouseDownEvent.mode = this.mode;
      this.dispatchEvent(mouseDownEvent);
    }
  };

  this.pointerMove = function (pointer) {
    var axis = this.axis;
    var mode = this.mode;
    var object = this.object;

    if (
      object === undefined ||
      axis === null ||
      this.dragging === false ||
      pointer.button !== -1
    )
      return;

    raycaster.setFromCamera(pointer, this.camera);

    var planeIntersect = intersectObjectWithRay(_plane, raycaster, true);

    if (!planeIntersect) return;

    pointEnd.copy(planeIntersect.point).sub(worldPositionStart);

    if (mode === "rotate") {
      offset.copy(pointEnd).sub(pointStart);

      var ROTATION_SPEED =
        5 /
        worldPosition.distanceTo(
          _tempVector.setFromMatrixPosition(this.camera.matrixWorld)
        );

      if (axis === "XYZE") {
        rotationAxis.copy(offset).cross(eye).normalize();
        rotationAngle =
          offset.dot(_tempVector.copy(rotationAxis).cross(this.eye)) *
          ROTATION_SPEED;
      }

      // Apply rotation snap

      if (this.rotationSnap)
        rotationAngle =
          Math.round(rotationAngle / this.rotationSnap) * this.rotationSnap;

      this.rotationAngle = rotationAngle;

      // Apply rotate
      if (axis === "XYZE") {
        rotationAxis.applyQuaternion(parentQuaternionInv);
        object.quaternion.copy(
          _tempQuaternion.setFromAxisAngle(rotationAxis, rotationAngle)
        );
        object.quaternion.multiply(quaternionStart).normalize();
      }
    }

    this.dispatchEvent(changeEvent);
    this.dispatchEvent(objectChangeEvent);
  };

  this.pointerUp = function (pointer) {
    if (pointer.button !== 0) return;

    if (this.dragging && this.axis !== null) {
      mouseUpEvent.mode = this.mode;
      this.dispatchEvent(mouseUpEvent);
    }

    this.dragging = false;
    this.axis = null;
  };

  // normalize mouse / touch pointer and remap {x,y} to view space.

  function getPointer(event) {
    if (scope.domElement.ownerDocument.pointerLockElement) {
      return {
        x: 0,
        y: 0,
        button: event.button,
      };
    } else {
      var pointer = event.changedTouches ? event.changedTouches[0] : event;

      var rect = domElement.getBoundingClientRect();

      return {
        x: ((pointer.clientX - rect.left) / rect.width) * 2 - 1,
        y: (-(pointer.clientY - rect.top) / rect.height) * 2 + 1,
        button: event.button,
      };
    }
  }

  // mouse / touch event handlers

  function onPointerHover(event) {
    if (!scope.enabled) return;

    switch (event.pointerType) {
      case "mouse":
      case "pen":
        scope.pointerHover(getPointer(event));
        break;
    }
  }

  function onPointerDown(event) {
    if (!scope.enabled) return;

    scope.domElement.style.touchAction = "none"; // disable touch scroll
    scope.domElement.ownerDocument.addEventListener(
      "pointermove",
      onPointerMove,
      false
    );

    scope.pointerHover(getPointer(event));
    scope.pointerDown(getPointer(event));
  }

  function onPointerMove(event) {
    if (!scope.enabled) return;

    scope.pointerMove(getPointer(event));
  }

  function onPointerUp(event) {
    if (!scope.enabled) return;

    scope.domElement.style.touchAction = "";
    scope.domElement.ownerDocument.removeEventListener(
      "pointermove",
      onPointerMove,
      false
    );

    scope.pointerUp(getPointer(event));
  }

  // TODO: deprecate

  this.getMode = function () {
    return scope.mode;
  };

  this.setMode = function (mode) {
    scope.mode = mode;
  };

  this.setRotationSnap = function (rotationSnap) {
    scope.rotationSnap = rotationSnap;
  };

  this.setSize = function (size) {
    scope.size = size;
  };

  this.setSpace = function (space) {
    scope.space = space;
  };

  this.update = function () {
    console.warn(
      "THREE.TransformControls: update function has no more functionality and therefore has been deprecated."
    );
  };
};

THREE.TransformControls.prototype = Object.assign(
  Object.create(THREE.Object3D.prototype),
  {
    constructor: THREE.TransformControls,

    isTransformControls: true,
  }
);

THREE.TransformControlsPlane = function () {
  "use strict";

  THREE.Mesh.call(
    this,
    new THREE.PlaneBufferGeometry(100000, 100000, 2, 2),
    new THREE.MeshBasicMaterial({
      visible: false,
      wireframe: true,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.1,
      toneMapped: false,
    })
  );

  this.type = "TransformControlsPlane";

  var unitX = new THREE.Vector3(1, 0, 0);
  var unitY = new THREE.Vector3(0, 1, 0);
  var unitZ = new THREE.Vector3(0, 0, 1);

  var tempVector = new THREE.Vector3();
  var dirVector = new THREE.Vector3();
  var alignVector = new THREE.Vector3();
  var tempMatrix = new THREE.Matrix4();
  var identityQuaternion = new THREE.Quaternion();

  this.updateMatrixWorld = function () {
    this.position.copy(this.worldPosition);

    unitX.set(1, 0, 0).applyQuaternion(identityQuaternion);
    unitY.set(0, 1, 0).applyQuaternion(identityQuaternion);
    unitZ.set(0, 0, 1).applyQuaternion(identityQuaternion);

    // Align the plane for current transform mode, axis and space.

    alignVector.copy(unitY);

    dirVector.set(0, 0, 0);

    if (dirVector.length() === 0) {
      // If in rotate mode, make the plane parallel to camera
      this.quaternion.copy(this.cameraQuaternion);
    } else {
      tempMatrix.lookAt(tempVector.set(0, 0, 0), dirVector, alignVector);

      this.quaternion.setFromRotationMatrix(tempMatrix);
    }

    THREE.Object3D.prototype.updateMatrixWorld.call(this);
  };
};

THREE.TransformControlsPlane.prototype = Object.assign(
  Object.create(THREE.Mesh.prototype),
  {
    constructor: THREE.TransformControlsPlane,

    isTransformControlsPlane: true,
  }
);
