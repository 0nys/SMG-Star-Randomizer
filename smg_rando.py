# **************************************
# * SUPER MARIO GALAXY STAR RANDOMIZER *
# **************************************
# by Onys
#
#
# This program gives you a random list of stars that you have to complete in
# that order in Super Mario Galaxy 1 in order to complete a given goal.
# This is not a mod, so it does not affect the game itself by any mean.
# The randomizer ensures that at any point in the list the next star is available,
# i.e. the player is never softlocked by the list of stars.
# However, regular comets and purple comets appearance may have to be triggered
# by the Comet Luma in order to be obtained.
#
# To use the randomizer:
# 	You can launch it with Python3 on a command line:
#		$ python3 smg_rando.py --goal=<goal>
# 	with <goal> being the objective of the randomizer.
# 	Three goals are available:
#		- <goal> = "any%" (beat the game by getting the Bowser's Galaxy Reactor star)
#		- <goal> = "100%" (get all 120 stars)
# 		- <goal> = "luigi%" (get all Luigi stars)
# 	You can also add three optional parameters to remove some stars from the logic:
# 		- --no-bits (removes stars that require to feed a Hungry Luma)
# 		- --no-luigi (removes all Luigi letter stars)
# 		- --no-comets (removes all comet (regular and purple) stars)
# 	The program creates a file `smg_rando.txt`, which contains
# 	the randomized list of stars.
# 	If the optional option --livesplit is given as well, smg_rando.txt is a split
# 	file readable by Livesplit

import random
import sys
import os
import getopt

star_names = [
	"Good_Egg_1", "Good_Egg_2", "Good_Egg_3", "Good_Egg_C", "Good_Egg_PC", "Good_Egg_?",
	"Honeyhive_1", "Honeyhive_2", "Honeyhive_3", "Honeyhive_C", "Honeyhive_PC", "Honeyhive_?",
	"Space_Junk_1", "Space_Junk_2", "Space_Junk_3", "Space_Junk_C", "Space_Junk_PC", "Space_Junk_?",
	"Battlerock_1", "Battlerock_2", "Battlerock_3", "Battlerock_C", "Battlerock_PC", "Battlerock_?", "Battlerock_G",
	"Beach_Bowl_1", "Beach_Bowl_2", "Beach_Bowl_3", "Beach_Bowl_C", "Beach_Bowl_PC", "Beach_Bowl_?",
	"Ghostly_1", "Ghostly_2", "Ghostly_3", "Ghostly_C", "Ghostly_PC", "Ghostly_?",
	"Gusty_Garden_1", "Gusty_Garden_2", "Gusty_Garden_3", "Gusty_Garden_C", "Gusty_Garden_PC", "Gusty_Garden_?",
	"Freezeflame_1", "Freezeflame_2", "Freezeflame_3", "Freezeflame_C", "Freezeflame_PC", "Freezeflame_?",
	"Dusty_Dune_1", "Dusty_Dune_2", "Dusty_Dune_3", "Dusty_Dune_C", "Dusty_Dune_PC", "Dusty_Dune_?", "Dusty_Dune_G",
	"Gold_Leaf_1", "Gold_Leaf_2", "Gold_Leaf_3", "Gold_Leaf_C", "Gold_Leaf_PC", "Gold_Leaf_?",
	"Sea_Slide_1", "Sea_Slide_2", "Sea_Slide_3", "Sea_Slide_C", "Sea_Slide_PC", "Sea_Slide_?",
	"Toy_Time_1", "Toy_Time_2", "Toy_Time_3", "Toy_Time_C", "Toy_Time_PC", "Toy_Time_?",
	"Deep_Dark_1", "Deep_Dark_2", "Deep_Dark_3", "Deep_Dark_C", "Deep_Dark_PC", "Deep_Dark_?",
	"Dreadnought_1", "Dreadnought_2", "Dreadnought_3", "Dreadnought_C", "Dreadnought_PC", "Dreadnought_?",
	"Melty_Molten_1", "Melty_Molten_2", "Melty_Molten_3", "Melty_Molten_C", "Melty_Molten_PC", "Melty_Molten_?",
	"Gateway", "Gateway_R",
	"Bowser_Jr.'s_Robot_Reactor",
	"Bowser's_Star_Reactor",
	"Bowser_Jr.'s_Airship_Armada",
	"Bowser's_Dark_Matter_Plant",
	"Bowser_Jr.'s_Lava_Reactor",
	"Bowser's_Galaxy_Reactor",
	"Loopdeeloop",
	"Flipswitch",
	"Rolling_Green",
	"Hurry_Scurry",
	"Bubble_Breeze",
	"Sweet_Sweet",
	"Sling_Pod",
	"Buoy_Base", "Buoy_Base_G",
	"Drip_Drop",
	"Boo's_Boneyard",
	"Honeyclimb",
	"Snow_Cap",
	"Bonefin",
	"Sand_Spiral",
	"Matter_Splatter",
	"Bigmouth",
	"Rolling_Gizmo",
	"Loopdeeswoop",
	"Bubble_Blast"
]

