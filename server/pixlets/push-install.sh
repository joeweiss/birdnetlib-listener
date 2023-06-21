echo "pushing to $DEVICE_ID"

pixlet render bird-summary.star 
pixlet push $DEVICE_ID -i "dailybird" bird-summary.webp

pixlet render bird-least-common.star 
pixlet push $DEVICE_ID -i "leastcommonbird" bird-least-common.webp

pixlet render bird-most-common.star 
pixlet push $DEVICE_ID -i "mostcommonbird" bird-most-common.webp
