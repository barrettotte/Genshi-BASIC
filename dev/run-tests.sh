#!/bin/bash
pushd . > /dev/null
pushd lib/GenshiBASIC > /dev/null
echo "Running all test cases..."
python3 -m unittest discover
popd > /dev/null 
popd > /dev/null
echo Done.