star_logic = {
	"Good_Egg_1" : ["star Gateway"],
	"Good_Egg_2" : ["star Good_Egg_1"],
	"Good_Egg_3" : ["star Good_Egg_2"],
	"Good_Egg_C" : ["geq 13", "star Good_Egg_1", "comet"],
	"Good_Egg_PC" : ["star Bowser's_Galaxy_Reactor", "comet"],
	"Good_Egg_?" : ["star Ghostly_1", "luigi"],
	"Honeyhive_1" : ["geq 3"],
	"Honeyhive_2" : ["star Honeyhive_1"],
	"Honeyhive_3" : ["star Honeyhive_2"],
	"Honeyhive_C" : ["geq 13", "star Honeyhive_1", "comet"],
	"Honeyhive_PC" : ["star Bowser's_Galaxy_Reactor", "star Honeyhive_1", "comet"],
	"Honeyhive_?" : ["geq 3", "star Battlerock_G", "luigi"],
	"Space_Junk_1" : ["geq 9", "star Bowser_Jr.'s_Robot_Reactor"],
	"Space_Junk_2" : ["star Space_Junk_1"],
	"Space_Junk_3" : ["star Space_Junk_2"],
	"Space_Junk_C" : ["geq 13", "star Space_Junk_1", "comet"],
	"Space_Junk_PC" : ["star Bowser's_Galaxy_Reactor", "star Space_Junk_2", "comet"],
	"Space_Junk_?" : ["star Space_Junk_2", "bits"],
	"Battlerock_1" : ["geq 12", "star Bowser_Jr.'s_Robot_Reactor"],
	"Battlerock_2" : ["star Battlerock_1"],
	"Battlerock_3" : ["star Battlerock_2"],
	"Battlerock_C" : ["geq 13", "star Battlerock_3", "comet"],
	"Battlerock_PC" : ["star Bowser's_Galaxy_Reactor", "star Battlerock_1", "comet"],
	"Battlerock_?" : ["star Battlerock_1"],
	"Battlerock_G" : ["geq 12", "star Good_Egg_?", "luigi"],
	"Beach_Bowl_1" : ["geq 16", "star Bowser's_Star_Reactor"],
	"Beach_Bowl_2" : ["star Beach_Bowl_1"],
	"Beach_Bowl_3" : ["star Beach_Bowl_2"],
	"Beach_Bowl_C" : ["star Beach_Bowl_3", "comet"],
	"Beach_Bowl_PC" : ["star Bowser's_Galaxy_Reactor", "star Beach_Bowl_3", "comet"],
	"Beach_Bowl_?" : ["star Beach_Bowl_1"],
	"Ghostly_1" : ["geq 20", "star Bowser's_Star_Reactor"],
	"Ghostly_2" : ["star Ghostly_1"],
	"Ghostly_3" : ["star Ghostly_2"],
	"Ghostly_C" : ["star Ghostly_3", "comet"],
	"Ghostly_PC" : ["star Bowser's_Galaxy_Reactor", "star Ghostly_2", "comet"],
	"Ghostly_?" : ["star Ghostly_1"],
	"Gusty_Garden_1" : ["geq 24", "star Bowser_Jr.'s_Airship_Armada"],
	"Gusty_Garden_2" : ["star Gusty_Garden_1"],
	"Gusty_Garden_3" : ["star Gusty_Garden_2"],
	"Gusty_Garden_C" : ["star Gusty_Garden_3", "comet"],
	"Gusty_Garden_PC" : ["star Bowser's_Galaxy_Reactor", "star Gusty_Garden_1", "comet"],
	"Gusty_Garden_?" : ["star Gusty_Garden_2"],
	"Freezeflame_1" : ["geq 26", "star Bowser_Jr.'s_Airship_Armada"],
	"Freezeflame_2" : ["star Freezeflame_1"],
	"Freezeflame_3" : ["star Freezeflame_2"],
	"Freezeflame_C" : ["star Freezeflame_1", "comet"],
	"Freezeflame_PC" : ["star Bowser's_Galaxy_Reactor", "star Freezeflame_1", "comet"],
	"Freezeflame_?" : ["geq 26", "star Bowser_Jr.'s_Airship_Armada"],
	"Dusty_Dune_1" : ["geq 29", "star Bowser_Jr.'s_Airship_Armada"],
	"Dusty_Dune_2" : ["star Dusty_Dune_1"],
	"Dusty_Dune_3" : ["star Dusty_Dune_2"],
	"Dusty_Dune_C" : ["star Dusty_Dune_3", "comet"],
	"Dusty_Dune_PC" : ["star Bowser's_Galaxy_Reactor", "star Dusty_Dune_2", "comet"],
	"Dusty_Dune_?" : ["star Dusty_Dune_2"],
	"Dusty_Dune_G" : ["star Dusty_Dune_1", "bits"],
	"Gold_Leaf_1" : ["geq 34", "star Bowser's_Dark_Matter_Plant"],
	"Gold_Leaf_2" : ["star Gold_Leaf_1"],
	"Gold_Leaf_3" : ["star Gold_Leaf_2"],
	"Gold_Leaf_C" : ["star Gold_Leaf_3", "comet"],
	"Gold_Leaf_PC" : ["star Bowser's_Galaxy_Reactor", "star Gold_Leaf_3", "comet"],
	"Gold_Leaf_?" : ["star Gold_Leaf_1"],
	"Sea_Slide_1" : ["geq 36", "star Bowser's_Dark_Matter_Plant"],
	"Sea_Slide_2" : ["star Sea_Slide_1"],
	"Sea_Slide_3" : ["star Sea_Slide_2"],
	"Sea_Slide_C" : ["star Sea_Slide_1", "comet"],
	"Sea_Slide_PC" : ["star Bowser's_Galaxy_Reactor", "star Sea_Slide_3", "comet"],
	"Sea_Slide_?" : ["star Sea_Slide_2", "bits"],
	"Toy_Time_1" : ["geq 40", "star Bowser's_Dark_Matter_Plant"],
	"Toy_Time_2" : ["star Toy_Time_1"],
	"Toy_Time_3" : ["star Toy_Time_2"],
	"Toy_Time_C" : ["star Toy_Time_?", "comet"],
	"Toy_Time_PC" : ["star Bowser's_Galaxy_Reactor", "star Toy_Time_2", "comet"],
	"Toy_Time_?" : ["star Toy_Time_1", "bits"],
	"Deep_Dark_1" : ["geq 46", "star Bowser_Jr.'s_Lava_Reactor"],
	"Deep_Dark_2" : ["star Deep_Dark_1"],
	"Deep_Dark_3" : ["star Deep_Dark_2"],
	"Deep_Dark_C" : ["star Deep_Dark_2", "comet"],
	"Deep_Dark_PC" : ["star Bowser's_Galaxy_Reactor", "star Deep_Dark_1", "comet"],
	"Deep_Dark_?" : ["geq 46", "star Bowser_Jr.'s_Lava_Reactor"],
	"Dreadnought_1" : ["geq 48", "star Bowser_Jr.'s_Lava_Reactor"],
	"Dreadnought_2" : ["star Dreadnought_1"],
	"Dreadnought_3" : ["star Dreadnought_2"],
	"Dreadnought_C" : ["star Dreadnought_3", "comet"],
	"Dreadnought_PC" : ["star Bowser's_Galaxy_Reactor", "star Dreadnought_2", "comet"],
	"Dreadnought_?" : ["star Dreadnought_2"],
	"Melty_Molten_1" : ["geq 52", "star Bowser_Jr.'s_Lava_Reactor"],
	"Melty_Molten_2" : ["star Melty_Molten_1"],
	"Melty_Molten_3" : ["star Melty_Molten_2"],
	"Melty_Molten_C" : ["star Melty_Molten_2", "comet"],
	"Melty_Molten_PC" : ["star Bowser's_Galaxy_Reactor", "star Melty_Molten_3", "comet"],
	"Melty_Molten_?" : ["geq 52", "star Bowser_Jr.'s_Lava_Reactor", "bits"],
	"Gateway" : [],
	"Gateway_R" : ["star Bowser_Jr.'s_Lava_Reactor"],
	"Bowser_Jr.'s_Robot_Reactor" : ["geq 8"],
	"Bowser's_Star_Reactor" : ["geq 15", "star Bowser_Jr.'s_Robot_Reactor"],
	"Bowser_Jr.'s_Airship_Armada" : ["geq 23", "star Bowser's_Star_Reactor"],
	"Bowser's_Dark_Matter_Plant" : ["geq 33", "star Bowser_Jr.'s_Airship_Armada"],
	"Bowser_Jr.'s_Lava_Reactor" : ["geq 45", "star Bowser's_Dark_Matter_Plant"],
	"Bowser's_Galaxy_Reactor" : ["geq 60", "star Bowser's_Dark_Matter_Plant"],
	"Loopdeeloop" : ["geq 5"],
	"Flipswitch" : ["geq 7"],
	"Rolling_Green" : ["geq 11", "star Bowser_Jr.'s_Robot_Reactor"],
	"Hurry_Scurry" : ["geq 18", "star Bowser_Jr.'s_Robot_Reactor"],
	"Bubble_Breeze" : ["geq 19", "star Bowser's_Star_Reactor"],
	"Sweet_Sweet" : ["geq 7", "bits"],
	"Sling_Pod" : ["star Space_Junk_3", "bits"],
	"Buoy_Base" : ["geq 30", "star Beach_Bowl_1"],
	"Buoy_Base_G" : ["geq 30", "star Beach_Bowl_1"],
	"Drip_Drop" : ["star Beach_Bowl_1", "bits"],
	"Boo's_Boneyard" : ["star Ghostly_1", "star Gateway_R", "bits"],
	"Honeyclimb" : ["geq 42", "star Bowser_Jr.'s_Airship_Armada"],
	"Snow_Cap" : ["star Melty_Molten_1", "bits"],
	"Bonefin" : ["geq 55", "star Drip_Drop"],
	"Sand_Spiral" : ["star Ghostly_1", "star Sea_Slide_2", "bits"],
	"Matter_Splatter" : ["geq 50", "star Toy_Time_1", "star Bowser_Jr.'s_Lava_Reactor"],
	"Bigmouth" : ["star Dusty_Dune_1", "bits"],
	"Rolling_Gizmo" : ["star Battlerock_G", "star Buoy_Base_G", "star Dusty_Dune_G"],
	"Loopdeeswoop" : ["star Battlerock_G", "star Buoy_Base_G", "star Dusty_Dune_G"],
	"Bubble_Blast" : ["star Battlerock_G", "star Buoy_Base_G", "star Dusty_Dune_G"]
}

