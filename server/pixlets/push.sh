echo "pushing to $DEVICE_ID"

pixlet render bird.star 
pixlet push $DEVICE_ID bird.webp 

pixlet render bird-summary.star 
pixlet push $DEVICE_ID -i "dailybird" bird-summary.webp
