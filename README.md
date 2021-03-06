# Basic-Chatbot-with-text-voice-and-visual-IO

Searching AI Chatbots on the Web, I found no visual capabilities.  I felt visual input is crucial in the 21st century, so I've added webcam access to Eliza, a basic AI script from my child hood created in the mid 1960s by Joseph Weizenbaum in an MIT AI project.  Its a very basic chatbot for this example of applying features using Tensorflowjs and Mobilenet.

This project includes inspiration and functionality from the Tensorflow Group and one of their project https://github.com/tensorflow/tfjs-examples/tree/master/mobilenet.  Other contributing projects include https://github.com/jhuckaby/webcamjs and modified interface from https://github.com/bwilcox-1234/ChatScript.  Of the many versions and varriations of Eliza, I've chosen this clean python conversion from https://www.smallsurething.com/implementing-the-famous-eliza-chatbot-in-python/.

The tensorflow Mobilenet model I'm using isn't ideal in that even with 1000 items to suggest, it doesn't recognize people or faces, and may be subject to suggesting that you are a cockatoo. Incorporating object detection would help the overall usage but the last I tried with YOLO(ver1) it was too resource intensive. Have fun!

You can find a demo of this project here:  http://ioegg.com/sandi/sandi.php

![sandi](https://user-images.githubusercontent.com/40084298/42117405-dec82e4e-7bc1-11e8-8174-537901091f6e.jpg)
