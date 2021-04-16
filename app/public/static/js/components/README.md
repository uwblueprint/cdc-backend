# Components

Simple documentation for components being used and a sample of their `animations_json`:

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
      - `rotation` - Defines the initial orientation of the object relative to the blackboard. Array of 3 floats: `[x, y, z]`
- Sample mock object

```json
{
  ...
  "animations_json": {
      "blackboardData": {
        "componentType": "rotation-controls",
        "jsonData": {
          "position": [0, 0, 5],
          "rotation": [0, 0, 0]
        }
      }
    },
  ...
}
```
