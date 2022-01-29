#! /bin/bash

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
cd ../app/public/static/assets

# for future reference
echo "" > fileschanged.txt

for file in $(find . -size +4M -name "*.glb")
do
  oldname=$(echo $file | sed 's/.\///g')
  mv "$file" ./old_"$oldname"
  gltf-pipeline -i ./old_"$oldname" -d -o "$file"
  echo "$file" >> fileschanged.txt
done