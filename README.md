# LogicGates
Creating computers from AND and NOT, inspired by Sebastian Lague : https://www.youtube.com/watch?v=QZwneRb-zqA

## SCREENSHOT:
![solarized palette](https://github.com/Yeb02/LogicGates/blob/main/screenshot.png)


## USER INSTRUCTIONS:  
-Run logic.py
-Make sure units.txt is closed while logic.py is running
-Line 427, replace False by True if you want the blocks you created to be erased when you will launch the script again (remove an anwanted block manually in the units.txt file).  
-Select a block in green on the bottom left, displace it by clicking on it.   
-Click on a node and release on another to link them. If you click on a node from the input block, it will only change it's value. To link those, select another node first.  
-Click on an input node to delete its connection.  
-An output node can be linked to several input nodes.  
-Press the button to register a field's input on the top left. 
-Press the create button to create a bloc from what is on the screen.  
-Press the clear button to clear the workbench.   


## BUGS (TODO):  
-Change input/output block's size before linking their nodes.   
-Blocks can't be removed yet (except by clearing the whole workbench)  
-Do not create unnamed blocks, or give the same name to different blocks, and use only letters.     
-Sometimes connections do not update, displace a block to force update if the results on screen are not the ones expected.   

