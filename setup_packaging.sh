#!/bin/bash

if [ -d ./dependencies ]
then 
	echo Found dependencies directory... deleting it.
	rm -r ./dependencies
fi

echo installing dependencies ask-sdk, untangle to folder dependencies
pip install --target ./dependencies ask-sdk untangle

echo entering dependencies and zipping contents...
cd ./dependencies
zip -rq ./dependencies *

echo bye
