# Components

Simple documentation for components being used and a sample of their `animations_json`.

The type of component is defined with the `componentType` field. The possible values are:

- `keypad`
- `text-pane`
- `rotation-controls`
- `visual-pane`

Below, the components are described in more detail.

## Keypad

- `animations_json` - object

  - `blackboardData`- object
    - `componentType` - Needs to be the string "keypad"
    - `jsonData` - object
      - `password` - Any 4-digit non-negative number.

- Sample mock object

```json
{
  ...
  "animations_json": {
    "blackboardData": {
      "componentType": "keypad",
      "jsonData": {
        "password": "1000"
      }
    }
  },
  ...
}
```

## Text Pane

- `animations_json` - object
  - `blackboardData`- object
    - `componentType` - Needs to be the string "text-pane"
    - `jsonData` - object
      - `text` - Array of strings to show.
      - `currPosition` - Starting element position in the array above.
- Sample mock object

```json
{
  ...
  "animations_json": {
      "blackboardData": {
        "componentType": "text-pane",
        "jsonData": {
          "text": [
            "Welcome to the Escape Room! This is a very loooooong sentence for testing. This is a test this is a test this is a test this is a test.",
            "This is where text will go. This is where text will go. This is where text will go",
            "This is some more text. This is some more text. This is some more text.",
            "This is the last text, clicking Done will close this in a later PR"
          ],
          "currPosition": 0
        }
      }
    },
  ...
}
```

## Rotation Controls

- `animations_json` - object
  - `blackboardData`- object
    - `componentType` - Needs to be the string "rotation-controls"
    - `jsonData` - object
      - `position` - Defines the distance of the object relative to the blackboard. Array of 3 floats: `[x, y, z]`
- Sample mock object

```json
{
  ...
  "animations_json": {
      "blackboardData": {
        "componentType": "rotation-controls",
        "jsonData": {
          "position": [0, 0, 5]
        }
      }
    },
  ...
}
```

## Visual Pane

- `animations_json` - object
  - `blackboardData`- object
    - `componentType` - Needs to be the string "visual-pane"
    - `jsonData` - object
      - `imageSrc` - A string URL pointing to the source of the image
      - `scaleBy` - A float value by which the image is scaled
      - `position` - Defines the distance of the object (image AND caption) relative to the blackboard. Array of 3 floats: `[x, y, z]`
      - `caption` - A string that is displayed below the image as a caption
- Sample mock object

```json
{
  ...
  "animations_json": {
      "blackboardData": {
        "componentType": "visual-pane",
        "jsonData": {
          "imageSrc": "/static/assets/dev/pic1.png",
          "scaleBy": 3,
          "position": [0, 0, 0],
          "caption": "Welcome to the Escape Room! This is a very loooooong sentence for testing. This is a test this is a test this is a test this is a test."
        }
      }
    },
  ...
}
```