star_description = {
	"Good_Egg_1" : "Good Egg 1 - Terrace",
	"Good_Egg_2" : "Good Egg 2 - Terrace",
	"Good_Egg_3" : "Good Egg 3 - Terrace",
	"Good_Egg_C" : "Good Egg Comet (red) - Terrace",
	"Good_Egg_PC" : "Good Egg Purple Comet - Terrace",
	"Good_Egg_?" : "Good Egg Secret (Luigi 1) - Terrace",
	"Honeyhive_1" : "Honeyhive 1 - Terrace",
	"Honeyhive_2" : "Honeyhive 2 - Terrace",
	"Honeyhive_3" : "Honeyhive 3 - Terrace",
	"Honeyhive_C" : "Honeyhive Comet (blue) - Terrace",
	"Honeyhive_PC" : "Honeyhive Purple Comet - Terrace",
	"Honeyhive_?" : "Honeyhive Secret (Luigi 3) - Terrace",
	"Space_Junk_1" : "Space Junk 1 - Fountain",
	"Space_Junk_2" : "Space Junk 2 - Fountain",
	"Space_Junk_3" : "Space Junk 3 - Fountain",
	"Space_Junk_C" : "Space Junk Comet (red) - Fountain",
	"Space_Junk_PC" : "Space Junk Purple Comet - Fountain",
	"Space_Junk_?" : "Space Junk Secret (50 bits) - Fountain",
	"Battlerock_1" : "Battlerock 1 - Fountain",
	"Battlerock_2" : "Battlerock 2 - Fountain",
	"Battlerock_3" : "Battlerock 3 - Fountain",
	"Battlerock_C" : "Battlerock Comet (white) - Fountain",
	"Battlerock_PC" : "Battlerock Purple Comet - Fountain",
	"Battlerock_?" : "Battlerock Secret - Fountain",
	"Battlerock_G" : "Battlerock Green (Luigi 2) - Fountain",
	"Beach_Bowl_1" : "Beach Bowl 1 - Kitchen",
	"Beach_Bowl_2" : "Beach Bowl 2 - Kitchen",
	"Beach_Bowl_3" : "Beach Bowl 3 - Kitchen",
	"Beach_Bowl_C" : "Beach Bowl Comet (yellow) - Kitchen",
	"Beach_Bowl_PC" : "Beach Bowl Purple Comet - Kitchen",
	"Beach_Bowl_?" : "Beach Bowl Secret - Kitchen",
	"Ghostly_1" : "Ghostly 1 - Kitchen",
	"Ghostly_2" : "Ghostly 2 - Kitchen",
	"Ghostly_3" : "Ghostly 3 - Kitchen",
	"Ghostly_C" : "Ghostly Comet (white) - Kitchen",
	"Ghostly_PC" : "Ghostly Purple Comet - Kitchen",
	"Ghostly_?" : "Ghostly Secret - Kitchen",
	"Gusty_Garden_1" : "Gusty Garden 1 - Bedroom",
	"Gusty_Garden_2" : "Gusty Garden 2 - Bedroom",
	"Gusty_Garden_3" : "Gusty Garden 3 - Bedroom",
	"Gusty_Garden_C" : "Gusty Garden Comet (white) - Bedroom",
	"Gusty_Garden_PC" : "Gusty Garden Purple Comet - Bedroom",
	"Gusty_Garden_?" : "Gusty Garden Secret - Bedroom",
	"Freezeflame_1" : "Freezeflame 1 - Bedroom",
	"Freezeflame_2" : "Freezeflame 2 - Bedroom",
	"Freezeflame_3" : "Freezeflame 3 - Bedroom",
	"Freezeflame_C" : "Freezeflame Comet (blue) - Bedroom",
	"Freezeflame_PC" : "Freezeflame Purple Comet - Bedroom",
	"Freezeflame_?" : "Freezeflame Secret - Bedroom",
	"Dusty_Dune_1" : "Dusty Dune 1 - Bedroom",
	"Dusty_Dune_2" : "Dusty Dune 2 - Bedroom",
	"Dusty_Dune_3" : "Dusty Dune 3 - Bedroom",
	"Dusty_Dune_C" : "Dusty Dune Comet (red) - Bedroom",
	"Dusty_Dune_PC" : "Dusty Dune Purple Comet - Bedroom",
	"Dusty_Dune_?" : "Dusty Dune Secret - Bedroom",
	"Dusty_Dune_G" : "Dusty Dune Green (20 bits) - Bedroom",
	"Gold_Leaf_1" : "Gold Leaf 1 - Engine Room",
	"Gold_Leaf_2" : "Gold Leaf 2 - Engine Room",
	"Gold_Leaf_3" : "Gold Leaf 3 - Engine Room",
	"Gold_Leaf_C" : "Gold Leaf Comet (blue) - Engine Room",
	"Gold_Leaf_PC" : "Gold Leaf Purple Comet - Engine Room",
	"Gold_Leaf_?" : "Gold Leaf Secret - Engine Room",
	"Sea_Slide_1" : "Sea Slide 1 - Engine Room",
	"Sea_Slide_2" : "Sea Slide 2 - Engine Room",
	"Sea_Slide_3" : "Sea Slide 3 - Engine Room",
	"Sea_Slide_C" : "Sea Slide Comet (blue) - Engine Room",
	"Sea_Slide_PC" : "Sea Slide Purple Comet - Engine Room",
	"Sea_Slide_?" : "Sea Slide Secret (40 bits) - Engine Room",
	"Toy_Time_1" : "Toy Time 1 - Engine Room",
	"Toy_Time_2" : "Toy Time 2 - Engine Room",
	"Toy_Time_3" : "Toy Time 3 - Engine Room",
	"Toy_Time_C" : "Toy Time Comet (yellow) - Engine Room",
	"Toy_Time_PC" : "Toy Time Purple Comet - Engine Room",
	"Toy_Time_?" : "Toy Time Secret (50 bits) - Engine Room",
	"Deep_Dark_1" : "Deep Dark 1 - Garden",
	"Deep_Dark_2" : "Deep Dark 2 - Garden",
	"Deep_Dark_3" : "Deep Dark 3 - Garden",
	"Deep_Dark_C" : "Deep Dark Comet (white) - Garden",
	"Deep_Dark_PC" : "Deep Dark Purple Comet - Garden",
	"Deep_Dark_?" : "Deep Dark Secret - Garden",
	"Dreadnought_1" : "Dreadnought 1 - Garden",
	"Dreadnought_2" : "Dreadnought 2 - Garden",
	"Dreadnought_3" : "Dreadnought 3 - Garden",
	"Dreadnought_C" : "Dreadnought Comet (red) - Garden",
	"Dreadnought_PC" : "Dreadnought Purple Comet - Garden",
	"Dreadnought_?" : "Dreadnought Secret - Garden",
	"Melty_Molten_1" : "Melty Molten 1 - Garden",
	"Melty_Molten_2" : "Melty Molten 2 - Garden",
	"Melty_Molten_3" : "Melty Molten 3 - Garden",
	"Melty_Molten_C" : "Melty Molten Comet (white) - Garden",
	"Melty_Molten_PC" : "Melty Molten Purple Comet - Garden",
	"Melty_Molten_?" : "Melty Molten Secret (80 bits) - Garden",
	"Gateway" : "Gateway",
	"Gateway_R" : "Gateway Red",
	"Bowser_Jr.'s_Robot_Reactor" : "Bowser Jr.'s Robot Reactor - Terrace",
	"Bowser's_Star_Reactor" : "Bowser's Star Reactor - Fountain",
	"Bowser_Jr.'s_Airship_Armada" : "Bowser Jr.'s Airship Armada - Kitchen",
	"Bowser's_Dark_Matter_Plant" : "Bowser's Dark Matter Plant - Bedroom",
	"Bowser_Jr.'s_Lava_Reactor" : "Bowser Jr.'s Lava Reactor - Engine Room",
	"Bowser's_Galaxy_Reactor" : "Bowser's Galaxy Reactor (the end)",
	"Loopdeeloop" : "Loopdeeloop - Terrace",
	"Flipswitch" : "Flipswitch - Terrace",
	"Rolling_Green" : "Rolling Green - Fountain",
	"Hurry_Scurry" : "Hurry Scurry - Fountain",
	"Bubble_Breeze" : "Bubble Breeze - Kitchen",
	"Sweet_Sweet" : "Sweet Sweet (400 bits) - Terrace",
	"Sling_Pod" : "Sling Pod (400 bits) - Fountain",
	"Buoy_Base" : "Buoy Base - Kitchen",
	"Buoy_Base_G" : "Buoy Base Green - Kitchen",
	"Drip_Drop" : "Drip Drop (600 bits) - Kitchen",
	"Boo's_Boneyard" : "Boo's Boneyard (1200 bits) - Gateway",
	"Honeyclimb" : "Honeyclimb - Bedroom",
	"Snow_Cap" : "Snow Cap (1600 bits) - Garden",
	"Bonefin" : "Bonefin - Engine Room",
	"Sand_Spiral" : "Sand Spiral (1000 bits) - Engine Room",
	"Matter_Splatter" : "Matter Splatter - Garden",
	"Bigmouth" : "Bigmouth (800 bits) - Bedroom",
	"Rolling_Gizmo" : "Rolling Gizmo - Trials",
	"Loopdeeswoop" : "Loopdeeswoop - Trials",
	"Bubble_Blast" : "Bubble Blast - Trials"
}

