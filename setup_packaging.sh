#!/bin/bash

if [ -d ./dependencies ]
then 
	echo Found dependencies directory... deleting it.
	rm -r ./dependencies
else
  mkdir ./dependencies
fi

echo installing dependencies ask-sdk, untangle to folder dependencies
pip3 install --target ./dependencies ask-sdk-model ask-sdk-core untangle

echo entering dependencies and zipping contents...
cd ./dependencies
zip -rq ./dependencies *

echo bye
