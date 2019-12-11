#  Final Project Checkpoint

## Plan from last checkpoint

1. Mailer object
2. Unit tests!!! Im not sure why but the structure of my directory is not making travis happy
3. Practice demo and create architecture diagram 
4. Maybe add some extra strategies and symbols?

## Work Completed

The app is done! 

The mailer object is created and it being used by the DailyCheck object when it runs to email users

I got a few unit tests working, they aren't exhaustive but I just wanted the experience working with them and flask together.

I put the architecture diagram in the resources folder, I'm gonna create some slides for my presentation to go along with the demo. I tried to make the architecture pretty simple.

I didn't add any extra strategies or symbols, but I did add functionality for my demo where it will randomly select two currencies from a list and email me the bid and ask exchange rate every 10 seconds for them, so I can show that it does actually send emails based on time. 

Also, I realized I had a bug and was checking dates I had in as examples so I had to do some debugging and refactoring there but it is all good now. 

Finally, I did implement a Factory pattern for the strategy objects. There isn't really any new front-facing functionality, so no screenshots this time, but you'll get to see it in live action on Thursday!