taken_stars = {}
for star in star_names :
	taken_stars[star] = False

nb_stars = 0
luigi_counter = 0

goals = ["any%", "100%", "luigi%"]
luigi_stars = ["Ghostly_1", "Good_Egg_?", "Battlerock_G", "Honeyhive_?"]

no_luigi = False
no_bits = False
no_comets = False
goal = goals[0] #default
livesplit = False


def in_logic(star) :

	if taken_stars[star]: return False
	
	for req in star_logic[star]:
		req_l = req.split(" ")
		req_type = req_l[0]
		if req_type == "geq":
			if nb_stars < int(req_l[1]): return False
		elif req_type == "star":
			if not taken_stars[req_l[1]]: return False
		elif req_type == "luigi":
			if luigi_counter > 0 or no_luigi: return False
		elif req_type == "comet":
			if no_comets: return False
		elif req_type == "bits":
			if no_bits: return False
		else:
			print("ERROR: wrong requirement type: " + req_type)
		
	return True


def rando(goal_stars, all_stars=False):
	
	# Global stuff
	global luigi_counter
	global nb_stars
	
	star_list = []
	goal_reached = False
	while not goal_reached:
		
		# Choose a star
		star_is_goal = False
		for goal_star in goal_stars:
			if in_logic(goal_star):
				star = goal_star # give priority to objective stars
				star_is_goal = True
		if not star_is_goal: # no star has priority
			star = random.choice(star_names)
			while not in_logic(star) :
				star = random.choice(star_names)
		
		# Take the star
		taken_stars[star] = True
		# Luigi management
		if star in luigi_stars:
			luigi_counter = 5
		else:
			luigi_counter = max(luigi_counter-1, 0)
		star_list.append(star)
		nb_stars += 1
		
		# Check the end
		if all_stars:
			if nb_stars == 120: goal_reached = True
		else:
			goal_reached = True
			for goal_star in goal_stars:
				if not taken_stars[goal_star]:
					goal_reached = False
	
	return star_list


