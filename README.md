Got to task 4 only, with not much testing in the code and the pixel counting is wrong...

For the open questions: 
7:
Simple test case: Create a image (or batch of images) with known pixel values and test that outpu match input. 
Complex: Create a batch of images with wrong pixel values, wrong batch size, wong images shapes (example samller then the squares) .. and check that the appropriate error messages show up

---
10: 
For deployment we could consider using ECS because we have a docker container. 
But I have no experiece with this so if I know this is pipeline is modular (in the sense that the defined input and output don't need additional logic), I would deploy on Lambda (because memory limits and processing time fit the lambda limits). 

--> On AWS I would create 1 (or 2) S3 bucket (object storage) to hold the images (raw and processed for tracebility) (assuming another pipeline is streaming the image to raw bucket). Then I would create a lambda with our code (using the AWS pandas layer should be enough otherwise package my own layers). 
The lambda would watch for events on the bucket (new file additions), and count the images available. If enough images for 5 batches of 20 images it will run the code in this git repo with following twists:

 1- The processed images would be stored in another bucket (using boto2)
 2 - I would add workers if we want to parrelalise the task. 
 3 - I would then inject the statist panda data frame to the relevant db tale (eg. using pyscopg2 if PostgreDb)
 4 - On succesful invoke I would add that the lambda send a message to relavant user using SNS (eg. email) 
 4 - Additionally on errors I would send errors to an SQS dead letter queue and pout a cloud watch alarm on the queue.  
 6 - Maek sure all the setup services have least privelege permissions with IAM
