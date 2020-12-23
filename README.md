# Final Project: Cosmic Vapor Valley
Allison Kim
---

## Description
I made a very basic farming simulator! I was... inspired by Stardew Valley, which I put quite the number of hours into last year.

But it was fun! I ended up procrastinating on all of my other work for this because it ended up being really fun. Anyways, here's the basic features:

* Plant, water, and harvest strawberries!
  * Use your tools to care for your crops!
    * You have to water your plants every day for them to grow!!
  * Inventory
* Sell them for monies!
  * Currency
* Time-based
  * One hour passes every 3 seconds! :^)
  * The lighting of the screen changes as the day goes on!
  * You can be up from 6AM-10PM, but you'll automatically have to sleep if you stay up!
* Limited energy
  * A person only has so much energy to do things in a day...
  * So you start out with 30 energy!!
* Load/save games!
  * Although rudimentary, it works. :P


## Installation instructions
The game only requires the third-party package `pygame`, so run the following line:

`pip install pygame`

But also, I'm not entirely sure, but I think Python3 is probably required.

## How to play

Didn't have time to implement instructions so:

* `1`: Seeds for planting
* `2`: Watering can
* `3`: Sickle for harvesting
* `space bar`: for skipping to the next day
* `p`: for selling crops in your inventory

And just click on the tiles to interact with them!

## Code Structure
I have the following files:
* game.py
  * the main file!!
  * This defines the main Game class!
  * Methods are for
    * displaying the screen and refreshing at the right framerate
      * all the `draw` methods!
    * Listening for mouse clicks and keyboard presses and updating the files accordingly
    * Saving and loading game state
      * This is where I use the `pickle` import to save and load the game file.
      * Based on the inputted name, either a new game is made with the farmer name or the existing file will be loaded.
* constants.py
* farm.py
  * Defines the Tile class, which stores information about the tile's agricultural properties
    * is watered?
    * crop (optional)
    * how many days until the crop is ripe!
    * Methods are for interacting with the tile
      * planting
      * watering
      * harvesting
* crop.py
  * Defines the Crop class model, which stores informationabout the crop
* farmer.py
  * Defines the Farmer class which stores the relevant information for a farmer
    * inventory
    * money
    * active item (Tool)
* tools.py
  * Defines the Tool class and tool ids for identification
* loaders.py
  * The intention was to have multiple loaders for images, properties, and different items
    * these loaders would only load information as needed
  * This is where I use the `json` import to get the information about the crops from the `crops.json` file. Right now, there's only the strawberries, but this way, it's scalable!
* constants.py
  * This file just contains some useful constants that I can simply change to affect the game as needed