def create_line_livesplit(i_star):
	return '<Segment><Name>{}</Name><Icon /><SplitTimes><SplitTime name="Personal Best" /></SplitTimes><BestSegmentTime /><SegmentHistory /></Segment>'.format(star_description[star_list[i_star]])






def dic_of_options(options):
    dic = {}
    for opt, v in options :
        dic[opt] = v
    return dic

# Read the parameters
try :
	options, _ = getopt.getopt(sys.argv[1:], "", ["goal=", "no-bits", "no-luigi", "no-comets", "livesplit"])
	dic = dic_of_options(options)
	no_bits = "--no-bits" in dic
	no_luigi = "--no-luigi" in dic
	no_comets = "--no-comets" in dic
	livesplit = "--livesplit" in dic
	if dic["--goal"] not in goals:
		print("ERROR: goal " + dic["--goal"] + " not recognized.")
		print("The recognized goals are :\n" + "\n".join(goals))
		exit()
	goal = dic["--goal"]
except getopt.GetoptError as err:
    print("ERROR: " + str(err))
except KeyError as err:
    print("ERROR: missing parameter " + str(err))



if goal == "any%":
	star_list = rando(["Bowser's_Galaxy_Reactor"])
elif goal == "100%":
	if no_bits or no_luigi or no_comets:
		print("ERROR: cannot remove any star from 100%")
		exit()
	star_list = rando([], True)
elif goal == "luigi%":
	if no_luigi:
		print("ERROR: cannot remove Luigi stars from Luigi%")
		exit()
	star_list = rando(luigi_stars)
else:
	print("ERROR: your computer has virus")


f = open("smg_rando.txt", "w+")

if livesplit:
	f.write('<?xml version="1.0" encoding="UTF-8"?><Run version="1.7.0"><GameIcon /><GameName>Super Mario Galaxy</GameName><CategoryName>Random%</CategoryName><Metadata><Run id="" /><Platform usesEmulator="False"></Platform><Region></Region><Variables /></Metadata><Offset>00:00:00</Offset><AttemptCount>0</AttemptCount><AttemptHistory /><Segments>')

	for i_star in range(len(star_list)):
		f.write(create_line_livesplit(i_star))

	f.write("</Segments><AutoSplitterSettings /></Run>)")

else:
	for i_star in range(len(star_list)):
		f.write(str(i_star+1) + " - " + star_description[star_list[i_star]] + "\n")

f.close()
