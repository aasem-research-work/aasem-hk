#!/bin/bash

# Loop through all .ui files in the current directory
for ui_file in *.ui; do
  # Extract the filename without the extension
  filename=$(basename -- "$ui_file")
  filename_noext="${filename%.*}"
  
  # Convert .ui to .py using pyuic5
  pyuic5 -x "$ui_file" -o "${filename_noext}.py"
  
  echo "Converted $ui_file to ${filename_noext}.py"

  pyrcc5 res_main.qrc  -o res_main_rc.py 

  echo "res_main.qrc converted to res_main_rc.py"
done

echo "Conversion complete."
