echo "pushing to $DEVICE_ID"

pixlet render bird-summary.star 
pixlet push $DEVICE_ID -i "dailybird" bird-summary.webp
