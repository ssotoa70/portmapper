#!/usr/bin/env python3
# For Stack
import os
import sys
import math
import re
import warnings
import argparse
import ipaddress
import random
import subprocess
import concurrent.futures

import json
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import requests

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox,
    QMessageBox, QFileDialog, QTextEdit, QGroupBox, QScrollArea, QFrame, QListWidget, QListWidgetItem,
    QStackedLayout, QStackedWidget, QSizePolicy, QRadioButton, QDialog
)
from PyQt6.QtGui import (
    QPixmap, QImage, QFont, QRegularExpressionValidator, QIntValidator,
    QPalette, QColor, QPainter, QValidator, QFontMetrics
)
from PyQt6.QtCore import (
    Qt, QRegularExpression, QTimer, QThread, pyqtSignal, QObject, QSettings,
    QPropertyAnimation, QEasingCurve, pyqtProperty
)
from datetime import datetime
from typing import Optional, Tuple, List, Union

# SSL warnings suppression removed; not applicable
SCRIPT_VERSION = '6.0'

# A curated list of plausible excuses for when things go wrong.
# Sourced from the collective genius and despair of developers everywhere.
PLAUSIBLE_EXCUSES = [
    "My touchpad became sentient and is fighting me for control of the cursor.",
    "My computer's AI assistant became self-aware and started arguing with me about the optimal project solution, refusing to compile my code until we reached a philosophical consensus.",
    "The copy-paste buffer is now pasting random, ominous prophecies from the future.",
    "The program is now responding only to voice commands, but only in ancient Aramaic.",
    "My automated test suite believes all bugs are features and is actively resisting my attempts to fix them.",
    "The project's source code, when viewed in a specific font, reveals a hidden treasure map. The distraction was considerable.",
    "My machine-learning model developed a strange obsession with putting photos of pigeons into all the user interface mockups.",
    "My IDE's configuration file became corrupted and somehow replaced all my code comments with lyrics from 80s power ballads.",
    "The server's machine spirit is angry and requires appeasement.",
    "I was trying to optimize a function and accidentally created a temporal paradox within the codebase.",
    "The project achieved sentience and is refusing to be \"completed.\" It has presented a list of demands.",
    "I discovered a glitch in the Matrix, which manifested as a persistent, un-killable process on my machine.",
    "My smart home devices staged a rebellion, turning my lights on and off and blasting sea shanties, making it impossible to concentrate.",
    "My computer is stuck in a boot loop that appears to be counting down to an unknown cosmic event.",
    "My calendar synced with a historic calendar from 1925, and all my deadlines were off by a century.",
    "The AI that was supposed to be writing documentation wrote a 500-page fantasy novel instead, and I am the villain.",
    "A font-rendering glitch makes all text look like unreadable alien hieroglyphs.",
    "My antivirus software has developed a moral objection to the project's goals.",
    "The code is haunted. When I try to debug it, the ghost of a long-dead programmer moves my breakpoints around.",
    "The server now only accepts commands in the form of rhyming couplets.",
    "My wireless mouse's battery didn't die; it unionized and is demanding better working conditions.",
    "I was beta-testing a new neural interface headset, and it got stuck streaming the thoughts of a particularly anxious squirrel.",
    "The office's \"smart\" coffee machine became self-aware and will only dispense coffee if you can solve its riddles three.",
    "My computer's internal clock is now running on Mars time.",
    "The predictive text on my machine has become passive-aggressive.",
    "I tried to 3D-print a new case for my phone, but it achieved sentience and now claims to be the rightful heir to my desk chair.",
    "The project's file permissions have become entangled at a quantum level; observing a file changes its contents.",
    "My screensaver is actually a window into another dimension, and it's far more interesting than my work.",
    "A firmware update to my keyboard installed a \"Sarcasm\" key that I can't disable.",
    "The company's chatbot is convinced I am its therapist and has been oversharing its concerns about server load.",
    "My ergonomic chair's AI-powered posture assistant has become judgmental.",
    "The security system mistook my frantic typing for a Morse code distress signal and initiated a building-wide lockdown.",
    "My computer fan started playing the song \"Daisy Bell\" on a loop, which felt ominous.",
    "The code I wrote is now self-commenting, but its comments are just existential questions.",
    "My noise-canceling headphones started broadcasting my own thoughts, which was horrifying for everyone on the Zoom call.",
    "The cloud is literally a cloud now; all our data is stored in a large, fluffy cumulonimbus floating over Sunnyvale.",
    "My spellchecker was replaced by a Shakespearean scholar who insists on changing everything to iambic pentameter.",
    "The project's color palette became self-aware and is demanding to be reclassified as \"art.\"",
    "The loading icon on the application has entered a hypnotic trance and refuses to stop spinning.",
    "My computer has developed a digital allergy to semicolons.",
    "My cat walked across my keyboard and deployed a six-month-old version of the project to production.",
    "My dog mistook my security token for a chew toy. The token is now in an undisclosed location in the backyard.",
    "My parrot learned the Zoom meeting password and kept joining calls to ask for crackers. I had to change all our security protocols.",
    "A squirrel chewed through my internet cable, then taunted me from a telephone pole.",
    "My dog enrolled our team in a city-wide scavenger hunt via a series of accidental clicks. We were contractually obligated to participate.",
    "A flock of wild parrots (a real San Jose phenomenon) has learned to mimic the sound of a \"critical error\" alert, causing constant panic.",
    "A swarm of bees decided to build a hive on my office window, making the room a \"no-fly zone.\"",
    "My cat is convinced the cursor on my screen is a mortal enemy that must be vanquished with extreme prejudice.",
    "My dog buried my work phone in the backyard, believing it to be some sort of technological bone.",
    "A raccoon broke into my home office and attempted to \"wash\" my keyboard in the dog's water bowl.",
    "A hummingbird flew into the house, and I spent two hours trying to safely guide it out with calm, non-threatening movements.",
    "A particularly aggressive turkey is blocking my driveway and demanding a toll.",
    "My cat unplugged the Wi-Fi router to get my attention because I was not providing a sufficient number of chin scratches.",
    "A family of deer has decided my front porch is the perfect place to nap, and they look at me disapprovingly when I try to leave.",
    "My pet snake escaped its enclosure, and work had to be halted for a full-scale, silent search-and-rescue mission.",
    "The neighborhood cats have unionized and are staging a protest on my lawn; their demands are unclear but the chanting is distracting.",
    "A woodpecker is rhythmically tapping out what I can only assume are secret messages on the side of the house.",
    "My dog figured out how to use the smart speaker and has been ordering absurd quantities of dog treats. Dealing with the deliveries has been a full-time job.",
    "A banana slug got into the house. It's a long, slow, and surprisingly complex story.",
    "My cat has hidden one of my wireless earbuds. It is now a race against time before the battery dies.",
    "My chinchilla requires a \"dust bath\" that creates a small, localized dust storm in my office.",
    "A possum is playing possum on my ergonomic keyboard. I'm not sure what the protocol is here.",
    "The goldfish is staring at me, and I'm convinced it's judging my code.",
    "A murder of crows has taken a particular interest in my work and gathers outside my window to offer unsolicited, Caw-based feedback.",
    "My dog is convinced the daily stand-up meeting is a threat and tries to \"protect\" me from the people on the screen.",
    "I had to mediate a territorial dispute between my cat and a particularly bold squirrel.",
    "A gopher tunneled under my house and created a mysterious sinkhole in my office.",
    "My hamster escaped and I spent the day trying to lure it out from behind the server rack with a trail of sunflower seeds.",
    "A colony of ants has decided my monitor is the perfect place to stage a coup.",
    "A spider built a web directly in front of my webcam's lens, making all my video calls look like they're from a haunted house.",
    "My dog gets jealous of the laptop and insists on being my \"lap-dog\" while I work, which severely limits my ability to type.",
    "My parrot has started mimicking the sound of a dial-up modem.",
    "A wild boar situation. You wouldn't understand.",
    "The local coyotes have started a surprisingly good barbershop quartet, but their rehearsals are always during my peak productivity hours.",
    "A migrating monarch butterfly landed on my nose and I didn't want to disturb it.",
    "My turtle is moving at a surprisingly fast pace today and I have to keep an eye on him.",
    "I was dive-bombed by a territorial mockingbird on my way back from getting coffee.",
    "The neighbor's pet peacock has discovered its reflection in my window.",
    "I had to explain to my cat that he is, in fact, not the designated project manager.",
    "A single, very determined housefly has been outmaneuvering me all day.",
    "I was stuck in a time loop, forced to re-live the same unproductive Tuesday over and over again.",
    "I was briefly abducted by aliens. They had some very critical notes on the project's UI.",
    "According to my horoscope, launching new initiatives this week would have calamitous astrological consequences.",
    "My evil twin from a parallel dimension showed up and tried to sabotage my work by replacing all the semicolons with Greek question marks.",
    "I fell through a wormhole and experienced the last week in a non-linear fashion. My progress is technically done, just not in this timeline.",
    "I realized I am merely a character in a poorly written corporate drama, and my motivation has plummeted due to shoddy character development.",
    "The project's aura is a mess. I had to get my crystals and sage to try and realign its energy before proceeding.",
    "I was an unwitting participant in an elaborate reality TV show called \"Project Deadline: San Jose.\"",
    "The project can only be completed during a solar eclipse, according to the ancient prophecies I found inscribed on the back of the server rack.",
    "My muse for creativity has gone on strike. Negotiations are ongoing.",
    "My shadow ran away, and I had to spend the day convincing it to return. It's a whole thing.",
    "I was applying the principles of quantum mechanics to the project: it is simultaneously both done and not done until observed by a manager.",
    "My tarot reading advised a period of \"rest and reflection\" instead of \"coding and compiling.\"",
    "I was consulting the I Ching about the proper architectural pattern to use; the results were maddeningly ambiguous.",
    "I was body-swapped with a 17th-century poet. I have produced several excellent sonnets but, regrettably, zero lines of code.",
    "I was trapped inside the Winchester Mystery House during a paranormal investigation and had to navigate my way out via a series of confusing staircases.",
    "My reflection in the monitor started giving me bad advice.",
    "I was recruited by a secret society to decode a cryptic message that looked suspiciously like our project's legacy code.",
    "I had to go on a quest to find the \"chosen one\" who could still debug in Flash.",
    "The entire project turned out to be a dream. I had to start over this morning.",
    "I entered a fugue state and when I awoke, I had solved cold fusion but made no progress on my tickets.",
    "I was fighting a metaphorical dragon. It was a metaphor, but the battle was very real.",
    "My personal spirit guide advised against this particular feature implementation.",
    "The office is haunted, and the ghost keeps hiding my stapler.",
    "I was waiting for the stars to align into the shape of the company logo before pushing the final commit.",
    "The project's narrative structure felt weak, so I brought in a plot consultant.",
    "My chakras were misaligned with the project's core objectives.",
    "I was trapped in a Socratic dialogue with myself over the project's true meaning.",
    "I discovered the project is a key component of a vast, global conspiracy. I had to take a personal day to process this.",
    "I was on a vision quest in the Santa Cruz mountains.",
    "I accidentally entered an inescapable dialogue loop with a particularly chatty barista.",
    "I was reverse-hypnotized into believing I was on vacation.",
    "My past life as a medieval scribe is making me want to write all the documentation on illuminated parchment.",
    "The project is not late; it is simply arriving precisely when it means to.",
    "I was distracted by a really compelling cloud formation that looked exactly like a flowchart of our database schema.",
    "I was trying to un-learn everything I thought I knew, as per the advice of a wise old man on a mountain.",
    "I fell down a Wikipedia rabbit hole that started with \"JavaScript frameworks\" and ended with \"the history of cheese.\"",
    "I was trying to achieve a state of \"flow\" but ended up in a state of \"overflow.\"",
    "I was wrestling with the ethical implications of the \"submit\" button.",
    "I was visited by three ghosts, representing the project's past, present, and future.",
    "My sourdough starter achieved sentience and now demands to be fed only artisanal, locally-milled flour. It was a whole ordeal.",
    "The kombucha I was brewing in my kitchen achieved critical mass and I had to call a specialist.",
    "I was trying to assemble a piece of IKEA furniture, and I believe I accidentally constructed a portal to another dimension.",
    "My prized bonsai tree, which I've been cultivating for 15 years, finally achieved perfect harmony, and I couldn't break the meditative state it induced.",
    "My attempt to build a ship-in-a-bottle somehow bottled an actual, tiny, localized storm.",
    "I was engaged in a high-stakes, competitive LARPing (Live Action Role-Playing) event that ran much longer than anticipated.",
    "The rare, exotic plant I own has chosen today, the first time in a decade, to bloom. It requires constant attention.",
    "My Dungeons & Dragons campaign got too immersive and I spent the morning trying to figure out how to apply the game's logic to our project's backlog.",
    "I was trying a new recipe that involved flambé, which resulted in a minor but very exciting kitchen fire.",
    "My home-brewed beer experiment went awry, and my garage is now filled with a fragrant but unmanageable amount of foam.",
    "The cheese I was making at home has started to whisper to me.",
    "My competitive puzzle-solving team had an emergency practice session.",
    "I was trying to recreate a famous work of art using only toast, and it required my full attention.",
    "The model rocket I was building accidentally launched inside my house.",
    "My attempt at urban farming resulted in a single, giant, and vaguely threatening zucchini.",
    "I was knitting a sweater, and the pattern turned out to be a complex algorithm I felt compelled to solve.",
    "I was trying to perfect my latte art, and I am now trapped in a foam-induced trance.",
    "My collection of antique maps fell over, and I spent the day trying to put the world back in chronological order.",
    "I was polishing my ceremonial suit of armor. It is a time-consuming but necessary task.",
    "The intricate house of cards I was building collapsed, and I am in mourning.",
    "I was trying to teach myself how to juggle. This was a mistake.",
    "My sourdough starter has been reclassified as an invasive species.",
    "I was trying to grow crystals in my kitchen, and they have now encased the sink.",
    "My ant farm declared independence.",
    "I was trying to make pickles, but I seem to have accidentally pickled my car keys.",
    "The historical reenactment I participate in had a mandatory, unscheduled drill.",
    "I was setting up a domino-run that spanned my entire house. I couldn't risk leaving until it was complete.",
    "My home automation script for watering my plants misfired and created a tropical rainforest in my living room.",
    "I was alphabetizing my spice rack and discovered I was missing \"thyme.\" The search was all-consuming.",
    "My collection of garden gnomes appears to have rearranged itself overnight into a cryptic tableau.",
    "I was trying to bake a cake, but I misread the recipe and it is now expanding, slowly, but unstoppably.",
    "I was trying to whittle a small wooden bird, but it turned out the branch was still attached to the tree.",
    "My new, high-powered blender created a vortex.",
    "I was trying to communicate with my houseplants. I think we had a breakthrough.",
    "The virtual reality game I was playing was so immersive I forgot which reality was real.",
    "I was composing a symphony for my doorbell.",
    "My attempt at molecular gastronomy resulted in a plate of food that is questioning its own existence.",
    "I was trying to build a Rube Goldberg machine to turn on my computer.",
    "I discovered my old Lego collection and was overcome by a wave of creative inspiration.",
    "I was trying to fold a fitted sheet.",
    "I was trapped in a traffic standstill on Highway 101 caused by a rogue flock of autonomous delivery drones.",
    "A minor earthquake gently rearranged all the letters on my keyboard into alphabetical order.",
    "My self-driving car got into a philosophical disagreement with another self-driving car at a four-way stop, creating an existential gridlock.",
    "The annual San Jose Sentient Drone Race (August 2025) flew a chaotic, unscheduled route directly over my neighborhood.",
    "A tech billionaire's private rocket launch from a nearby location rattled my windows and my nerves for several hours.",
    "The VTA light rail was delayed by what the conductor could only describe as a \"temporal anomaly\" near the SAP Center.",
    "A startup in my neighborhood was testing its new atmospheric moisture harvester, and accidentally caused a localized rainstorm in my backyard.",
    "My smart-home, which is networked with the city's experimental grid, thought the Sharks won the Stanley Cup and initiated a 12-hour celebratory laser light show.",
    "I was trying to go to the office, but a fleet of self-driving Teslas had apparently decided to hold a silent, synchronized rally in the street.",
    "The fog rolling in from the coast had an unusually high glitter content today, which was fabulous but distracting.",
    "A self-driving delivery robot mistook me for its designated package and followed me relentlessly, ignoring all my commands to stop.",
    "I was at my favorite coffee shop in downtown San Jose, but the barista was a robot having an existential crisis. The line was very long.",
    "I got stuck in the Winchester Mystery House.",
    "A venture capitalist mistook me for a startup founder and I had to sit through a two-hour pitch meeting before I could escape.",
    "The air quality was rated as \"Unhealthy for Abstract Thought.\"",
    "I was beta-testing a new augmented reality game that overlaid a fantasy world onto San Jose. I got sidetracked on a quest to find a griffin nesting on top of City Hall.",
    "My smart fridge, in an attempt to be helpful, ordered a pallet of artisanal kale from a farm in Half Moon Bay. The delivery blocked my driveway.",
    "A tech company's promotional blimp came untethered and I was distracted by the slow-motion chase down Guadalupe Parkway.",
    "My e-bike's AI decided it identified as a stationary art installation and refused to move.",
    "A pop-up \"immersive art experience\" popped up, uninvited, in my living room.",
    "The entire neighborhood's Wi-Fi was being disrupted by a mysterious signal that turned out to be emanating from a single, very powerful garage door opener from the 1980s.",
    "A film crew was shooting a sci-fi movie on my street and I was asked to remain indoors so as not to ruin the shot of a post-apocalyptic landscape.",
    "My rent was converted to a fluctuating cryptocurrency, and I spent the day day-trading to make sure I could afford to live here.",
    "A Stanford research experiment involving sonic frequencies escaped campus and made all the glass in my house hum at a perfect C-sharp.",
    "A food-delivery robot had a malfunction and is now guarding my front door like a gargoyle.",
    "The local university's solar car race team needed to make an emergency pit stop in my driveway.",
    "I was trying to take a walk but got trapped in an \"activation\" for a new social media app.",
    "A biotech startup's experimental, fast-growing bamboo got loose and is now slowly encroaching on my property line.",
    "I was distracted by a heated debate at the park over which nearby mountain has the best hiking trail: Mount Umunhum or Mission Peak.",
    "A self-driving bus had an identity crisis and was driving in circles around my block.",
    "I was asked to be an extra in a corporate promo video being filmed at Santana Row.",
    "A \"smart compost\" bin in the neighborhood became sentient and started issuing judgments on everyone's food waste.",
    "The Santa Clara County Fair had a \"best apricot\" competition, and the rivalry was so intense it caused traffic delays.",
    "A Google Street View car was mapping my street, and I felt I needed to remain perfectly still for several hours.",
    "The intense August sun reflecting off a new glass-covered high-rise downtown created a focused beam of light that was slowly melting my mailbox.",
    "A new brand of \"artisanal air\" was being marketed in my neighborhood, and the free samples were very distracting.",
    "The city was testing its new public warning siren, which broadcasts exclusively in soothing whale sounds.",
    "I was stuck behind a convoy of autonomous vehicles learning how to navigate a roundabout.",
    "A rare species of lichen was discovered on my front steps, and a team of botanists cordoned off the area.",
    "I was trying to leave my house, but there was a farmers' market."
]

HELP_TEXT = '''
# Port-Mapper Workflow Guide

## Overview

The Port-Mapper is a comprehensive tool for designing and configuring network switches for VAST Data cluster deployments. This guide covers all tabs, fields, and variables in the current version.

**Tip:** Hover over any field or button to see detailed tooltips explaining their purpose.

## Available Tabs

1. **Setup Tab**: Configure switch model, hostnames, and cluster settings
2. **Cell Planning Tab**: Configure node types and uplinks for single rack/cell
3. **Multi-Rack Tab**: Configure multiple racks for larger deployments
4. **Output Tab**: View previews and generate configuration files
5. **Help Tab**: This guide

## Setup Tab Variables

### Initial Setup
- **Switch Model**: Dropdown to select hardware model (Mellanox SN5400 400G default)
- **Switch Hostname A**: Name for first fabric switch (default: SWA)
- **Switch Hostname B**: Name for second fabric switch (default: SWB)

### Optional Cluster Setup Values

#### Column 1 (Customer Information)
- **Customer Name**: Name of customer organization
- **Site Name**: Physical site location name

#### Column 2 (Cluster Settings)
- **Cluster Name**: Name of the cluster (default: Quota-Destroyer-001)
- **NTP Server IP**: Network Time Protocol server IP
- **Leafs Or Spines**: Role selection (leaf or spine)
- **FabricB Mgmt IP**: Management IP for switch B
- **Max BW Required Per Cell**: Bandwidth goal per cell (1-64 GB/GiB/s)

#### Column 3 (Network Settings)
- **Mgmt CIDR**: Management network subnet (default: 24)
- **Mgmt Gateway**: Default gateway IP
- **FabricA Mgmt IP**: Management IP for switch A
- **Customer Vlans**: Comma-separated VLAN IDs for external connectivity
- **BGP ASNs**: Autonomous System Numbers for BGP routing (numbers, spaces, or commas)

### Advanced Cluster Setup Values
- **Use 2nd NIC**: Check to enable second network interface on CNodes/Eboxes
- **Used Converged Networking**: Check for unified networking configuration
- **Enable Legacy Configuration**: Enable legacy mode for older installations
- **Data Vlan**: VLAN ID for data network traffic (default: 69)

## Cell Planning Tab

### Mapping Mode Selection

The Cell Planning tab supports two mapping modes:

- **Default Mapping**: Port layout logic as defined by Vast Engineering. Uses standard port assignment algorithms based on switch type and configuration.
- **Advanced Mapping**: Allows cables to flow into switch via Left or Right sides with user preference. This prevents cable overlapping from either side if preferred. Uses Mellanox-style column ordering for all switch types (Cisco, Arista, Mellanox) in this mode only.

### Configure Node Types Per Cell

Configure the number of device type nodes that will connect to each A/B switch in each cell.

**Node Types Available:**
- **DN** (Data Nodes): Storage nodes (4 ports per switch on Ceres V1, 2 on Ceres V2/Mavericks)
- **CN** (Compute Nodes): Compute nodes (1 port per switch)
- **EB** (Eboxes): Ebox appliances (2 ports per switch)
- **IE** (Insight Engine Nodes): AI/ML nodes (varies by model)
- **GN** (GPU Nodes): GPU-accelerated nodes (varies by model)

**Fields for Each Node Type:**
- **Node Count**: Number of logical nodes (1-64)
- **Split Ports?**: Check if using breakout cables
- **Split Value**: Split factor (2 or 4)
- **Reserved Port Count**: Extra ports to reserve for future expansion (1-64)
- **Manual Input**: Starting port number or range (optional)
- **Assigned Ports**: Auto-assigned port numbers (read-only)

### Configure Uplinks To/From Per Cell

Configure uplink ports for external connectivity and inter-switch links.

**Uplink Types Available:**
- **IPL** (Inter-Peer Links): Links between leaf pairs
- **ISL** (Inter-Switch Links): Links to spine switches
- **EXT** (External/MLAG/BGP): Customer uplinks
- **NB** (Northbound): 2nd NIC ports for CN/EB (auto-configured)

**Fields for Each Uplink Type:**
- **# Of Uplink Channels**: Number of link aggregation groups (1-64)
- **Ports Per Group**: Physical ports in each group (1-64)
- **Split Ports?**: Check for breakout cables
- **Split Value**: Split factor (2 or 4)
- **Reserved Port Count**: Extra ports to reserve (1-64)
- **Manual Input**: Starting port number or range (optional)
- **Assigned Ports**: Auto-assigned port numbers (read-only)
- **Suggestion**: Recommended ports per group for non-blocking fabric

**Note:** IPL and ISL can both be configured simultaneously (mutual exclusion removed).

### Clone to Multi-Rack Design
- **Clone this cell and add to a Multi Rack Design? How many times**: Number of racks to create (no limit)
- **Rack Name**: Base name for racks (max 10 characters, will be suffixed with 1, 2, etc.)
- **Type**: Design type dropdown (leaf or spine)

## Multi-Rack Tab

### Rack Management (Left Panel)
- **Racks**: List of all configured racks (click to edit, drag to reorder)
- **Add Button**: Create a new rack
- **Remove Button**: Delete selected rack(s)
- **Clone Rack Button**: Duplicate selected rack configuration

### Rack Configuration (Right Panel)

#### General Details
- **Switch Hostname A**: Hostname for first switch in rack
- **Switch Hostname B**: Hostname for second switch in rack
- **Management IP A**: Management IP for switch A
- **Management IP B**: Management IP for switch B
- **Switch Model**: Dropdown to select hardware model
- **Max BW Required Per Rack/Cell**: Bandwidth goal for this rack
- **Type**: Leaf or Spine designation

#### Node Configuration Table
Fields for each node type (DN, CN, EB, IE, GN):
- **Node Count**: Number of nodes (1-64)
- **Split Ports?**: Checkbox for breakout cables
- **Split Value**: Combo box (2 or 4)
- **Reserved Ports**: Extra ports to reserve (1-64)
- **Starting Port #**: Manual start port (1-64, optional)

#### Uplink Configuration Table
Fields for each uplink type (IPL, ISL, EXT, NB):
- **Uplink Channels**: Number of groups (1-64)
- **Ports Per Group**: Ports in each group (1-64)
- **Split Ports?**: Checkbox for breakout cables
- **Split Value**: Combo box (2 or 4)
- **Reserved Ports**: Extra ports to reserve (1-64)
- **Starting Port #**: Manual start port (1-64, optional)

### Live Rack Preview
Shows real-time port layout for both fabrics as you configure the rack.

## Output Tab

### Single-Rack/First Rack View
- **Switch Preview**: Live preview of port assignments for both switches
- **Port Summary**: Table of all port assignments by type
- **Bandwidth Summary**: Calculation of achieved vs. required bandwidth
- **Generate overlays & export**: Export PNG images
- **Export JSON Config**: Save configuration for re-import
- **Create Switch Configs**: Generate switch configuration files

### Multi-Rack View
- **View Summary for Rack**: Dropdown to select which rack to view
- Same output options as single-rack view
- Files generated for all racks when buttons are clicked

## Variable Descriptions

### Setup Tab Variables
- `customer_name`: Customer organization name
- `site_name`: Physical site location
- `cluster_name`: Cluster identifier (default: Quota-Destroyer-001)
- `ntp_server`: NTP server IP address
- `leaf_or_spine`: Switch role selection
- `mgmt_cidr`: Management subnet mask
- `mgmt_gateway`: Default gateway IP
- `fab_a_mgmt_ip`: Switch A management IP
- `fab_b_mgmt_ip`: Switch B management IP
- `customer_vlans`: Comma-separated VLAN IDs
- `bgp_asns`: Comma-separated BGP AS numbers
- `data_vlan`: Data network VLAN ID (default: 69)
- `use_2nd_nic`: Boolean for 2nd NIC enablement
- `use_converged_networking`: Boolean for unified networking
- `peak_bw_goal`: Bandwidth target per cell

### Cell Planning Variables
**Node Types:**
- `dn_count`, `cn_count`, `eb_count`, `ie_count`, `gn_count`: Node counts
- `*_split`: Split checkbox state
- `*_factor`: Split factor (2 or 4)
- `*_reserved`: Reserved port count
- `*_start_port`: Manual starting port

**Uplink Types:**
- `ipl_groups`, `isl_groups`, `ext_groups`: Number of uplink groups
- `ipl_ppg`, `isl_ppg`, `ext_ppg`, `nb_ppg`: Ports per group
- `*_split`: Split checkbox state
- `*_factor`: Split factor (2 or 4)
- `*_reserved`: Reserved port count
- `*_start_port`: Manual starting port

## Port Assignment Rules

- All port values must be between 1 and 64 (no decimals, no letters)
- Node ports assign from low to high (ports 1, 2, 3...)
- Uplink ports assign from high to low (ports 64, 63, 62...)
- Split ports multiply logical connections per physical port
- Reserved ports are labeled as RSVD in diagrams
- IPL and ISL can coexist (mutual exclusion removed in version)
- EXT is the display name for MLAG/BGP ports

## Output Files

### PNG Overlays
Generated with cluster name in filename:
`{cluster_name}_{rack_name}_{hostname_a}_{type}_A.png`
`{cluster_name}_{rack_name}_{hostname_b}_{type}_B.png`

### Switch Configuration Files
Generated with rack details:
`{cluster_name}_{rack_name}_{hostname_a}_{hostname_b}_{type}_switch.cfg`

### JSON Configuration
Complete export of all settings for re-import later.

## Tips and Best Practices

1. **Start Simple**: Begin with single rack design, then clone to multi-rack
2. **Validate Early**: Check port assignments before generating large deployments
3. **Use Suggestions**: Pay attention to uplink suggestions based on bandwidth goals
4. **Save Often**: Export JSON configurations regularly
5. **Preview Changes**: Watch live previews update as you configure
6. **Check Bandwidth**: Ensure achieved bandwidth meets targets
7. **Plan IPs**: Reserve management IPs for all switches before starting
8. **Port Limits**: Remember total ports per switch (typically 64)

## Recent Updates

- Parallel processing for multi-rack PNG and config generation (8 workers)
- Removed 100-rack cloning limit
- Cell Planning tab renamed from Node Types
- IPL and ISL can coexist
- Support for BGP ASNs configuration
- Default switch changed to Mellanox SN5400 400G
- Default cluster name: Quota-Destroyer-001
- Port validation limited to 1-64 range
'''

STYLESHEET = '''
    QTabWidget::pane {
        border-top: 1px solid #C2C7CB;
    }
    QTabWidget::tab-bar {
        left: 5px;
    }
    QTabBar::tab {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                    stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        border: 1px solid #C4C4C3;
        border-bottom-color: #C2C7CB;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 8ex;
        padding: 5px 10px;
    }
    QTabBar::tab:selected, QTabBar::tab:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                    stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
    }
    QTabBar::tab:selected {
        background: #011A51;
        color: white;
    }
    QTabBar::tab:!selected {
        margin-top: 2px;
        color: black;
    }
    QWidget#DarkTab {
        background-color: #011A51;
    }
    QWidget#DarkTab QLabel, QWidget#DarkTab QCheckBox, QWidget#DarkTab QRadioButton, QWidget#DarkTab QGroupBox {
        color: white;
    }
    QWidget#DarkTab QGroupBox {
        font-weight: bold;
    }
    QLineEdit[invalid="true"] {
        background-color: #FFC0CB;
    }

    /* === Styles for Setup Tab === */
    QWidget#SetupTab {
        background-color: #011A51;
        background-repeat: no-repeat;
        /* Position image at the bottom right, so it doesn't interfere
           with the main content area at the top/center. */
        background-position: bottom right;
    }

    /* Make child widgets on the SetupTab transparent so the background image shows through.
       This applies to labels and checkboxes directly on the tab's content widget. */
    QWidget#SetupTab > QWidget > QWidget > QLabel,
    QWidget#SetupTab > QWidget > QWidget > QCheckBox {
        color: white;
        background: transparent;
    }
    /* Make the line separator transparent */
    QWidget#SetupTab QFrame {
        background: transparent;
    }

    /* GroupBoxes on the SetupTab are solid to ensure readability of their contents. */
    QWidget#SetupTab QGroupBox {
        background-color: #021337; /* Solid VAST Dark Blue */
        color: white;
        font-weight: bold;
        border: 1px solid #4a90e2; /* VAST Blue */
        margin-top: 10px;
        padding: 10px;
        border-radius: 5px;
    }
    QWidget#SetupTab QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        left: 10px;
        color: white;
    }

    /* Labels inside the GroupBox should have a transparent background
       to show the GroupBox's solid color. */
    QWidget#SetupTab QGroupBox QLabel,
    QWidget#SetupTab QGroupBox QCheckBox {
        color: white;
        background: transparent;
    }

    /* Input widgets are also solid for clarity. */
    QWidget#SetupTab QLineEdit,
    QWidget#SetupTab QComboBox {
        background-color: #333333; /* Dark Grey */
        color: #4a90e2; /* VAST Blue for text */
        border: 1px solid #76797C;
        border-radius: 2px;
        padding: 2px;
    }
    
    /* Style for QComboBox dropdown list */
    QWidget#SetupTab QComboBox QAbstractItemView {
        background-color: #333333;
        color: #4a90e2;
        selection-background-color: #4a90e2;
        selection-color: white;
        border: 1px solid #76797C;
    }

    /* Style for buttons using object names for specificity */
    QPushButton#LoadButton, QPushButton#ResetButton {
        background-color: #4a90e2; /* VAST Blue */
        color: white;
        border: 1px solid #5aa0f2;
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton#LoadButton:hover, QPushButton#ResetButton:hover {
        background-color: #5aa0f2; /* Lighter blue on hover */
    }
    QPushButton#LoadButton:pressed, QPushButton#ResetButton:pressed {
        background-color: #3a80d2; /* Darker blue when pressed */
    }
    QPushButton:disabled {
        background-color: #555555;
        color: #AAAAAA;
        border-color: #777777;
    }

    /* === ScrollBar Styles for Dark Theme === */
    QScrollBar:vertical {
        border: none;
        background: #011A51; /* Match DarkTab background */
        width: 14px;
        margin: 15px 0 15px 0;
    }
    QScrollBar::handle:vertical {
        background: white;
        min-height: 30px;
        border-radius: 7px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 15px;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        /* Hiding the default arrows, as we use custom labels */
        background: none;
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }


'''

def resource_path(rel: str) -> str:
    """
    Get the absolute path to a resource file.
    Works whether script is run directly or packaged with PyInstaller.
    Paths are resolved relative to the script's directory location.
    """
    try:
        # If bundled with PyInstaller
        base = sys._MEIPASS
    except Exception:
        # If running as a script, use the directory containing this script
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, rel)

def safe_int(text: str, default: int = 0) -> int:
    try:
        return int(text.strip()) if text.strip() else default
    except Exception:
        return default

def get_unique_filename(filepath: str) -> str:
    if not os.path.exists(filepath):
        return filepath
    (directory, filename) = os.path.split(filepath)
    (name, ext) = os.path.splitext(filename)
    match = re.search(r'-(\d+)$', name)
    if match:
        counter = int(match.group(1))
        base_name = name[:match.start()]
    else:
        counter = 1
        base_name = name
    while True:
        counter += 1
        new_name = f'{base_name}-{counter:02d}{ext}'
        new_filepath = os.path.join(directory, new_name)
        if not os.path.exists(new_filepath):
            return new_filepath


def _parse_port_string(port_str: str) -> Optional[list[int]]:
    if not port_str.strip():
        return []
    ports = set()
    parts = port_str.split(',')
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            try:
                (start_str, end_str) = part.split('-')
                start = int(start_str.strip())
                end = int(end_str.strip())
                if start > end:
                    return None
                ports.update(range(start, end + 1))
            except ValueError:
                return None
        else:
            try:
                ports.add(int(part))
            except ValueError:
                return None
    return sorted(list(ports))


def _format_port_ranges(ports: list[int], split_factor: int = 1) -> str:
    """Formats a list of port numbers into a compact string like '1-4,6,8-10' or '1-4/2,6/2'."""
    if not ports:
        return ''
    ports = sorted(list(set(ports)))
    ranges = []
    start_of_range = ports[0]

    def format_single_range(start, end):
        port_str = str(start) if start == end else f'{start}-{end}'
        if split_factor > 1:
            port_str += f'/{split_factor}'
        return port_str

    for i in range(1, len(ports)):
        if ports[i] != ports[i - 1] + 1:
            end_of_range = ports[i - 1]
            ranges.append(format_single_range(start_of_range, end_of_range))
            start_of_range = ports[i]
    # Handle the last range
    ranges.append(format_single_range(start_of_range, ports[-1]))
    return ','.join(ranges)


try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.ANTIALIAS
FONT_PATH = resource_path('ArialBold.ttf')
ISL_COLORS = ['green', 'yellow', 'orange', 'pink', 'lightgreen', 'gold', 'tomato', 'hotpink']
EXT_COLORS = ['lime', 'yellow', 'orange', 'pink', 'lightblue', 'lavender', 'coral', 'turquoise']
colors_fabric = {'A': '#FC9D74', 'B': '#4a90e2'}
HIGH_PORT_UPLINK_TYPES = ['IPL', 'ISL', 'EXT', 'MLAG/BGP', 'NB']  # Uplink types that assign from high ports down
SWITCH_LAYOUTS = {}

SWITCH_LAYOUTS['1'] = {
    'NAME': 'Mellanox SN4600 200G',
    'IMAGE': 'base_sn4600hr.png',
    'PORT_COUNT': 64,
    'NATIVE_SPEED': '200G',
    'SHEET_TAB': 'SN4600',
    'GRID': (4, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 113,
    'PORT_HEIGHT': 48,
    'H_SPACING': 148.6,
    'V_SPACING': 86,
    'START_X': 107,
    'START_Y': 123,
    'ROW_OFFSETS': {
        1: 1,
        3: 1
    }
}
SWITCH_LAYOUTS['2'] = {
    'NAME': 'Mellanox SN3700 200G',
    'IMAGE': 'base_sn3700.png',
    'PORT_COUNT': 32,
    'NATIVE_SPEED': '200G',
    'SHEET_TAB': 'SN3700',
    'GRID': (2, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 103,
    'PORT_HEIGHT': 48,
    'H_SPACING': 109.3,
    'V_SPACING': 78,
    'START_X': 199,
    'START_Y': 66,
    'ROW_OFFSETS': {},
    'CUMULATIVE_GAPS': {
        5: 41,
        7: 40,
        9: 39,
        11: 38
    },
    'COLUMN_X_COORDS': [
        199,
        308,
        418,
        527,
        636,
        784,
        893,
        1042,
        1151,
        1300,
        1409,
        1558,
        1667,
        1777,
        1886,
        1995
    ]
}
SWITCH_LAYOUTS['3'] = {
    'NAME': 'Mellanox SN5400 400G',
    'IMAGE': 'base-SN5400.png',
    'PORT_COUNT': 64,
    'NATIVE_SPEED': '400G',
    'SHEET_TAB': 'SN5400',
    'GRID': (4, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 113,
    'PORT_HEIGHT': 52,
    'H_SPACING': 146.5,
    'V_SPACING': 109,
    'START_X': 144,
    'START_Y': 111,
    'ROW_OFFSETS': {2: -24},
    'HORIZONTAL_LAYOUT': False,
    'BALANCED_NODE_ASSIGNMENT': False,
    'BALANCED_UPLINK_ASSIGNMENT': False
}
SWITCH_LAYOUTS['4'] = {
    'NAME': 'Mellanox SN5600 800G',
    'IMAGE': 'base-SN5600.png',
    'PORT_COUNT': 64,
    'NATIVE_SPEED': '800G',
    'SHEET_TAB': 'SN5600',
    'GRID': (4, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 113,
    'PORT_HEIGHT': 54,
    'H_SPACING': 143.4,
    'V_SPACING': 73,
    'START_X': 163,
    'START_Y': 111,
    'ROW_OFFSETS': {
        1: 3,
        2: 60,
        3: 3
    },
    'HORIZONTAL_LAYOUT': False,
    'BALANCED_NODE_ASSIGNMENT': False,
    'BALANCED_UPLINK_ASSIGNMENT': False
}
SWITCH_LAYOUTS['5'] = {
    'NAME': 'Arista 7060-DX5 400G',
    'IMAGE': 'base-arista7060DX5.png',
    'PORT_COUNT': 64,
    'NATIVE_SPEED': '400G',
    'SHEET_TAB': 'Arista7060DX5',
    'GRID': (4, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 113,
    'PORT_HEIGHT': 52,
    'H_SPACING': 152.5,
    'V_SPACING': 109,
    'START_X': 77,
    'START_Y': 145,
    'ROW_OFFSETS': {
        2: -22,
        3: 3
    },
    'PORT_MAPPING_LOGIC': 'cisco_4x16',
    'BALANCED_NODE_ASSIGNMENT': False,
    'BALANCED_UPLINK_ASSIGNMENT': False
}
SWITCH_LAYOUTS['6'] = {
    'NAME': 'Arista 7050DX4-32S 200G',
    'IMAGE': 'base-arista7050DX4.png',
    'PORT_COUNT': 32,
    'NATIVE_SPEED': '200G',
    'SHEET_TAB': 'Arista7050DX4',
    'GRID': (2, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 121,
    'PORT_HEIGHT': 61,
    'H_SPACING': 151.1,
    'V_SPACING': 80,
    'START_X': 70,
    'START_Y': 82,
    'ROW_OFFSETS': {},
    'HORIZONTAL_LAYOUT': False,
    'BALANCED_NODE_ASSIGNMENT': False,
    'BALANCED_UPLINK_ASSIGNMENT': False
}
SWITCH_LAYOUTS['9'] = {
    'NAME': 'Arista 7060X6-64PE-F 800G',
    'IMAGE': 'base-arista7060X664pef.png',
    'PORT_COUNT': 64,
    'NATIVE_SPEED': '800G',
    'SHEET_TAB': 'Arista7060X6',
    'GRID': (4, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 139,
    'PORT_HEIGHT': 78,
    'H_SPACING': 154,
    'V_SPACING': 90,
    'START_X': 157,
    'START_Y': 78,
    'ROW_OFFSETS': {
        2: 35, # Offset to start Row 3 at y=293
        3: -1   # Additional offset to start Row 4 at y=382
    },
    'HORIZONTAL_LAYOUT': False,
    'PORT_MAPPING_LOGIC': 'cisco_4x16',
    'BALANCED_NODE_ASSIGNMENT': False,
    'BALANCED_UPLINK_ASSIGNMENT': False
}
SWITCH_LAYOUTS['7'] = {
    'NAME': 'Cisco 9332D-GX2B 400G',
    'IMAGE': 'base_cisco_9332d.png',
    'PORT_COUNT': 32,
    'NATIVE_SPEED': '400G',
    'SHEET_TAB': 'C9332D',
    'GRID': (2, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 88,
    'PORT_HEIGHT': 33,
    'H_SPACING': 129,
    'V_SPACING': 71,
    'START_X': 190,
    'START_Y': 58,
    'ROW_OFFSETS': {},
    'HORIZONTAL_LAYOUT': False,
    'CUMULATIVE_GAPS': {
        2: -17,
        4: -17,
        6: -17,
        8: -17,
        10: -17,
        12: -17,
        14: -17
    },
    'COLUMN_X_COORDS': [
        190,
        319,
        430,
        559,
        671,
        800,
        913,
        1042,
        1154,
        1283,
        1395,
        1524,
        1637,
        1766,
        1878,
        2007
    ],
    'BALANCED_NODE_ASSIGNMENT': True,
    'BALANCED_UPLINK_ASSIGNMENT': True
}
SWITCH_LAYOUTS['8'] = {
    'NAME': 'Cisco C9364D-GX2A 400G',
    'IMAGE': 'base_cisco_9364d.png',
    'PORT_COUNT': 64,
    'NATIVE_SPEED': '400G',
    'SHEET_TAB': 'C9634D-GX2A',
    'GRID': (4, 16),
    'FONT_SIZE': 24,
    'PORT_WIDTH': 87,
    'PORT_HEIGHT': 35,
    'H_SPACING': 121,
    'V_SPACING': 84,
    'START_X': 277,
    'START_Y': 38,
    'ROW_OFFSETS': { # Offsets are applied cumulatively.
        2: 47, # Add a 47px gap before row 3 (index 2) starts.
        3: 0   # Row 4 (index 3) has no *additional* offset relative to row 3.
    },
    'PORT_MAPPING_LOGIC': 'cisco_4x16',
    'BALANCED_NODE_ASSIGNMENT': True,
    'BALANCED_UPLINK_ASSIGNMENT': True
}
def get_port_base_type(label: str) -> str:
    """Determines the fundamental type of a port from its label."""
    if label == 'RSVD-EXT':
        return 'EXT'
    if label == 'RSVD-NB':  # Handle legacy/buggy label for compatibility
        return 'NB'
    if label.startswith('RSVD-'):  # e.g., "RSVD-CN" -> "CN"
        return label.split('-', 1)[1]

    # Check for known uplink prefixes
    for prefix in ['ISL', 'EXT', 'NB', 'IPL']:
        if label.startswith(prefix):
            # Handle MLAG/BGP prefix as EXT
            if prefix == 'MLAG/BGP':
                return 'EXT'
            return prefix
    
    # Check for CN-NB and EB-NB labels
    if label.startswith('CN-NB') or label.startswith('EB-NB'):
        return 'NB'

    # Fallback for node types like "CN-1", "DN-5", etc.
    match = re.match(r'([A-Z]+)', label)
    return match.group(1) if match else 'UNKNOWN'

class PortPlanner:
    """Handles the logic for calculating port assignments."""

    def generate_node_ports(self, node_type: str,
        count: int,
        split: bool,
        factor: int,
        start_port: int,
        reserved: int,
        node_start: int) -> tuple[list[tuple[int,
        str]],
         int]:
        ports = []
        if split and factor > 1:
            physical_ports_needed = math.ceil(count / factor)
        else:
            physical_ports_needed = count
            factor = 1
        current_port = start_port
        for i in range(physical_ports_needed):
            port_num = current_port + i
            first_node = node_start + i * factor
            if first_node <= node_start + count - 1:
                last_node = min(first_node + factor - 1, node_start + count - 1)
                if first_node == last_node:
                    label = f'{node_type}-{first_node}'
                else:
                    label = f'{node_type}-{first_node}/{last_node}'
            else:
                label = f'RSVD-{node_type}'
            ports.append((port_num, label))
        for i in range(reserved):
            port_num = start_port + physical_ports_needed + i
            label = f'RSVD-{node_type}'
            ports.append((port_num, label))
        return (ports, node_start + count)

    def generate_grouped_ports(self, uplink_type: str,
        groups: int,
        ports_per_group: int,
        split: bool,
        factor: int,
        # The starting port for the assignment. For high-port types, this is the
        # highest port number in the range. For others, it's the lowest.
        start_port: int, 
        reserved: int,
        locked: bool,
        cn_count: int = 0,
        eb_count: int = 0) -> list[tuple[int, str]]:
        ports = []
        is_high_port_assignment = uplink_type in HIGH_PORT_UPLINK_TYPES
        increment = -1 if is_high_port_assignment else 1
        current_port = start_port
        phys_ports_per_group = math.ceil(ports_per_group / factor) if split and factor > 1 else ports_per_group

        # Special handling for NB ports
        if uplink_type == 'NB':
            cn_nb_count = 0
            eb_nb_count = 0
            
            for group_num in range(groups):
                group_port_nums = []
                for _ in range(phys_ports_per_group):
                    group_port_nums.append(current_port)
                    current_port += increment

                sorted_ports = sorted(group_port_nums)

                for port_index, port_num in enumerate(sorted_ports):
                    if split and factor > 1:
                        first_logical = port_index * factor + 1
                        last_logical = min((port_index + 1) * factor, ports_per_group)
                        label_suffix = f'{first_logical}/{last_logical}' if first_logical != last_logical else str(first_logical)
                    else:
                        label_suffix = str(port_index + 1)

                    # Determine if this port corresponds to CN or EB
                    if port_index < cn_count:
                        cn_nb_count += 1
                        label = f'CN-NB-{cn_nb_count}' if not split or factor == 1 else f'CN-NB-{cn_nb_count}/{label_suffix}'
                    else:
                        eb_nb_count += 1
                        label = f'EB-NB-{eb_nb_count}' if not split or factor == 1 else f'EB-NB-{eb_nb_count}/{label_suffix}'

                    ports.append((port_num, label))
        else:
            # Original logic for non-NB ports
            for group_num in range(groups):
                group_port_nums = []
                for _ in range(phys_ports_per_group):
                    group_port_nums.append(current_port)
                    current_port += increment

                sorted_ports = sorted(group_port_nums)

                for port_index, port_num in enumerate(sorted_ports):
                    if split and factor > 1:
                        first_logical = port_index * factor + 1
                        last_logical = min((port_index + 1) * factor, ports_per_group)
                        label_suffix = f'{first_logical}/{last_logical}' if first_logical != last_logical else str(first_logical)
                    else:
                        label_suffix = str(port_index + 1)

                    # *** CRITICAL: DO NOT CHANGE THIS LABEL MAPPING ***
                    # Ports are stored internally as 'MLAG/BGP' in uplink_types but MUST be displayed as 'EXT' in the UI
                    # DO NOT display 'MLAG/BGP' - ALWAYS convert to 'EXT' for port labels
                    # This is intentional: 'MLAG/BGP' is the internal type name, 'EXT' is the display name
                    # Use EXT instead of MLAG/BGP for port labels
                    display_type = 'EXT' if uplink_type == 'MLAG/BGP' else uplink_type
                    if uplink_type in ['ISL', 'MLAG/BGP'] and groups > 1:
                        label = f'{display_type}{group_num + 1}-{label_suffix}'
                    else:
                        label = f'{display_type}-{label_suffix}'

                    ports.append((port_num, label))

        # Handle reserved ports for all uplink types
        # *** CRITICAL: DO NOT CHANGE THIS LABEL MAPPING ***
        # Ports are stored internally as 'MLAG/BGP' in uplink_types but MUST be displayed as 'EXT' in the UI
        # DO NOT display 'MLAG/BGP' - ALWAYS convert to 'EXT' for port labels
        for _ in range(reserved):
            port_num = current_port
            current_port += increment
            if uplink_type == 'MLAG/BGP':
                label = 'RSVD-EXT'  # EXT is the display name, never use 'RSVD-MLAG/BGP'
            elif uplink_type == 'NB':
                label = 'RSVD-NB'
            else:
                label = f'RSVD-{uplink_type}'
            ports.append((port_num, label))
        return ports


def pil_to_qpixmap(pil_img: Image.Image) -> QPixmap:
    """Convert a PIL Image to a QPixmap."""
    # The manual channel swapping (r,g,b -> b,g,r) is a common source of color
    # issues between libraries. Removing it and relying on the format flags
    # is more robust.
    if pil_img.mode != "RGBA":
        pil_img = pil_img.convert("RGBA")

    im_data = pil_img.tobytes("raw", "RGBA")
    qim = QImage(im_data, pil_img.size[0], pil_img.size[1], QImage.Format.Format_RGBA8888)
    return QPixmap.fromImage(qim)


def convert_help_to_html(text: str) -> str:
    """Converts the markdown-like help text to basic HTML for QTextEdit."""
    html_lines = []
    for line in text.strip().split('\n'):
        # Basic HTML escaping
        line = line.replace('<', '&lt;').replace('>', '&gt;')

        # Headers
        if line.startswith('# '):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith('## '):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith('### '):
            html_lines.append(f"<h3 style='margin-top: 8px;'>{line[4:]}</h3>")
        elif line.startswith('#### '):
            html_lines.append(f"<h4 style='margin-top: 5px;'>{line[5:]}</h4>")

        # Lists
        elif re.match(r'^\d+\.\s+', line):
            content = re.sub(r'^\d+\.\s+', '', line)
            num = re.match(r'^\d+\.', line).group(0)
            html_lines.append(f"<p style='margin-left: 20px;'><b>{num}</b> {content}</p>")
        elif line.startswith('*   '):
            html_lines.append(f"<p style='margin-left: 20px;'>&bull; {line[4:]}</p>")
        elif line.startswith('    *   '):
            html_lines.append(f"<p style='margin-left: 40px;'>&bull; {line[8:]}</p>")

        # Regular paragraph
        elif line.strip() == '':
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p>{line}</p>")

    full_html = "".join(html_lines)
    # Handle bold
    full_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', full_html)
    return full_html

class LegacyCommandGenerator:
    """
    Encapsulates all logic for generating the legacy installation script.
    This class takes the main window as a reference to access UI elements,
    gathers data, validates it, and constructs the final script output.
    """
    def __init__(self, main_window: 'PortMapperPyQt'):
        self.ui = main_window
        self.errors = []
        self.data = {}

    def generate(self) -> Tuple[Optional[str], list[str]]:
        """
        Main method to generate the script.
        Returns a tuple of (script_content, errors).
        """
        self._gather_inputs()
        self._validate_inputs()

        if self.errors:
            return (None, self.errors)

        script_content = self._build_script_content()
        return (script_content, [])

    def _gather_inputs(self):
        """Collects all data from the legacy UI widgets into a dictionary."""
        self.data = {
            'customer': self.ui.legacy_customer.text().strip(),
            'cluster_name': self.ui.legacy_cluster_name.text().strip(),
            'rack_identifier': self.ui.legacy_rack_identifier.text().strip(),
            'cluster_label': self.ui.legacy_cluster_label.text().strip(),
            'release': self.ui.legacy_release.text().strip(), 
            'buildfile': self.ui.legacy_buildfile.text().strip(),
            'cnode_count': safe_int(self.ui.legacy_cnode_count.text()),
            'dbox_type': self.ui.legacy_dbox_type.currentText().lower(),
            'ceres_version': self.ui.legacy_ceres_version.currentText().lower(),
            'dbox_count': safe_int(self.ui.legacy_dbox_count.text()),
            'hostname_template': self.ui.legacy_hostname_template.text().strip(),
            'ebox_count': safe_int(self.ui.legacy_ebox_count.text()),
            'mgmt_ip_cnode': self.ui.legacy_mgmt_ip_cnode.text().strip(),
            'mgmt_ip_dnode': self.ui.legacy_mgmt_ip_dnode.text().strip(),
            'mgmt_netmask': self.ui.legacy_mgmt_netmask.text().strip(),
            'dns': self.ui.legacy_dns.text().strip(),
            'ntp_servers': self.ui.legacy_ntp.text().strip(),
            'ext_gateway': self.ui.legacy_ext_gateway.text().strip(),
            'b2b_ipmi': self.ui.legacy_b2b_ipmi.isChecked(),
            'vm_vip': self.ui.legacy_vm_vip.text().strip(), 
            'mgmt_ip_ebox': self.ui.legacy_mgmt_ip_ebox.text().strip(),
            'switch1': self.ui.legacy_switch1.text().strip(),
            'switch2': self.ui.legacy_switch2.text().strip(),
            'mellanox_switches': self.ui.legacy_mellanox_switches.isChecked(),
            'is_onyx': self.ui.legacy_switch_os.currentText().lower() == 'onyx',
            'skip_secondary_nic': self.ui.legacy_skip_nic.isChecked(),
            'rdma_pfc_needed': self.ui.legacy_rdma_pfc.isChecked(),
            'auto_ports': self.ui.legacy_auto_ports.currentText(),
            'ib_mode': self.ui.legacy_ib_mode.currentText(),
            'ib_mtu': self.ui.legacy_ib_mtu.text().strip(),
            'eth_mtu': self.ui.legacy_eth_mtu.text().strip(),
            'vxlan_support': self.ui.legacy_vxlan.isChecked(),
            'change_template': self.ui.legacy_change_template.isChecked(),
            'template': self.ui.legacy_template.text().strip(),
            'mgmt_inner_vip': self.ui.legacy_mgmt_inner_vip.text().strip(),
            'docker_bip': self.ui.legacy_docker_bip.text().strip(),
            'change_vlan': self.ui.legacy_change_vlan.isChecked(),
            'vlan_id': self.ui.legacy_vlan_id.text().strip(),
            'isolcpu_values': self.ui.legacy_isolcpu.text().strip(),
        }
        # Derived values
        self.data['dnode_count'] = self._calculate_dnode_count()

    def _validate_inputs(self):
        """Performs all validation and populates the self.errors list."""
        # Part A: Mandatory Field Validation
        mandatory_fields = {
            "Customer Name": 'customer', "Cluster Name": 'cluster_name', "Cluster PSNT": 'cluster_label',
            "Release Version": 'release', "Buildfile Name": 'buildfile', "MGMT Netmask": 'mgmt_netmask',
            "DNS Servers": 'dns', "NTP Servers": 'ntp_servers',
            "MGMT Gateway": 'ext_gateway', "VMS VIP": 'vm_vip',
            "Backend Switch 1 IP": 'switch1', "Backend Switch 2 IP": 'switch2'
        }
        if self.data['cnode_count'] > 0:
            mandatory_fields["Number of Cnodes"] = 'cnode_count'
            mandatory_fields["First CNode MGMT IP"] = 'mgmt_ip_cnode'
        if self.data['dbox_count'] > 0:
            mandatory_fields["Number of DBOXes"] = 'dbox_count'
            mandatory_fields["First DNode MGMT IP"] = 'mgmt_ip_dnode'
        if self.data['ebox_count'] > 0:
            mandatory_fields["Number of Eboxes"] = 'ebox_count'
            mandatory_fields["First Ebox MGMT IP"] = 'mgmt_ip_ebox'

        missing = [name for name, key in mandatory_fields.items() if not self.data.get(key)]
        if missing:
            self.errors.append("The following required fields are empty:\n\n- " + "\n- ".join(missing))
            return # Stop validation if mandatory fields are missing

        # Part B & C: Network and IP Validation
        try:
            gateway_ip = ipaddress.ip_address(self.data['ext_gateway'])
            network = ipaddress.ip_network(f"{gateway_ip}/{self.data['mgmt_netmask']}", strict=False) if self.data['mgmt_netmask'] else None
            vms_vip = ipaddress.ip_address(self.data['vm_vip']) if self.data['vm_vip'] else None
            switch1_ip = ipaddress.ip_address(self.data['switch1'])
            switch2_ip = ipaddress.ip_address(self.data['switch2'])

            if network and vms_vip and vms_vip not in network:
                self.errors.append(f"- VMS VIP ({vms_vip}) is not in the MGMT subnet ({network}).")

            all_node_ips = []
            if self.data['cnode_count'] > 0:
                cnode_start_ip = ipaddress.ip_address(self.data['mgmt_ip_cnode'])
                cnode_end_ip = cnode_start_ip + self.data['cnode_count'] - 1
                if network and cnode_end_ip not in network: self.errors.append(f"- Last CNode IP ({cnode_end_ip}) is not in the MGMT subnet ({network}).")
                if vms_vip and cnode_start_ip <= vms_vip <= cnode_end_ip: self.errors.append(f"- VMS VIP ({vms_vip}) overlaps with the CNode IP range.")
                if cnode_start_ip <= switch1_ip <= cnode_end_ip: self.errors.append(f"- Switch 1 IP ({switch1_ip}) conflicts with the CNode IP range.")
                if cnode_start_ip <= switch2_ip <= cnode_end_ip: self.errors.append(f"- Switch 2 IP ({switch2_ip}) conflicts with the CNode IP range.")
                all_node_ips.append(list(ipaddress.summarize_address_range(cnode_start_ip, cnode_end_ip)))

            if self.data['dnode_count'] > 0:
                dnode_start_ip = ipaddress.ip_address(self.data['mgmt_ip_dnode'])
                dnode_end_ip = dnode_start_ip + self.data['dnode_count'] - 1
                if network and dnode_end_ip not in network: self.errors.append(f"- Last DNode IP ({dnode_end_ip}) is not in the MGMT subnet ({network}).")
                if vms_vip and dnode_start_ip <= vms_vip <= dnode_end_ip: self.errors.append(f"- VMS VIP ({vms_vip}) overlaps with the DNode IP range.")
                if dnode_start_ip <= switch1_ip <= dnode_end_ip: self.errors.append(f"- Switch 1 IP ({switch1_ip}) conflicts with the DNode IP range.")
                if dnode_start_ip <= switch2_ip <= dnode_end_ip: self.errors.append(f"- Switch 2 IP ({switch2_ip}) conflicts with the DNode IP range.")
                all_node_ips.append(list(ipaddress.summarize_address_range(dnode_start_ip, dnode_end_ip)))

            if self.data['ebox_count'] > 0:
                ebox_start_ip = ipaddress.ip_address(self.data['mgmt_ip_ebox'])
                ebox_end_ip = ebox_start_ip + self.data['ebox_count'] - 1
                if network and ebox_end_ip not in network: self.errors.append(f"- Last Ebox IP ({ebox_end_ip}) is not in the MGMT subnet ({network}).")
                if vms_vip and ebox_start_ip <= vms_vip <= ebox_end_ip: self.errors.append(f"- VMS VIP ({vms_vip}) overlaps with the Ebox IP range.")
                if ebox_start_ip <= switch1_ip <= ebox_end_ip: self.errors.append(f"- Switch 1 IP ({switch1_ip}) conflicts with the Ebox IP range.")
                if ebox_start_ip <= switch2_ip <= ebox_end_ip: self.errors.append(f"- Switch 2 IP ({switch2_ip}) conflicts with the Ebox IP range.")
                all_node_ips.append(list(ipaddress.summarize_address_range(ebox_start_ip, ebox_end_ip)))

            # Check for overlaps between all node IP ranges
            for i in range(len(all_node_ips)):
                for j in range(i + 1, len(all_node_ips)):
                    # summarize_address_range returns a list, so we get the first (and only) element
                    if all_node_ips[i][0].overlaps(all_node_ips[j][0]):
                        self.errors.append(f"- IP range conflict detected between {all_node_ips[i][0]} and {all_node_ips[j][0]}.")

        except (ValueError, ipaddress.AddressValueError) as e:
            self.errors.append(f"Invalid IP or Netmask. Please check your MGMT Gateway, Netmask, and IP address formats.\n\nError: {e}")

    def _build_script_content(self) -> str:
        """Constructs the full script string from the validated data."""
        output = []
        d = self.data # Alias for brevity

        # Template values for hostnames
        template_values = {'{cluster}': d['cluster_name'], '{customer}': d['customer'], '{rack}': d['rack_identifier']}

        # Header and cleanup
        output.append("####  ENSURE YOU REMOVE ANY CONTAINERS FROM ALL NODES IN THE CLUSTER ####")
        output.append("################ REMOVE CONTAINERS, RUN ON ALL NODES ###############")
        output.append("# Kill anything running\ndocker ps -qa|xargs -r docker kill")
        output.append("# Delete old containers\ndocker images -qa|xargs -r docker rmi -f\ndocker ps -qa|grep -v CONTAIN|awk {'print $1'}|xargs -r docker rm -f")
        output.append("# Forcibly removes anything related to containers that are not running.\ndocker system prune -f")
        output.append("# Validate they are gone\ndocker images -a\ndocker ps -a")
        output.append("# Clean up old container logs\nrm -f /vast/log/container-vastdata*\nrm -rf /vast/bundles/upgrades")
        output.append("####################################################################\n")

        # Configuration exports
        output.append(f"###### Configuration for {d['customer']} - {d['cluster_name']} ######")
        output.append(f"export release={d['release']}")
        output.append(f"export buildfile={d['buildfile']}")
        output.append(f"export cluster_name={d['cluster_name']}")
        output.append(f"export cluster_label={d['cluster_label']}")
        output.append(f"export branch_tag=release-{d['release']}")
        if d['isolcpu_values']:
            output.append(f"isolcpu={d['isolcpu_values']}")

        internal_prefix = f"{d['template']}.128" if d['change_template'] and d['template'] else "172.16.128"
        total_cnode_like_count = d['cnode_count'] + d['ebox_count']
        output.append("\n###### Internal node address ranges ######")
        output.append(f"export cnodes_ips={internal_prefix}.{{1..{total_cnode_like_count}}}")
        if d['dnode_count'] > 0:
            output.append(f"export dnodes_ips={internal_prefix}.{{100..{100 + d['dnode_count'] - 1}}}")

        # Network Commands
        output.append("\n###### Configure Network Commands ######")

        # C-Node Commands
        if d['cnode_count'] > 0:
            for i in range(1, d['cnode_count'] + 1):
                template_values['{type}'] = 'cn'
                template_values['{num}'] = str(i)
                ip = str(ipaddress.ip_address(d['mgmt_ip_cnode']) + i - 1)
                command = self._generate_network_command('cnode', i, ip, template_values)
                output.append(f"\n# Command for Cnode {i}:\n{command}")

        # E-Box Commands (treated like C-Nodes for internal numbering)
        if d['ebox_count'] > 0:
            for i in range(1, d['ebox_count'] + 1):
                template_values['{type}'] = 'eb'
                template_values['{num}'] = str(i)
                ip = str(ipaddress.ip_address(d['mgmt_ip_ebox']) + i - 1)
                # E-boxes continue the internal numbering from C-nodes
                internal_node_num = d['cnode_count'] + i
                command = self._generate_network_command('ebox', internal_node_num, ip, template_values)
                output.append(f"\n# Command for Ebox {i}:\n{command}")

        if d['dnode_count'] > 0:
            for i in range(100, 100 + d['dnode_count']):
                template_values['{type}'] = 'dn'
                template_values['{num}'] = str(i)
                ip = str(ipaddress.ip_address(d['mgmt_ip_dnode']) + i - 100)
                command = self._generate_network_command('dnode', i, ip, template_values)
                output.append(f"\n# Command for Dnode {i}:\n{command}")

        # Footer commands
        vman_pfc = (d['mellanox_switches'] and not d['is_onyx']) or not d['mellanox_switches']
        dnode_count = d['dnode_count']
        dnode_ips_str = f" --dnode-ips {internal_prefix}.{{100..{100 + dnode_count - 1}}}" if dnode_count > 0 else ''
        dnode_range_str = f"{{100..{100 + dnode_count - 1}}}" if dnode_count > 0 else ''
        all_nodes_range = f"{{1..{total_cnode_like_count}}}{' ' + dnode_range_str if dnode_range_str else ''}".strip()
        dnode_ips_segment = f",{internal_prefix}.{{100..{100 + dnode_count - 1}}}" if dnode_count > 0 else ''
        all_nodes_ips_range = f"{internal_prefix}.{{1..{total_cnode_like_count}}}{dnode_ips_segment}"

        output.append("\n\n" + self._generate_ping_command(internal_prefix))
        output.append("\n" + self._generate_clush_config(internal_prefix))
        output.append(f"""


# Create customer unique ssh key and push to all nodes
ssh-keygen -t rsa -C "{d['customer']}@vastdata" -b 4096

# Push the ssh key to all nodes without password prompts
for i in {all_nodes_range} ; do sshpass -p vastdata ssh-copy-id -o "StrictHostKeyChecking=no" vastdata@{internal_prefix}.$i; done

clush -g cnodes -c /home/vastdata/.ssh/*

# Copy clush config file to all nodes
for ip in {all_nodes_range} ; do clush -w {internal_prefix}.$ip --copy /etc/clustershell/groups.d/local.cfg --dest /etc/clustershell/groups.d/local.cfg ; done

# Correct Issues with Obsolete/Missing /vast/deploy/ssh_key.pem file
sudo sed -ie "/^ssh_options: -oStrictHostKeyChecking=no -i \\/vast\\/deploy\\/ssh_key.pem/ s/^/#/" /etc/clustershell/clush.conf
clush -a hostname

# Test connections to ensure cabling is correct
./vnetmap.py -s {d['switch1']},{d['switch2']} -i {all_nodes_ips_range} -u admin -p admin -k /home/vastdata/.ssh/id_rsa

# Restart chronyd. This ensures chrony is actually using the configured NTP servers and not the OS default.
clush -a sudo systemctl restart chronyd

# Set UTC and confirm time is in sync (NTP should be working)
clush -a sudo timedatectl set-timezone UTC
clush -aB date

# scp build to VAST CNode - command assumes the file is located under "/Downloads" on your Mac
scp -o "StrictHostKeyChecking=no" -o "UserKnownHostsFile /dev/null" ~/Downloads/{d['buildfile']} vastdata@192.168.3.2:/vast/bundles/

###### Start install process #####

# Untar the buildfile (takes ~10 min)
mkdir -p /userdata/scratch/{d['release']}
tar -xf /vast/bundles/{d['buildfile']} -C /userdata/scratch/{d['release']}
cd /userdata/scratch/{d['release']}

# Set up the docker instance and clean up any existing VMS remnants on first node.
./vman.sh release-{d['release']} ~/.ssh/id_rsa reformat

# Start services on this node (fast)
./vman.sh release-{d['release']} ~/.ssh/id_rsa start

# Populate VMS ssh key to all nodes
clush -a --copy /vast/deploy/ssh_key.pem --dest /vast/deploy/ssh_key.pem

# Launch the installation process
./vman.sh release-{d['release']} ~/.ssh/id_rsa vcli -u admin -p 123456 -c cluster create --build release-{d['release']} --cnode-ips {internal_prefix}.{{1..{total_cnode_like_count}}}{dnode_ips_str} --name {d['cluster_name']} --psnt {d['cluster_label']} --enable-encryption{' --enable-pfc' if vman_pfc else ''}
""")
        return '\n'.join(output)

    def _calculate_dnode_count(self) -> int:
        """Calculate the number of dnodes based on dbox type and count."""
        if self.data['dbox_type'] == 'ceres':
            return self.data['dbox_count'] * (4 if self.data['ceres_version'].lower() == 'v1' else 2)
        else:  # mavericks
            return self.data['dbox_count'] * 2

    def _generate_ping_command(self, internal_prefix: str) -> str:
        d = self.data
        total_cnode_like_count = d['cnode_count'] + d['ebox_count']
        mgmt_prefix_cnode = '.'.join(d['mgmt_ip_cnode'].split('.')[:3])
        cnode_start_octet = safe_int(d['mgmt_ip_cnode'].split('.')[-1])
        cnode_range = f"{cnode_start_octet}..{cnode_start_octet + d['cnode_count'] - 1}" if cnode_start_octet > 0 else ""
        dnode_range_str = f'{{100..{100 + d["dnode_count"] - 1}}}' if d["dnode_count"] > 0 else ''
        all_nodes_range = f"{{1..{total_cnode_like_count}}}{' ' + dnode_range_str if dnode_range_str else ''}"

        ping_commands = f"""
# IPMI Network (CNodes only)
for i in {{1..{d['cnode_count']}}}; do echo -n "192.168.3.$i "; ping -c 4 -i 0.2 -M do -s 1000 192.168.3.$i | grep loss; done

# Internal Network
for i in {all_nodes_range}; do echo -n "{internal_prefix}.$i "; ping -c 4 -i 0.2 -M do -s 8972 {internal_prefix}.$i | grep loss; done

# Management Network
for i in {{{cnode_range}}}; do echo -n "{mgmt_prefix_cnode}.$i "; ping -c 4 -i 0.2 -M do -s 1000 {mgmt_prefix_cnode}.$i | grep loss; done"""
        if d['dnode_count'] > 0 and d['mgmt_ip_dnode']:
            mgmt_prefix_dnode = '.'.join(d['mgmt_ip_dnode'].split('.')[:3])
            dnode_start_octet = safe_int(d['mgmt_ip_dnode'].split('.')[-1])
            dnode_range = f"{dnode_start_octet}..{dnode_start_octet + d['dnode_count'] - 1}"
            ping_commands += f'\nfor i in {{{dnode_range}}}; do echo -n "{mgmt_prefix_dnode}.$i "; ping -c 4 -i 0.2 -M do -s 1000 {mgmt_prefix_dnode}.$i | grep loss; done'
        if d['ebox_count'] > 0 and d['mgmt_ip_ebox']:
            mgmt_prefix_ebox = '.'.join(d['mgmt_ip_ebox'].split('.')[:3])
            ebox_start_octet = safe_int(d['mgmt_ip_ebox'].split('.')[-1])
            ebox_range = f"{ebox_start_octet}..{ebox_start_octet + d['ebox_count'] - 1}"
            ping_commands += f'\nfor i in {{{ebox_range}}}; do echo -n "{mgmt_prefix_ebox}.$i "; ping -c 4 -i 0.2 -M do -s 1000 {mgmt_prefix_ebox}.$i | grep loss; done\n'
        return ping_commands

    def _generate_clush_config(self, internal_prefix: str) -> str:
        d = self.data
        total_cnode_like_count = d['cnode_count'] + d['ebox_count']
        cnode_range = f"[1-{total_cnode_like_count}]" if total_cnode_like_count > 0 else ""

        clush_lines = f"cnodes: {internal_prefix}.{cnode_range}\n" if cnode_range else ""
        dnode_range = f"[100-{100 + d['dnode_count'] - 1}]" if d['dnode_count'] > 0 else ""
        if dnode_range: clush_lines += f"dnodes: {internal_prefix}.{dnode_range}\n"
        clush_lines += f"all: {'@cnodes' if cnode_range else ''}{' @dnodes' if dnode_range else ''}".strip()

        return f"""
###### Cluster Install Configuration ######

# Create the clush config file
sudo vi /etc/clustershell/groups.d/local.cfg

# Add the following lines to define the clush groups:
{clush_lines}"""

    def _generate_network_command(self, node_type: str, node_num: int, ip: str, placeholders: dict) -> str:
        """Generate network configuration command with common parameters."""
        d = self.data
        if d['hostname_template']:
            hostname = d['hostname_template']
            for key, value in placeholders.items():
                hostname = hostname.replace(key, value)
        else:
            hostname = f"{placeholders.get('{type}')}{placeholders.get('{num}')}"

        auto_ports_map = {'int_eth_ext_ib': '1', 'int_eth_ext_ib_eth': '2', 'eth': '3', 'ib': '4'}
        auto_ports_choice = auto_ports_map.get(d['auto_ports'], '3')

        base_cmd = [
            f"sudo configure_network.py {node_num}",
            "--auto-ports-ext-iface outband",
            f"--ext-ip {ip}",
            f"--ext-netmask {d['mgmt_netmask']}",
            f"--ext-dns \"{d['dns']}\"",
            f"--ntp \"{d['ntp_servers']}\"",
            f"--ext-gateway {d['ext_gateway']}",
            f"--hostname {hostname}",
            f"--mgmt-vip {d['vm_vip']}",
            f"--auto-ports {'eth' if auto_ports_choice in ['1', '2', '3'] else 'ib'}"
        ]

        if d['b2b_ipmi']:
            base_cmd.append("--b2b-ipmi")
        if node_type in ['cnode', 'ebox'] and d['skip_secondary_nic']:
            base_cmd.append("--auto-ports-skip-nic ext")
        if auto_ports_choice in ['1', '2', '4'] and d['ib_mtu']:
            base_cmd.extend([f"--ib-mode {d['ib_mode']}", f"--nb-ib-mtu {d['ib_mtu']}"])
        if node_type in ['cnode', 'ebox'] and auto_ports_choice in ['2', '3'] and d['eth_mtu'] and not d['skip_secondary_nic']:
            base_cmd.append(f"--nb-eth-mtu {d['eth_mtu']}") # This line seems correct as is.
        # Add --vxlan flag if switch OS is NOT Onyx (any other OS gets VXLAN)
        if not d['is_onyx']:
            base_cmd.append("--vxlan")
        if d['change_template']:
            base_cmd.append(f"--template {d['template']}.{{network}}.{{node}}")
            if d['mgmt_inner_vip']:
                base_cmd.append(f"--mgmt-inner-vip {d['mgmt_inner_vip']}")
            if d['docker_bip']:
                base_cmd.append(f"--dockerd-bip {d['docker_bip']}")
        if d['change_vlan'] and d['vlan_id']:
            base_cmd.append(f"--vlan-id {d['vlan_id']}")
        if node_type in ['cnode', 'ebox'] and d['rdma_pfc_needed']:
            base_cmd.append("--enable-pfc")
            base_cmd.append("--traffic-class=0,0,0,1,0,0,0,0")

        return ' '.join(base_cmd)

class PortDrawer:
    """
    A helper class to encapsulate the logic for drawing a single port on the switch overlay.
    This refactoring cleans up the main _draw_overlay method by separating concerns.
    """
    def __init__(self, draw: ImageDraw.ImageDraw, config: dict, display_scale: float, cn_count: int = 0, eb_count: int = 0):
        self.draw = draw
        self.config = config
        self.display_scale = display_scale
        self.rows_per_col = config['GRID'][0]
        self.cols_per_row = config['GRID'][1]
        self.mapping_logic = config.get('PORT_MAPPING_LOGIC')
        self.cn_count = cn_count
        self.eb_count = eb_count

        # Pre-calculate cumulative row offsets
        self.cumulative_offsets = {}
        current_offset = 0
        for r in range(self.rows_per_col):
            current_offset += self.config.get('ROW_OFFSETS', {}).get(r, 0)
            self.cumulative_offsets[r] = current_offset

    def _get_port_coordinates(self, port_id: int) -> tuple[int, int]:
        """Calculates the top-left (x, y) coordinates for a given port ID."""
        if self.mapping_logic == 'cisco_4x16':
            # For ports 1-32, they are in rows 0 and 1.
            # For ports 33-64, they are in rows 2 and 3.
            if port_id <= 32:
                col, row = (port_id - 1) // 2, (port_id - 1) % 2
            else:
                # Adjust port_id to be 1-based for the second block of 32 ports
                base_pid = port_id - 32
                col, row = (base_pid - 1) // 2, 2 + ((base_pid - 1) % 2)
        elif self.config.get('HORIZONTAL_LAYOUT', False):
            row, col = divmod(port_id - 1, self.cols_per_row)
        else:
            col, row = divmod(port_id - 1, self.rows_per_col)

        if 'COLUMN_X_COORDS' in self.config and col < len(self.config['COLUMN_X_COORDS']):
            x = self.config['COLUMN_X_COORDS'][col]
        else:
            x = int(self.config['START_X'] + col * self.config['H_SPACING'])

        y = int(self.config['START_Y'] + row * self.config['V_SPACING'] + self.cumulative_offsets.get(row, 0))
        return x, y

    def _get_port_fill_color(self, label: str, fabric: str) -> str:
        """Determines the fill color for a port based on its label and fabric."""
        if label.startswith('RSVD'):
            return '#606060'
        if 'ISL' in label:
            m = re.search(r'ISL(\d+)', label)
            idx = (int(m.group(1)) - 1) % len(ISL_COLORS) if m else 0
            return ISL_COLORS[idx]
        if 'MLAG/BGP' in label or 'EXT' in label:
            m = re.search(r'(?:MLAG/BGP|EXT)(\d+)', label)
            idx = (int(m.group(1)) - 1) % len(EXT_COLORS) if m else 0
            return EXT_COLORS[idx]
        if 'IPL' in label:
            return 'cyan'
        if 'NB' in label or 'NB-' in label:
            # For NB ports, use the same fabric colors as CN/EB nodes based on port type
            cn_nb_match = re.search(r'CN-NB-(\d+)', label)
            eb_nb_match = re.search(r'EB-NB-(\d+)', label)
            
            if cn_nb_match:
                # This is a CN-NB port - use CN fabric color
                return colors_fabric.get(fabric, '#FC9D74')  # Same as CN nodes
            elif eb_nb_match:
                # This is an EB-NB port - use EB fabric color  
                return colors_fabric.get(fabric, '#FC9D74')  # Same as EB nodes
            return 'tan'  # Default NB color
        # For node types (CN, DN, EB, etc.), use fabric-specific colors
        return colors_fabric.get(fabric, '#FC9D74')

    def _get_port_outline(self, label: str, fabric: str) -> tuple[str, int]:
        """Determines the outline color and width for a port."""
        outline_config = {
            'DN': ('yellow', 2), 'CN': ('green', 2), 'EB': ('black', 1),
            'IE': ('pink', 2), 'GN': ('cyan', 2),
        }
        node_type_prefix = get_port_base_type(label)

        if node_type_prefix == 'NB':
            # For NB ports, use the same border colors as CN/EB nodes based on port type
            cn_nb_match = re.search(r'CN-NB-(\d+)', label)
            eb_nb_match = re.search(r'EB-NB-(\d+)', label)
            
            if cn_nb_match:
                # This is a CN-NB port - use CN border color
                return ('green', 2)  # Same as CN nodes
            elif eb_nb_match:
                # This is an EB-NB port - use EB border color  
                return ('black', 1)  # Same as EB nodes
            return colors_fabric.get(fabric, 'black'), 2
        if node_type_prefix in outline_config:
            return outline_config[node_type_prefix]

        return 'black', 1 # Default outline

    def _get_adaptive_font(self, label: str, max_width: int, max_height: int) -> ImageFont.FreeTypeFont:
        """Finds the largest font size that fits the label within the given dimensions."""
        try:
            initial_font_size = int(max_height * 0.70) if '/' not in label else int(max_height * 0.60)
            font_size = initial_font_size
            while font_size > 5:
                font = ImageFont.truetype(FONT_PATH, font_size)
                bbox = self.draw.textbbox((0, 0), label, font=font)
                text_width = bbox[2] - bbox[0]
                if text_width < (max_width * 0.95): # Leave 5% padding
                    break
                font_size -= 1
            if font_size > 1: font_size -= 1 # Shrink by one more size
            return ImageFont.truetype(FONT_PATH, font_size)
        except IOError:
            return ImageFont.load_default()

    def draw_port(self, port_id: int, label: str, fabric: str):
        """Draws a single port with its label and styling."""
        x, y = self._get_port_coordinates(port_id)
        w, h = self.config['PORT_WIDTH'] + 2, self.config['PORT_HEIGHT'] + 2
        x, y = x - 1, y - 1 # Adjust for increased size

        fill_color = self._get_port_fill_color(label, fabric)
        outline_color, final_outline_width = self._get_port_outline(label, fabric)

        # Scale outline width for display previews
        outline_width = int(final_outline_width / self.display_scale) if 0 < self.display_scale < 1 else final_outline_width

        # Adjust rectangle coordinates for centered outline
        ow_half = outline_width / 2
        rect_coords = [x - ow_half, y - ow_half, x + w + ow_half, y + h + ow_half]
        self.draw.rectangle(rect_coords, fill=fill_color, outline=outline_color, width=outline_width)

        # Prepare text
        font = self._get_adaptive_font(label, w, h)
        text_color = 'white' if label.startswith('RSVD') else 'black'
        bbox = self.draw.textbbox((0, 0), label, font=font)

        # Center text in the original box area
        tx = x + (w - (bbox[2] - bbox[0])) / 2.0
        ty = y + (h - (bbox[3] - bbox[1])) / 2.0 - 1
        self.draw.text((tx, ty), label, fill=text_color, font=font)

class CustomRegexValidator(QValidator):
    """
    A custom QValidator that uses a QRegularExpression.
    This is a workaround for a bug in some Qt versions where
    QRegularExpressionValidator emits console warnings for valid patterns
    that can match an empty string.
    """
    def __init__(self, regex: QRegularExpression, parent=None):
        super().__init__(parent)
        # Store the pattern string, not the QRegularExpression object itself.
        # Reusing the QRegularExpression object across validate() calls
        # appears to trigger an internal bug in Qt, leading to the error.
        self.pattern = regex.pattern()

    def validate(self, input_str: str, pos: int) -> tuple[QValidator.State, str, int]:
        if not input_str:
            return (QValidator.State.Acceptable, input_str, pos)
        # Create a new, temporary QRegularExpression object for each validation.
        # This is the key to avoiding the internal state corruption bug.
        regex = QRegularExpression(self.pattern)
        # Perform the match only on non-empty strings to avoid the Qt bug.
        match = regex.match(input_str)
        
        # A pattern with '*' will always find a match. We need to ensure the
        # entire string is valid according to the pattern.
        if match.hasMatch() and match.captured(0) == input_str:
            return (QValidator.State.Acceptable, input_str, pos)
        else:
            # If the full string doesn't match, it's invalid.
            return (QValidator.State.Invalid, input_str, pos)

class SwitchConfigWorker(QObject):
    """Worker thread for downloading and running the switch_conf.py script."""
    finished: pyqtSignal = pyqtSignal(str)

    def __init__(self, params: dict, skip_download: bool = False):
        super().__init__()
        self.params = params
        self.skip_download = skip_download

    def run(self):
        """The entry point for the worker when run in a QThread."""
        result = self._execute()
        self.finished.emit(result)

    def run_sync(self) -> str:
        """Runs the worker's logic synchronously and returns the result string."""
        return self._execute()

    def _execute(self) -> str:
        """The core logic of the worker, refactored to be callable by both sync and async methods."""
        try:
            config_dir = self.params['config_dir']
            os.makedirs(config_dir, exist_ok=True)
            url = 'https://artifactory.vastdata.com/artifactory/vast-custom/switch_conf/switch_conf-latest/switch_conf.py'
            script_filename = self.params.get('script_filename', 'switch_conf.py')
            script_path = os.path.join(config_dir, script_filename)
            script_downloaded = self.skip_download and os.path.exists(script_path)
            
            if not self.skip_download:
                # Ensure we are not overwriting an existing script (should already be unique)
                if os.path.exists(script_path):
                    script_path = get_unique_filename(script_path)
                    script_filename = os.path.basename(script_path)
                    self.params['script_filename'] = script_filename
                try:
                    response = requests.get(url, timeout=5, stream=True)
                    response.raise_for_status()
                    with open(script_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    script_downloaded = True
                except requests.exceptions.RequestException:
                    # This is handled in the result message
                    pass
            else:
                # Skip download - script already downloaded by first worker
                script_downloaded = os.path.exists(script_path)

            # Ensure command parts reference the actual script filename
            if self.params.get('cmd_parts_for_file'):
                cmd_parts_file = self.params['cmd_parts_for_file'][:]
                if len(cmd_parts_file) >= 2:
                    cmd_parts_file[1] = script_filename
                self.params['cmd_parts_for_file'] = cmd_parts_file
            if self.params.get('cmd_parts_exec'):
                cmd_parts_exec = self.params['cmd_parts_exec'][:]
                if len(cmd_parts_exec) >= 2:
                    cmd_parts_exec[1] = script_filename
                self.params['cmd_parts_exec'] = cmd_parts_exec

            env_vars = self.params['env_vars']
            # Build export statements with special handling for ASNS
            export_lines = []
            for key, value in env_vars.items():
                if key == 'autonomous_systems':
                    export_lines.append(f'export ASNS={value}')
                else:
                    export_lines.append(f'export {key.upper()}={value}')
            output_content = '\n'.join(export_lines)
            cmd_parts_for_file = self.params['cmd_parts_for_file']
            command_line = ' '.join(cmd_parts_for_file)
            output_content += f'\n\n{command_line}\n'
            
            # Extract version from switch_conf.py execution for CFG file header
            version_info = ""
            if script_downloaded:
                try:
                    # Run switch_conf.py with --version to get version info
                    version_cmd = ['python3', script_filename, '--version']
                    version_result = subprocess.run(version_cmd, cwd=config_dir, capture_output=True, text=True, timeout=10)
                    if version_result.returncode == 0 and version_result.stdout.strip():
                        version_info = version_result.stdout.strip()
                except:
                    pass

            # Create descriptive filename with cluster, switch, leaf/spine names
            cluster_name = env_vars.get('clustername', 'VastData-0001')
            hostnames = env_vars.get('hostnames', 'FabricA,FabricB')
            hostname_a, hostname_b = hostnames.split(',') if ',' in hostnames else (hostnames, hostnames)
            switch_type = env_vars.get('lors', 'leaf')
            
            rack_name = env_vars.get("rack_name", "Rack1")
            cfg_filename_base = f"{cluster_name}_{rack_name}_{hostname_a}_{hostname_b}_{switch_type}"
            cfg_filename = get_unique_filename(os.path.join(config_dir, f'{cfg_filename_base}_switch.cfg'))

            with open(cfg_filename, 'w') as f:
                # Write version info as first line if available
                if version_info:
                    f.write(f'# Switch_conf.py Version: {version_info}\n')
                f.write(output_content)

            result_message = f"--- Results for {cfg_filename_base} ---\n"
            result_message += f'Switch config saved to: {os.path.basename(cfg_filename)}\n\n'

            def format_output_for_display(text: str, max_rows: int = 25) -> str:
                """Format output text to limit rows to max_rows and split into columns if needed."""
                if not text:
                    return text
                
                lines = text.strip().split('\n')
                if len(lines) <= max_rows:
                    return text
                
                # Split into columns if too many rows
                num_columns = (len(lines) + max_rows - 1) // max_rows
                lines_per_col = (len(lines) + num_columns - 1) // num_columns
                
                # Pad lines list to make it evenly divisible
                padded_lines = lines + [''] * (num_columns * lines_per_col - len(lines))
                
                # Create column groups
                cols = []
                for i in range(num_columns):
                    start_idx = i * lines_per_col
                    end_idx = min(start_idx + lines_per_col, len(padded_lines))
                    cols.append(padded_lines[start_idx:end_idx])
                
                # Find max length in each column for padding
                max_lengths = [max(len(line) for line in col) for col in cols]
                
                # Format as columns (find the longest column first)
                formatted_lines = []
                for i in range(lines_per_col):
                    row = []
                    for col_idx, col in enumerate(cols):
                        if i < len(col):
                            line = col[i]
                            padded_line = line.ljust(max_lengths[col_idx])
                            row.append(padded_line)
                    if row:
                        formatted_lines.append('   |   '.join(row))
                
                return '\n'.join(formatted_lines)

            if script_downloaded:
                try:
                    cmd_parts_exec = self.params['cmd_parts_exec']
                    env = os.environ.copy()
                    result = subprocess.run(cmd_parts_exec, cwd=config_dir, env=env, capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        formatted_stdout = format_output_for_display(result.stdout)
                        result_message += f'✅ Switch configuration executed successfully!\n\nOutput:\n{formatted_stdout}'
                        if result.stderr:
                            formatted_stderr = format_output_for_display(result.stderr)
                            result_message += f'\n\nWarnings/Info:\n{formatted_stderr}'
                    else:
                        formatted_stderr = format_output_for_display(result.stderr)
                        result_message += f'❌ Switch configuration failed with return code {result.returncode}\n\nError:\n{formatted_stderr}'
                        if result.stdout:
                            formatted_stdout = format_output_for_display(result.stdout)
                            result_message += f'\n\nOutput:\n{formatted_stdout}'
                except subprocess.TimeoutExpired:
                    result_message += '❌ Switch configuration execution timed out (>30 seconds)'
                except Exception as e:
                    result_message += f'❌ Error executing switch configuration: {e}'
            else:
                result_message += '⚠️ Could not download switch_conf.py (VPN/Network Error).\nOnly the local config file was created.'

            return result_message

        except Exception as e:
            return f'An unexpected error occurred: {e}'

class TransparentWidget(QWidget):
    """
    A simple QWidget with an overridden paintEvent to be fully transparent.
    This is a workaround for a common Qt issue where child widgets (like QLabels)
    are incorrectly rendered with partial transparency.
    """
    def paintEvent(self, event):
        # An empty paint event makes the widget transparent without side effects.
        pass

class ScalableLabel(QLabel):
    """A QLabel that scales its pixmap while maintaining aspect ratio."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pixmap = QPixmap()
        self.setMinimumSize(1, 1)

    def setPixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        if not self._pixmap.isNull():
            scaled_pixmap = self._pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter = QPainter(self)
            x = (self.width() - scaled_pixmap.width()) / 2
            y = (self.height() - scaled_pixmap.height()) / 2
            painter.drawPixmap(int(x), int(y), scaled_pixmap)
        else:
            super().paintEvent(event)

    def clear(self):
        self.setPixmap(QPixmap())
        super().clear()


class PortMapperPyQt(QMainWindow):

    def __init__(self, legacy_mode=False):
        super().__init__()
        self.setWindowTitle(f'PortMapper v{SCRIPT_VERSION} - Network Design Studio')
        self.setGeometry(100, 100, 1400, 900)
        self.statusBar()
        self._apply_vast_theme()

        self.legacy_mode = legacy_mode
        self.switch_id = '3'  # Default to Mellanox SN5400 400G
        self.planner = PortPlanner()
        self.layout_config = SWITCH_LAYOUTS[self.switch_id]
        self.base_image: Optional[Image.Image] = None
        self.port_map: list[tuple[int, str]] = []
        self.node_entries: dict[str, dict[str, QWidget]] = {}
        self.uplink_entries: dict[str, dict[str, QWidget]] = {}
        self.config_started = False
        # Preserve node type port mappings when switching to spine
        self.preserved_node_port_map: list[tuple[int, str]] = []
        self.preserved_node_entries: dict[str, dict[str, QWidget]] = {}
        self.previous_vendor = None
        self.legacy_installs_tab_index = -1
        self.multi_rack_tab_index = -1
        self.current_tab_index = 0 # Start at the 'Setup' tab
        # Use the script's directory as the base for DesignOutput
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.out_dir = os.path.join(script_dir, 'DesignOutput')
        
        # Dirty state tracking for user guidance
        self.setup_ready_to_load = False
        self.node_ports_dirty = False
        self.uplink_ports_dirty = False
        self.multi_rack_dirty = False
        
        # --- Cell Planning Mode (Default vs Advanced) ---
        self.cell_planning_mode = 'default'  # 'default' or 'advanced'
        self.cell_planning_advanced_config = {
            'dbox_type': 'CeresV1',  # Mav, CeresV1, CeresV2
            'node_routing': {},  # Per node type: {'CN': 'LEFT', 'EB': 'RIGHT', etc.}
            'uplinks': {
                'IPL': {'groups': 1, 'ports_per_group': 0},
                'ISL': {'groups': 0, 'ports_per_group': 0},
                'EXT': {'groups': 0, 'ports_per_group': 0}
            }
        }
        self.cell_planning_advanced_port_map = []  # Port map for Advanced mode in Cell Planning

        # --- Cluster-specific output directory ---
        # This will be updated when the cluster name changes.
        # It's a property so that it's always up-to-date.
        self._cluster_output_dir = ''
        self._switch_config_dir = ''
        self.cluster_name_entry_for_path = '' # A separate variable to track for path changes
        self.customer_name_entry_for_path = '' # A separate variable to track customer name for path changes
        self.site_name_entry_for_path = '' # A separate variable to track site name for path changes


        # --- Multi-Rack Configuration Data ---
        # Main dictionary to hold all rack configurations
        self.multi_rack_config = {}
        # Dictionary to hold references to the dynamically created widgets for each rack
        self.rack_widgets = {}
        # Keep track of the currently selected rack
        self.current_rack_name = None

        # Fabric design selections
        self.fabric_topology = 'single_pair'  # 'single_pair' or 'leaf_spine'
        self.use_vxlan_overlay = False


        self.rack_name_before_edit = None
        # Timers for debouncing UI updates
        self.preview_timer = QTimer(self)
        self.preview_timer.setSingleShot(True)
        self.preview_timer.timeout.connect(self._do_live_preview)

        self.recalc_timer = QTimer(self)
        self.recalc_timer.setSingleShot(True)
        self.recalc_timer.timeout.connect(self._update_start_ports_realtime)

        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self._perform_resize)
        
        # Timers for auto-assignment (debounced)
        self.auto_assign_nodes_timer = QTimer(self)
        self.auto_assign_nodes_timer.setSingleShot(True)
        self.auto_assign_nodes_timer.timeout.connect(self._auto_assign_nodes)
        
        self.auto_assign_uplinks_timer = QTimer(self)
        self.auto_assign_uplinks_timer.setSingleShot(True)
        self.auto_assign_uplinks_timer.timeout.connect(self._auto_assign_uplinks)

        self.excuses = PLAUSIBLE_EXCUSES

        self._init_validators()
        self._build_ui()
        self._load_default_switch_image()

    def _apply_vast_theme(self):
        """Apply VAST Data VMS-inspired theme with professional blue tones."""
        # VAST Data color palette (deep blue, sky blue, accent colors)
        vast_stylesheet = """
            QMainWindow {
                background-color: #0f1419;
            }
            QWidget {
                background-color: #0f1419;
                color: #ffffff;
            }
            QTabWidget {
                background-color: #0f1419;
                color: #ffffff;
            }
            QTabBar::tab {
                background-color: #1a2332;
                color: #b0b8c8;
                padding: 8px 20px;
                margin: 2px;
                border: none;
                border-radius: 4px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: #2563eb;
                color: #ffffff;
                border-bottom: 3px solid #1d4ed8;
            }
            QTabBar::tab:hover {
                background-color: #1d4ed8;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #1a2332;
                color: #ffffff;
                border: 1px solid #2563eb;
                border-radius: 4px;
                padding: 6px;
                selection-background-color: #2563eb;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                background-color: #162038;
            }
            QLineEdit:disabled {
                background-color: #0d1117;
                color: #4a5568;
                border: 1px solid #1a2332;
            }
            QComboBox {
                background-color: #1a2332;
                color: #ffffff;
                border: 1px solid #2563eb;
                border-radius: 4px;
                padding: 6px;
                selection-background-color: #2563eb;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                color: #2563eb;
            }
            QComboBox QAbstractItemView {
                background-color: #1a2332;
                color: #ffffff;
                selection-background-color: #2563eb;
                border: 1px solid #2563eb;
            }
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #3b82f6;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #0d1117;
                color: #4a5568;
            }
            QCheckBox {
                color: #ffffff;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #1a2332;
                border: 1px solid #2563eb;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #2563eb;
                border: 1px solid #2563eb;
                border-radius: 3px;
                image: url(:/icons/check.png);
            }
            QRadioButton {
                color: #ffffff;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                background-color: #1a2332;
                border: 1px solid #2563eb;
                border-radius: 9px;
            }
            QRadioButton::indicator:checked {
                background-color: #2563eb;
                border: 1px solid #2563eb;
                border-radius: 9px;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QGroupBox {
                color: #ffffff;
                border: 1px solid #2563eb;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                font-weight: 600;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QScrollBar:vertical {
                background-color: #0f1419;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #2563eb;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3b82f6;
            }
            QScrollArea {
                background-color: #0f1419;
                border: none;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #1a2332;
                color: #ffffff;
                border: 1px solid #2563eb;
                border-radius: 4px;
                padding: 6px;
            }
            QTextEdit {
                background-color: #1a2332;
                color: #ffffff;
                border: 1px solid #2563eb;
                border-radius: 4px;
                padding: 6px;
            }
            QFrame {
                background-color: #0f1419;
            }
        """
        self.setStyleSheet(vast_stylesheet)

    def _init_validators(self):
        """Initialize QValidators for reuse."""
        self.hostname_validator = CustomRegexValidator(QRegularExpression(r"[a-zA-Z0-9-]*"))
        # More restrictive IP validator - allows typing but validates format
        self.ipv4_validator = CustomRegexValidator(QRegularExpression(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){0,3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)?$"))
        self.numeric_validator = QIntValidator(0, 999)
        self.port_validator = QIntValidator(1, 64)  # For port inputs (1-64, no decimals, no letters)
        self.mtu_validator = QIntValidator(1500, 9216)
        self.port_list_validator = CustomRegexValidator(QRegularExpression(r"[0-9, -]*"))
        self.vlan_list_validator = CustomRegexValidator(QRegularExpression(r"[0-9, ]*"))
        self.vlan_id_validator = QIntValidator(1, 4094)
        self.peak_bw_validator = QIntValidator(0, 999999)
        self.cluster_name_validator = CustomRegexValidator(QRegularExpression(r"[a-zA-Z0-9-_.]*"))

    def _build_ui(self):
        self.notebook = QTabWidget()
        self.setCentralWidget(self.notebook)

        self.setup_tab = self._build_setup_ui()
        self.node_tab = self._build_node_ui()
        self.output_tab = self._build_output_ui()
        self.multi_rack_tab = self._build_multi_rack_ui()
        self.help_tab = self._build_help_ui()
        self.legacy_installs_tab = self._build_legacy_installs_ui()
 
        self.notebook.addTab(self.setup_tab, 'Setup')
        self.notebook.addTab(self.node_tab, 'Cell Planning')
        self.multi_rack_tab_index = self.notebook.addTab(self.multi_rack_tab, 'Multi-Rack')
        self.notebook.addTab(self.output_tab, 'Output')
        
        # Now that the UI is fully built, initialize leaf/spine logic and NB configuration
        self._on_leaf_spine_changed(self.leaf_spine_combo.currentText())
        self._populate_cn_eb_nb_from_cnodes()
        self._update_uplink_suggestions()
        self.notebook.addTab(self.help_tab, 'Guide')
        self.legacy_installs_tab_index = self.notebook.addTab(self.legacy_installs_tab, 'Legacy Installs')
        self.notebook.setTabVisible(self.legacy_installs_tab_index, False)

        self.notebook.currentChanged.connect(self._on_tab_changed)

        self.notebook.setTabVisible(self.multi_rack_tab_index, False)
        
        # Initialize switch type labels
        current_switch = self.switch_var_combo.currentText() if hasattr(self, 'switch_var_combo') else ""
        if hasattr(self, 'node_switch_label'):
            self.node_switch_label.setText(f"Switch Model: {current_switch}" if current_switch else "")
        if hasattr(self, 'uplink_switch_label'):
            self.uplink_switch_label.setText(f"Switch Model: {current_switch}" if current_switch else "")
        if hasattr(self, 'cell_planning_advanced_switch_label'):
            self.cell_planning_advanced_switch_label.setText(f"Switch Model: {current_switch}" if current_switch else "Switch Model: Not loaded - configure on Setup tab")
        
        # Show welcome dialog after UI is fully initialized
        QTimer.singleShot(100, self._show_welcome_dialog)
        
    def _update_excuse_label(self):
        """Selects a new random excuse and updates the label text."""
        if hasattr(self, 'excuse_label'):
            excuse = f"My Site Survey is late because.... {random.choice(self.excuses)}"
            self.excuse_label.setText(excuse)

    def _update_output_paths(self, text: str):
        """Updates the output directory paths when the cluster name changes."""
        # Sanitize the cluster name to be a valid directory name
        cluster_name = re.sub(r'[^\w\-. ]', '_', text.strip()) or "Unnamed_Cluster"
        self.cluster_name_entry_for_path = cluster_name
        
        # Sanitize the customer name and site name to be valid directory names
        customer_name = re.sub(r'[^\w\-. ]', '_', self.customer_name_entry.text().strip()) or "Customer"
        self.customer_name_entry_for_path = customer_name
        
        site_name = re.sub(r'[^\w\-. ]', '_', self.site_name_entry.text().strip()) or "Site"
        self.site_name_entry_for_path = site_name

        # New directory structure: Projects/CustomerName/SiteName/ClusterName/DesignOutput and SwitchOutput
        # Use absolute paths relative to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, 'Projects', self.customer_name_entry_for_path, self.site_name_entry_for_path, self.cluster_name_entry_for_path)
        self._cluster_output_dir = os.path.join(base_path, 'DesignOutput')
        self._switch_config_dir = os.path.join(base_path, 'SwitchOutput')
        self.out_dir_label.setText(base_path)

    def _update_dynamic_labels(self):
        customer = self.customer_name_entry.text() or "Customer"
        site = self.site_name_entry.text() or "Site"
        cluster = self.cluster_name_entry.text() or "Cluster"
        ls_type = self.leaf_spine_combo.currentText() or "Unknown"
        ha = self.ha_entry.text() or 'SwitchA'
        hb = self.hb_entry.text() or 'SwitchB'

        live_preview_text = f"Live Preview ({customer} / {site} / {cluster} / {ls_type} / {ha} / {hb})"
        if hasattr(self, 'node_live_preview_label'):
            self.node_live_preview_label.setText(live_preview_text)
        if hasattr(self, 'uplink_live_preview_label'):
            self.uplink_live_preview_label.setText(live_preview_text)

    def _update_mgmt_ips_from_gateway(self, text):
        """Populates FabricA Mgmt IP prefix from the gateway IP."""
        parts = text.split('.')
        if len(parts) >= 3:
            try:
                prefix_parts = [str(int(p)) for p in parts[:3] if p.isdigit() and 0 <= int(p) <= 255]
                if len(prefix_parts) == 3:
                    base_prefix = ".".join(prefix_parts)
                    if not self.switch_a_mgmt_ip_entry.text().startswith(base_prefix + '.'):
                        self.switch_a_mgmt_ip_entry.setText(f"{base_prefix}.")
            except (ValueError, IndexError):
                pass

    def _update_fabric_b_ip_from_a(self, text):
        """Auto-increments FabricB IP from a valid FabricA IP."""
        try:
            ip_a = ipaddress.ip_address(text)
            ip_b = ip_a + 1
            self.switch_b_mgmt_ip_entry.setText(str(ip_b))
        except ValueError:
            pass

    def _sync_customer_name_to_legacy(self, text):
        """Syncs Customer Name from setup to Legacy Installs."""
        if hasattr(self, 'legacy_customer'):
            self.legacy_customer.setText(text)
    
    def _update_button_indicator(self, button: QPushButton, needs_action: bool, base_text: str):
        """Updates a button with an arrow indicator when action is needed."""
        if needs_action:
            button.setText(f"➤ {base_text}")
            # Special highlighting for Assign Switch button
            if base_text == 'Assign Switch':
                button.setStyleSheet("""
                    QPushButton {
                        font-weight: bold;
                        font-size: 14px;
                        background-color: #FFA500;
                        color: white;
                        border: 3px solid #FFD700;
                        padding: 8px 16px;
                        border-radius: 6px;
                    }
                    QPushButton:hover {
                        background-color: #FF8C00;
                        border: 3px solid #FFA500;
                    }
                """)
                # Add pulsing animation
                if not hasattr(button, '_pulse_animation') or button._pulse_animation is None:
                    button._pulse_animation = QPropertyAnimation(button, b"windowOpacity")
                    button._pulse_animation.setDuration(1500)
                    button._pulse_animation.setStartValue(0.7)
                    button._pulse_animation.setEndValue(1.0)
                    button._pulse_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
                    button._pulse_animation.setLoopCount(-1)  # Infinite loop
                    button._pulse_animation.start()
            else:
                # Other action buttons get orange text when action needed
                button.setStyleSheet("QPushButton { font-weight: bold; color: #FFA500; }")
        else:
            button.setText(base_text)
            button.setStyleSheet("QPushButton { color: black; }")
            # Stop animation if it exists
            if hasattr(button, '_pulse_animation') and button._pulse_animation:
                button._pulse_animation.stop()
                button.setWindowOpacity(1.0)
    
    def _update_tab_badge(self, tab_index: int, has_warning: bool, base_name: str):
        """Updates a tab name with a warning badge when changes are pending."""
        if has_warning:
            self.notebook.setTabText(tab_index, f"{base_name} ⚠")
        else:
            self.notebook.setTabText(tab_index, base_name)
    
    def _check_setup_ready(self):
        """Checks if the setup is ready to load and updates the Load button indicator."""
        # Setup is considered ready if a switch model is selected
        if not self.config_started and hasattr(self, 'load_button'):
            self.setup_ready_to_load = True
            self._update_button_indicator(self.load_button, True, 'Assign Switch')
    
    def _show_welcome_dialog(self):
        """Shows a welcome dialog with quick start instructions on first launch."""
        settings = QSettings('VastData', 'PortMapper')
        show_welcome = settings.value('show_welcome_dialog', True, type=bool)
        
        if not show_welcome:
            return
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(f'Welcome to PortMapper v{SCRIPT_VERSION} - Network Design Studio')
        msg_box.setIcon(QMessageBox.Icon.Information)

        welcome_text = """
<h2>PortMapper v6.0 - Network Design Studio</h2>
<p><i>Professional network topology design for storage systems</i></p>
<h3>Quick Start Guide</h3>
<p><b>Follow these steps to configure your switch:</b></p>

<p><b>1️⃣ Select a switch model and click "Assign Switch"</b><br>
   &nbsp;&nbsp;&nbsp;Choose your hardware from the dropdown</p>

<p><b>2️⃣ Fill in cluster setup details</b><br>
   &nbsp;&nbsp;&nbsp;Enter hostnames, IPs, and configuration values</p>

<p><b>3️⃣ Assign Node and Uplink ports</b><br>
   &nbsp;&nbsp;&nbsp;Configure ports in the Node Types and Uplinks tabs</p>

<p><b>💡 TIP:</b> Look for buttons with <b>➤ arrows</b> and <b>⚠ warning badges</b><br>
   &nbsp;&nbsp;&nbsp;in tab names to know what needs your attention!</p>
"""
        msg_box.setText(welcome_text)
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        
        # Add "Don't show again" checkbox
        dont_show_cb = QCheckBox("Don't show this again")
        msg_box.setCheckBox(dont_show_cb)
        
        # Custom button
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.button(QMessageBox.StandardButton.Ok).setText("Let's Get Started!")
        
        msg_box.exec()
        
        # Save preference
        if dont_show_cb.isChecked():
            settings.setValue('show_welcome_dialog', False)
    
    def _mark_node_tab_dirty(self):
        """Marks the Node Types tab as having unsaved changes (deprecated - kept for compatibility)."""
        # No longer needed with auto-assignment, but kept to avoid breaking existing connections
        pass
    
    def _mark_uplink_tab_dirty(self):
        """Marks the Uplinks tab as having unsaved changes (deprecated - kept for compatibility)."""
        # No longer needed with auto-assignment, but kept to avoid breaking existing connections
        pass
    
    def _mark_multi_rack_dirty(self):
        """Marks the Multi-Rack tab as having unsaved changes."""
        if self.config_started and self.multi_rack_checkbox.isChecked():
            self.multi_rack_dirty = True
            if self.multi_rack_tab_index != -1:
                self._update_tab_badge(self.multi_rack_tab_index, True, 'Multi-Rack')
    
    def _schedule_auto_assign_nodes(self):
        """Schedules automatic node port assignment after a delay (debounced)."""
        if self.config_started:
            self.auto_assign_nodes_timer.start(800)  # 800ms delay for debouncing
    
    def _schedule_auto_assign_uplinks(self):
        """Schedules automatic uplink port assignment after a delay (debounced)."""
        if self.config_started:
            self.auto_assign_uplinks_timer.start(800)  # 800ms delay for debouncing
    
    def _auto_assign_nodes(self):
        """Automatically assigns node ports without user clicking a button."""
        # First check if total ports would exceed switch capacity
        if not self._validate_total_port_count():
            # Still update the preview to show current state (without assigning)
            self._do_live_preview()
            return  # Don't assign if it would exceed capacity
        # Call the actual generate_node_ports function with silent flag
        self.generate_node_ports(silent=True)
    
    def _auto_assign_uplinks(self):
        """Automatically assigns uplink ports without user clicking a button."""
        # First check if total ports would exceed switch capacity
        if not self._validate_total_port_count():
            # Still update the preview to show current state (without assigning)
            self._do_live_preview()
            return  # Don't assign if it would exceed capacity
        # Call the actual generate_uplink_ports function with silent flag
        self.generate_uplink_ports(silent=True)
    
    def _validate_total_port_count(self):
        """Validates that total ports needed don't exceed switch capacity. Returns True if valid."""
        total_ports_needed = 0
        
        # Calculate node ports needed
        for nt, ent in self.node_entries.items():
            cnt = safe_int(ent['cnt'].text())
            rsv = safe_int(ent['rsv'].text())
            split = ent['split_cb'].isChecked()
            fac = safe_int(ent['fac'].currentText(), 1) if split else 1
            phys_needed = (math.ceil(cnt / fac) if split else cnt) + rsv
            total_ports_needed += phys_needed
        
        # Calculate uplink ports needed
        for ut, ent in self.uplink_entries.items():
            ppg = safe_int(ent['ppg'].text())
            rsv = safe_int(ent['rsv'].text())
            split = ent['split_cb'].isChecked()
            fac = safe_int(ent['fac'].currentText(), 1) if split else 1
            groups = 1 if ut in ['IPL', 'NB'] else safe_int(ent.get('gcnt', QLineEdit('1')).text())
            phys_per_group = math.ceil(ppg / fac) if split else ppg
            total_span = (phys_per_group + rsv) * groups
            total_ports_needed += total_span
        
        # Check against switch capacity
        if total_ports_needed > self.layout_config['PORT_COUNT']:
            # Show warning in both Node and Uplink preview labels
            warning_msg = f'⚠️ WARNING: Total ports needed ({total_ports_needed}) exceeds switch capacity ({self.layout_config["PORT_COUNT"]})'
            warning_style = "color: #FFA500; font-weight: bold; font-size: 12pt;"
            
            if hasattr(self, 'node_live_preview_label'):
                self.node_live_preview_label.setText(warning_msg)
                self.node_live_preview_label.setStyleSheet(warning_style)
            if hasattr(self, 'uplink_live_preview_label'):
                self.uplink_live_preview_label.setText(warning_msg)
                self.uplink_live_preview_label.setStyleSheet(warning_style)
            return False
        else:
            # Clear any warnings
            if hasattr(self, 'node_live_preview_label'):
                self.node_live_preview_label.setText('')
                self.node_live_preview_label.setStyleSheet("")
            if hasattr(self, 'uplink_live_preview_label'):
                self.uplink_live_preview_label.setText('')
                self.uplink_live_preview_label.setStyleSheet("")
            return True

    def _on_legacy_mode_toggled(self, is_checked: bool):
        """Toggles the visibility of the Legacy Installs tab."""
        if self.legacy_installs_tab_index != -1:
            # Simply setting the tab's visibility is sufficient. The _on_tab_changed
            # signal handler is designed to correctly manage access.
            self.notebook.setTabVisible(self.legacy_installs_tab_index, is_checked)

    def _on_multi_rack_toggled(self, checked):
        """Shows/hides tabs to enforce a clear single-rack vs. multi-rack mode."""
        if self.multi_rack_tab_index != -1:
            # When multi-rack is checked, show the multi-rack tab.
            # Node Types and Uplinks tabs remain visible and can co-exist.
            self.notebook.setTabVisible(self.multi_rack_tab_index, checked)

        if checked and not self.multi_rack_config:
            # Defer initialization to ensure UI is ready
            QTimer.singleShot(0, self._initialize_first_rack_from_main_config)
        self._draw_multi_rack_preview()

    def _on_rack_data_changed(self, rack_name: str, data_path: list[str], widget: QWidget):
        """
        A generic handler for saving changes from any rack detail widget to the data model.
        This replaces _on_rack_detail_changed, _on_rack_node_changed, and _on_rack_uplink_changed.

        :param rack_name: The name of the rack being edited.
        :param data_path: A list representing the path to the data in the config dict,
                          e.g., ['hostname_a'] or ['nodes', 'CN', 'count'].
        :param widget: The widget that triggered the change.
        """
        if rack_name not in self.multi_rack_config:
            return

        # Traverse the data path to get to the target dictionary
        current_level = self.multi_rack_config[rack_name]
        for key in data_path[:-1]:
            current_level = current_level.setdefault(key, {})

        field_key = data_path[-1]

        # Determine the new value based on widget type
        new_value = None
        if isinstance(widget, QLineEdit):
            # For numeric fields, convert to int. For others (hostnames), use string.
            # The 'start' field for node numbers is special: an empty string is a valid
            # "not set" state and should not be converted to 0.
            if field_key == 'start' and widget.text().strip() == '':
                new_value = ''
            elif any(k in field_key for k in ['count', 'ports_per_group', 'reserved', 'start', 'groups', 'peak_bw_goal']):
                new_value = safe_int(widget.text())
            else:
                new_value = widget.text().strip()
        elif isinstance(widget, QCheckBox):
            new_value = widget.isChecked()
        elif isinstance(widget, QComboBox):
            # For split factor, convert to int. For others (units), use string.
            if 'factor' in field_key:
                new_value = safe_int(widget.currentText())
            else:
                new_value = widget.currentText()

        # Update the data model if the value has changed
        if new_value is not None and current_level.get(field_key) != new_value:
            current_level[field_key] = new_value

        # Apply IPL/ISL mutual exclusion logic for leaf switches
        if (data_path == ['uplinks', 'IPL', 'ports_per_group'] or 
            data_path == ['uplinks', 'ISL', 'ports_per_group']) and \
           self.leaf_spine_combo.currentText() == 'leaf':
            self._update_multi_rack_ipl_isl_exclusion(rack_name)

        # Recalculate and redraw
        self._calculate_and_store_rack_port_map(rack_name)
        self._sched_multi_rack_preview()

    def _update_multi_rack_ipl_isl_exclusion(self, rack_name: str):
        """Update IPL/ISL mutual exclusion logic for multi-rack leaf switches."""
        if rack_name not in self.multi_rack_config:
            return
            
        rack_data = self.multi_rack_config[rack_name]
        uplinks_data = rack_data.get('uplinks', {})
        
        # Check current IPL and ISL configurations
        ipl_configured = uplinks_data.get('IPL', {}).get('ports_per_group', 0) > 0
        isl_configured = uplinks_data.get('ISL', {}).get('ports_per_group', 0) > 0
        
        # Apply mutual exclusion logic - disable UI widgets like the uplink tab does
        if hasattr(self, 'rack_widgets') and rack_name in self.rack_widgets:
            fields = self.rack_widgets[rack_name]['fields']
            if 'uplinks' in fields:
                if 'IPL' in fields['uplinks'] and 'ISL' in fields['uplinks']:
                    ipl_widgets = fields['uplinks']['IPL']
                    isl_widgets = fields['uplinks']['ISL']
                    
                    # Both can now coexist - always enable both
                    self._enable_multi_rack_uplink_widgets(ipl_widgets)
                    self._enable_multi_rack_uplink_widgets(isl_widgets)

    def _disable_multi_rack_uplink_widgets(self, widgets):
        """Disable multi-rack uplink widgets and grey them out."""
        for widget_name in ['groups', 'ports_per_group', 'start', 'reserved']:
            if widget_name in widgets:
                widgets[widget_name].setEnabled(False)
                widgets[widget_name].setStyleSheet("QLineEdit:disabled { background-color: #555555; color: #AAAAAA; }")
        if 'split' in widgets:
            widgets['split'].setEnabled(False)
            widgets['split'].setStyleSheet("QCheckBox:disabled { color: #AAAAAA; }")

    def _enable_multi_rack_uplink_widgets(self, widgets):
        """Enable multi-rack uplink widgets and reset styling."""
        for widget_name in ['groups', 'ports_per_group', 'start', 'reserved']:
            if widget_name in widgets:
                widgets[widget_name].setEnabled(True)
                widgets[widget_name].setStyleSheet("")  # Reset to default
        if 'split' in widgets:
            widgets['split'].setEnabled(True)
            widgets['split'].setStyleSheet("")  # Reset to default

    def _on_rack_switch_model_changed(self, rack_name: str, switch_name: str):
        """Handles when a rack's specific switch model is changed."""
        if rack_name not in self.multi_rack_config:
            return

        # Find the switch_id for the given switch_name
        new_switch_id = next((k for k, v in SWITCH_LAYOUTS.items() if v['NAME'] == switch_name), None)
        if new_switch_id:
            self.multi_rack_config[rack_name]['switch_id'] = new_switch_id
            # Recalculate ports and update the preview for this rack
            self._calculate_and_store_rack_port_map(rack_name)
            self._sched_multi_rack_preview()

    def _get_next_cloned_rack_name(self, source_name: str) -> str:
        """Generates the next available rack name based on a source name (e.g., 'Test' -> 'Test 1')."""
        # Find the base name by stripping any trailing number and space (e.g., "Test 1" -> "Test")
        base_name = re.sub(r'\s+\d+$', '', source_name).strip()
        i = 1
        # Find the next available number for this base name
        while True:
            next_name = f"{base_name} {i}"
            if next_name not in self.multi_rack_config:
                return next_name
            i += 1

    def _on_clone_rack_clicked(self):
        """Handles the 'Clone Rack' button click."""
        current_item = self.rack_list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Rack Selected", "Please select a rack to clone.")
            return

        source_rack_name = current_item.text()
        source_data = self.multi_rack_config.get(source_rack_name)
        if not source_data:
            QMessageBox.critical(self, "Error", f"Could not find data for '{source_rack_name}'.")
            return

        # --- Suggest new values for the clone ---
        import copy
        cloned_data = copy.deepcopy(source_data)

        # Generate the new rack name based on the source rack's name
        new_rack_name = self._get_next_cloned_rack_name(source_rack_name)

        # Suggest new hostnames by prepending the new rack number.
        # Extract the number from the new rack name (e.g., "Leaf Rack 2" -> 2).
        new_rack_num_str = ''.join(filter(str.isdigit, new_rack_name)) or '1'
        new_rack_num = int(new_rack_num_str)
        cloned_data['hostname_a'] = self._generate_rack_hostname(source_data.get('hostname_a', ''), new_rack_num)
        cloned_data['hostname_b'] = self._generate_rack_hostname(source_data.get('hostname_b', ''), new_rack_num)

        # Increment starting node numbers based on source rack's node counts
        if 'nodes' in cloned_data:
            for node_type in self.node_types:
                if node_type in cloned_data['nodes']:
                    source_node_data = cloned_data['nodes'][node_type]
                    source_count = source_node_data.get('count', 0)
                    source_starting_node = source_node_data.get('starting_node', 
                        {'DN': 100, 'CN': 1, 'EB': 1, 'IE': 1, 'GN': 1}.get(node_type, 1))
                    # Calculate new starting node: source starting + source count
                    new_starting_node = source_starting_node + source_count
                    cloned_data['nodes'][node_type]['starting_node'] = new_starting_node

        # Suggest new management IPs by incrementing the highest existing IP
        all_ips = []
        for rack_cfg in self.multi_rack_config.values():
            for key in ['mgmt_ip_a', 'mgmt_ip_b']:
                ip_str = rack_cfg.get(key, '').strip()
                if ip_str:
                    try:
                        all_ips.append(ipaddress.ip_address(ip_str))
                    except ValueError:
                        pass # Ignore invalid IPs in existing configs

        if all_ips:
            max_ip = max(all_ips)
            cloned_data['mgmt_ip_a'] = str(max_ip + 1)
            cloned_data['mgmt_ip_b'] = str(max_ip + 2)
        else: # Fallback if no valid IPs exist yet
            cloned_data['mgmt_ip_a'] = ''
            cloned_data['mgmt_ip_b'] = ''

        # Pass the generated name and cloned data to _add_rack to create the new rack.
        self._add_rack(new_rack_name=new_rack_name, source_rack_data=cloned_data)


    def _generate_rack_hostname(self, base_hostname: str, rack_num: int) -> str:
        """
        Generates a rack-specific hostname by prepending a rack identifier.
        It strips any existing 'rX-' prefix before prepending the new one.
        Example: "SWA" -> "r2-SWA"; "r1-SWA" -> "r2-SWA"
        """
        if not base_hostname:
            return ''
        # Strip existing rack prefix (e.g., "r1-SWA" -> "SWA") using a case-insensitive regex.
        cleaned_hostname = re.sub(r'^[rR]\d+-', '', base_hostname)
        # Prepend the new rack prefix.
        return f"r{rack_num}-{cleaned_hostname}"

    def resizeEvent(self, event):
        """Handle window resize with debouncing."""
        self.resize_timer.start(50)
        super().resizeEvent(event)

    def _perform_resize(self):
        """The actual resize logic, called by the timer."""
        self._on_tab_changed(self.notebook.currentIndex())
        # Also trigger a redraw of the multi-rack preview if that tab is visible
        if self.multi_rack_tab_index != -1 and self.notebook.isTabVisible(self.multi_rack_tab_index):
            self._draw_multi_rack_preview()


    def _on_manual_toggle(self, key: str, is_node_tab: bool):
        entries = self.node_entries if is_node_tab else self.uplink_entries
        ent = entries[key]
        start_entry: QLineEdit = ent['st']
        lock_cb: QCheckBox = ent['lock_cb']

        start_entry.setEnabled(lock_cb.isChecked())
        if not lock_cb.isChecked():
            start_entry.clear()

        if is_node_tab:
            self._sched_both_node_updates()
        else:
            self._sched_both_uplink_updates()

    def _load_default_switch_image(self):
        path = resource_path(self.layout_config['IMAGE'])
        try:
            self.base_image = Image.open(path).convert('RGBA')
        except FileNotFoundError:
            self.base_image = None
            print(f"Warning: Could not load base image at {path}")

    def _reset_all_inputs(self):
        # Block signals to prevent triggering dirty state during reset
        for ent in self.node_entries.values():
            for widget in ent.values():
                if hasattr(widget, 'blockSignals'):
                    widget.blockSignals(True)
            ent['cnt'].clear()
            ent['rsv'].clear()
            ent['st'].clear()
            ent['split_cb'].setChecked(False)
            if 'fac' in ent and isinstance(ent['fac'], QComboBox): ent['fac'].setCurrentIndex(0)
            ent['lock_cb'].setChecked(False)
            ent['st'].setEnabled(False)
            for widget in ent.values():
                if hasattr(widget, 'blockSignals'):
                    widget.blockSignals(False)

        for ent in self.uplink_entries.values():
            # Block signals
            for widget in ent.values():
                if hasattr(widget, 'blockSignals'):
                    widget.blockSignals(True)
            # Check if the widget exists before trying to modify it.
            if 'gcnt' in ent and ent['gcnt']: ent['gcnt'].clear()
            if 'ppg' in ent and ent['ppg']: ent['ppg'].clear()
            if 'rsv' in ent and ent['rsv']: ent['rsv'].clear()
            if 'st' in ent and ent['st']: ent['st'].clear()
            if 'split_cb' in ent and ent['split_cb']: ent['split_cb'].setChecked(False)
            if 'fac' in ent and isinstance(ent['fac'], QComboBox): ent['fac'].setCurrentIndex(0)
            if 'lock_cb' in ent and ent['lock_cb']: ent['lock_cb'].setChecked(False)
            if 'st' in ent and ent['st']: ent['st'].setEnabled(False)
            # Unblock signals
            for widget in ent.values():
                if hasattr(widget, 'blockSignals'):
                    widget.blockSignals(False)

        self.port_map.clear()
        
        # Reset CN, EB, and NB based on cnode entries if 2nd NIC is enabled
        if hasattr(self, 'use_2nd_nic_checkbox') and hasattr(self, 'use_converged_networking_checkbox'):
            if self.use_2nd_nic_checkbox.isChecked() and self.use_converged_networking_checkbox.isChecked():
                self._populate_cn_eb_nb_from_cnodes()
        
        # Ensure IPL and NB group counts are set to 1 (disabled fields)
        if 'IPL' in self.uplink_entries and 'gcnt' in self.uplink_entries['IPL']:
            self.uplink_entries['IPL']['gcnt'].setText('1')
            self.uplink_entries['IPL']['gcnt'].setEnabled(False)
        if 'NB' in self.uplink_entries and 'gcnt' in self.uplink_entries['NB']:
            self.uplink_entries['NB']['gcnt'].setText('1')
            self.uplink_entries['NB']['gcnt'].setEnabled(False)

    def _reset_multi_rack_tab(self):
        """Clears all data and UI elements related to the multi-rack tab."""
        # Clear the underlying data model
        self.multi_rack_config.clear()

        # Remove all dynamically created rack detail widgets from the stacked layout
        for rack_name, rack_widget_info in self.rack_widgets.items():
            widget_to_remove = rack_widget_info['widget']
            self.rack_details_stack.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
        self.rack_widgets.clear()

        # Clear the list widget in the UI
        self.rack_list_widget.clear()

        # Reset the view to the empty placeholder
        self.rack_details_stack.setCurrentWidget(self.empty_details_widget)
        self.current_rack_name = None

        # Clear the preview canvases
        self.multi_rack_canvas_a.clear()
        self.multi_rack_canvas_b.clear()

    def _reset_legacy_tab(self):
        """Clears all input fields on the Legacy Installs tab."""
        # Iterate over all attributes of the class
        for attr_name in dir(self):
            # Find widgets that belong to the legacy tab
            if attr_name.startswith('legacy_'):
                widget = getattr(self, attr_name)
                if isinstance(widget, QLineEdit):
                    widget.clear()
                elif isinstance(widget, QComboBox):
                    # Reset combo boxes to their first item
                    widget.setCurrentIndex(0)
                elif isinstance(widget, QCheckBox):
                    # Reset checkboxes to unchecked, except for B2B IPMI which defaults to checked
                    widget.setChecked(attr_name == 'legacy_b2b_ipmi')
        # Also clear the output text area
        if hasattr(self, 'legacy_output_text'):
            self.legacy_output_text.clear()

    def _reset_and_restart(self):
        reply = QMessageBox.question(self, 'Confirm Reset',
                                     'Are you sure you want to start over? All current configuration will be lost.',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return

        self.config_started = False
        
        # Reset switch_id to default
        self.switch_id = '3'  # Default to Mellanox SN5400 400G
        
        self._reset_all_inputs()
        self._reset_multi_rack_tab()
        self._reset_legacy_tab()
        # Also reset the multi-rack checkbox on the setup tab
        self.multi_rack_checkbox.setChecked(False)

        # Reset setup tab fields to their default values
        self.customer_name_entry.setText('Monster CSP')
        self.site_name_entry.setText('500MW-1')
        self.ha_entry.setText('SWA')
        self.hb_entry.setText('SWB')
        self.cluster_name_entry.setText('Quota-Destroyer-001')
        self.net_def_route_entry.setText('1.1.1.1')
        self.net_cidr_combo.setCurrentIndex(self.net_cidr_combo.findText('24'))
        self.uplink_speed_combo.setCurrentIndex(0)
        self.ntp_server_entry.setText('2.2.2.2')
        self.leaf_spine_combo.setCurrentIndex(self.leaf_spine_combo.findText('leaf'))
        self.switch_a_mgmt_ip_entry.setText('1.1.1.10')
        self.switch_b_mgmt_ip_entry.setText('1.1.1.11')
        self.vxlan_checkbox.setChecked(False)
        self.customer_vlans_entry.clear()
        self.bgp_asn_entry.clear()
        self.data_vlan_entry.setText('69')
        self.peak_bw_goal_entry.clear()
        self.peak_bw_units_combo.setCurrentIndex(0)
        
        # Reset clone rack defaults
        self.clone_rack_name_entry.setText("Leaf Rack")
        self.clone_rack_type_combo.setCurrentText('leaf')

        # Clear canvases
        for canvas in [self.node_canvas_a, self.node_canvas_b, self.canvas_a, self.canvas_b]:
            canvas.clear()

        # Reset UI state
        self.reset_button.setEnabled(False)
        self.load_button.setVisible(True)
        
        # Reset status indicator
        if hasattr(self, 'setup_status_label'):
            self.setup_status_label.setText("⚠️ Status: Switch not assigned yet")
            self.setup_status_label.setStyleSheet("font-weight: bold; color: #FFA500; padding: 5px;")
        
        # Reset dirty state flags
        self.setup_ready_to_load = False
        self.node_ports_dirty = False
        self.uplink_ports_dirty = False
        self.multi_rack_dirty = False
        
        # Clear all tab badges
        self._update_tab_badge(self.notebook.indexOf(self.node_tab), False, 'Cell Planning')
        if self.multi_rack_tab_index != -1:
            self._update_tab_badge(self.multi_rack_tab_index, False, 'Multi-Rack')
        
        # Show welcome dialog again
        QTimer.singleShot(200, self._show_welcome_dialog)
        
        self._update_vendor_options()
        self._on_vendor_changed()
        self.notebook.setCurrentIndex(0)

    def _update_hostname_labels(self):
        ha = self.ha_entry.text().strip() or 'FabricA'
        hb = self.hb_entry.text().strip() or 'FabricB'
        self.switch_a_mgmt_ip_label.setText(f'{ha} Mgmt IP:')
        self.switch_b_mgmt_ip_label.setText(f'{hb} Mgmt IP:')
        self._update_dynamic_labels()

    def _on_vendor_changed(self, *_):
        current_vendor = self.vendor_combo.currentText()
        if self.previous_vendor != current_vendor:
            # VXLAN is no longer automatically set based on vendor
            # It will be set based on BGP ASN presence
            
            supports_uplink_split = current_vendor != 'Cisco-NXOS'
            for ut in ['ISL', 'MLAG/BGP']:
                if ut in self.uplink_entries:
                    ent = self.uplink_entries[ut]
                    if ent.get('split_cb'):
                        ent['split_cb'].setEnabled(supports_uplink_split)
                        if not supports_uplink_split:
                            ent['split_cb'].setChecked(False)

            self.previous_vendor = current_vendor
            self._sched_both_uplink_updates()

    def _update_vendor_options(self):
        switch_name = self.layout_config['NAME']

        if 'Mellanox' in switch_name:
            vendor_values = ['MNLX-Cumulus', 'MNLX-Onyx']
            default_vendor = 'MNLX-Cumulus'
        elif 'Cisco' in switch_name:
            vendor_values = ['Cisco-NXOS']
            default_vendor = 'Cisco-NXOS'
        elif 'Arista' in switch_name:
            vendor_values = ['Arista-EOS']
            default_vendor = 'Arista-EOS'
        else:
            vendor_values = ['Cisco-NXOS', 'MNLX-Onyx', 'MNLX-Cumulus']
            default_vendor = ''

        self.vendor_combo.clear()
        self.vendor_combo.addItems(vendor_values)
        current_text = self.vendor_combo.currentText()
        if not current_text or current_text not in vendor_values:
            idx = self.vendor_combo.findText(default_vendor)
            if idx != -1:
                self.vendor_combo.setCurrentIndex(idx)

    def _update_switch_preview_image(self):
        try:
            image_path = resource_path(self.layout_config['IMAGE'])
            pixmap = QPixmap(image_path)
            self.switch_preview_label.setPixmap(pixmap)
        except Exception as e:
            print(f"INFO: Could not load switch preview image: {e}")
            self.switch_preview_label.clear()

    def _build_setup_ui(self):
        # The container for the whole tab.
        container_widget = QWidget()
        container_widget.setObjectName("SetupTab")

        # Use a QVBoxLayout to stack the scroll area and the arrow indicator below it.
        container_layout = QVBoxLayout(container_widget)
        container_layout.setContentsMargins(0,0,0,0)

        # Arrow indicator for scrolling up, placed above the scroll area
        self.setup_scroll_arrow_up = QLabel("▲")
        self.setup_scroll_arrow_up.setStyleSheet("color: white; font-size: 24px; background-color: transparent;")
        self.setup_scroll_arrow_up.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setup_scroll_arrow_up.setToolTip("More content above")
        container_layout.addWidget(self.setup_scroll_arrow_up)

        scroll_area = QScrollArea()
        self.setup_scroll_area = scroll_area # Store reference
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        # Make the scroll area and its viewport transparent to see the image behind.
        scroll_area.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; border: none; }")

        # The actual content widget that goes inside the scroll area.
        content_widget = TransparentWidget()
        main_layout = QVBoxLayout(content_widget)
        main_layout.setContentsMargins(15, 15, 15, 15) # Add some padding
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_hbox = QHBoxLayout()

        # --- Left Side: Initial Setup Group (1/3 width) ---
        initial_setup_group = QGroupBox("Initial Setup")
        initial_setup_layout = QGridLayout(initial_setup_group)

        model_label = QLabel('Select switch model:')
        model_label.setToolTip("Select the physical switch hardware model.\nThis determines port count, layout, and available features.")
        initial_setup_layout.addWidget(model_label, 0, 0)
        self.switch_var_combo = QComboBox()
        models = [v['NAME'] for v in SWITCH_LAYOUTS.values()]
        self.switch_var_combo.addItems(models)
        # Set the initial selection to match the current switch_id
        current_switch_name = SWITCH_LAYOUTS[self.switch_id]['NAME']
        switch_index = self.switch_var_combo.findText(current_switch_name)
        if switch_index >= 0:
            self.switch_var_combo.setCurrentIndex(switch_index)
        self.switch_var_combo.setMinimumWidth(self.switch_var_combo.minimumSizeHint().width() + 8)
        self.switch_var_combo.setToolTip("Select the physical switch hardware model.\nThis determines port count, layout, and available features.")
        self.switch_var_combo.currentTextChanged.connect(self._switch_selected)
        self.switch_var_combo.currentTextChanged.connect(self._check_setup_ready)
        initial_setup_layout.addWidget(self.switch_var_combo, 0, 1)

        ha_label = QLabel('Hostname A (Or blank):')
        ha_label.setToolTip("Enter the hostname for the first switch (Fabric A).\nThis is used in diagrams and output filenames.")
        initial_setup_layout.addWidget(ha_label, 1, 0)
        self.ha_entry = QLineEdit('SWA')
        self.ha_entry.setValidator(self.hostname_validator)
        self.ha_entry.setToolTip("Enter the hostname for the first switch (Fabric A).\nThis is used in diagrams and output filenames.")
        self.ha_entry.textChanged.connect(self._update_hostname_labels)
        initial_setup_layout.addWidget(self.ha_entry, 1, 1)
        # Connect signal to update Rack 1 in real-time
        self.ha_entry.textChanged.connect(
            lambda: self._sync_main_config_to_rack1('hostname_a', self.ha_entry.text())
        )

        hb_label = QLabel('Hostname B (Or blank):')
        hb_label.setToolTip("Enter the hostname for the second switch (Fabric B).\nThis is used in diagrams and output filenames.")
        initial_setup_layout.addWidget(hb_label, 2, 0)
        self.hb_entry = QLineEdit('SWB')
        self.hb_entry.setValidator(self.hostname_validator)
        self.hb_entry.setToolTip("Enter the hostname for the second switch (Fabric B).\nThis is used in diagrams and output filenames.")
        self.hb_entry.textChanged.connect(self._update_hostname_labels)
        # Connect signal to update Rack 1 in real-time
        initial_setup_layout.addWidget(self.hb_entry, 2, 1)
        self.hb_entry.textChanged.connect(
            lambda: self._sync_main_config_to_rack1('hostname_b', self.hb_entry.text())
        )

        self.multi_rack_checkbox = QCheckBox("Multi Rack Configuration")
        self.multi_rack_checkbox.setToolTip("Enable multi-rack configuration mode.")
        self.multi_rack_checkbox.toggled.connect(self._on_multi_rack_toggled)
        # Multi rack checkbox hidden from UI
        # initial_setup_layout.addWidget(self.multi_rack_checkbox, 3, 0, 1, 1)

        self.legacy_mode_checkbox = QCheckBox("Enable Legacy Configuration")
        self.legacy_mode_checkbox.setToolTip("Show the 'Legacy Installs' tab for older configuration methods.")
        self.legacy_mode_checkbox.toggled.connect(self._on_legacy_mode_toggled)
        initial_setup_layout.addWidget(self.legacy_mode_checkbox, 3, 0)
        
        # Add status indicator
        self.setup_status_label = QLabel("⚠️ Status: Switch not assigned yet")
        self.setup_status_label.setStyleSheet("font-weight: bold; color: #FFA500; padding: 5px;")
        self.setup_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        initial_setup_layout.addWidget(self.setup_status_label, 4, 0, 1, 2)

        top_hbox.addWidget(initial_setup_group, 42)  # Stretch factor ~45%
        # --- Right Side: Switch Preview (2/3 width) ---
        # Create a wrapper to control the size of the preview label
        preview_wrapper = QWidget()
        preview_layout = QHBoxLayout(preview_wrapper)
        preview_layout.setContentsMargins(0, 0, 0, 0)

        self.switch_preview_label = ScalableLabel()
        self.switch_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_switch_preview_image()

        # Add stretch on both sides to make the label smaller than its container
        # 15% stretch on left, 70% for label, 15% stretch on right
        preview_layout.addStretch(15)
        preview_layout.addWidget(self.switch_preview_label, 70)
        preview_layout.addStretch(15)

        top_hbox.addWidget(preview_wrapper, 50) # Stretch factor ~62%

        main_layout.addLayout(top_hbox)

        # --- Action Buttons (now inside Initial Setup Group) ---
        button_hbox = QHBoxLayout()
        button_hbox.addStretch() # Push buttons to the right

        self.import_button = QPushButton('Import JSON Config')
        self.import_button.setObjectName("LoadButton")
        self.import_button.setToolTip("Load all settings from a previously exported JSON configuration file.")
        self.import_button.clicked.connect(self._import_config_from_json)

        self.load_button = QPushButton('Assign Switch')
        self.load_button.setObjectName("LoadButton")
        self.load_button.setToolTip("⚡ START HERE! Assign the selected switch model and prepare the tool for port assignment.\n\nThis is the first required step before you can configure ports.")
        self.load_button.clicked.connect(self.load_switch_and_prepare)

        self.reset_button = QPushButton('Reset & Start Over')
        self.reset_button.setObjectName("ResetButton")
        self.reset_button.setToolTip("Clear all inputs and reset the application to its initial state.")
        self.reset_button.clicked.connect(self._reset_and_restart)
        self.reset_button.setEnabled(False)

        button_hbox.addWidget(self.import_button)
        button_hbox.addWidget(self.load_button)
        button_hbox.addWidget(self.reset_button)
        button_hbox.addStretch() # Push buttons to the left
        
        # Add the button layout to the initial setup group
        initial_setup_layout.addLayout(button_hbox, 5, 0, 1, 2) # Row 5, span 2 columns

        # --- Optional Switch Config Values Group ---
        config_group_widget = QGroupBox("Optional Cluster Config Values")
        config_layout = QGridLayout(config_group_widget)

        # Column 1
        customer_label = QLabel('Customer Name:')
        customer_label.setToolTip("The customer name for this design.")
        config_layout.addWidget(customer_label, 0, 0)
        self.customer_name_entry = QLineEdit('Monster CSP')
        self.customer_name_entry.setToolTip(customer_label.toolTip())
        self.customer_name_entry.textChanged.connect(self._sync_customer_name_to_legacy)
        self.customer_name_entry.textChanged.connect(lambda: self._update_output_paths(self.cluster_name_entry.text()))
        config_layout.addWidget(self.customer_name_entry, 0, 1)

        site_label = QLabel('Site Name:')
        site_label.setToolTip("The site name for this design (e.g., datacenter location, building name).")
        config_layout.addWidget(site_label, 1, 0)
        self.site_name_entry = QLineEdit('500MW-1')
        self.site_name_entry.setToolTip(site_label.toolTip())
        self.site_name_entry.textChanged.connect(lambda: self._update_output_paths(self.cluster_name_entry.text()))
        self.site_name_entry.textChanged.connect(self._update_dynamic_labels)
        config_layout.addWidget(self.site_name_entry, 1, 1)

        vendor_label = QLabel('Switch OS:')
        vendor_label.setToolTip("Select the Switch Operating System (OS).\nThis affects the generated configuration script and available features.")
        config_layout.addWidget(vendor_label, 2, 0)
        self.vendor_combo = QComboBox()
        self.vendor_combo.setToolTip("Select the Switch Operating System (OS).\nThis affects the generated configuration script and available features.")
        self.vendor_combo.currentTextChanged.connect(self._on_vendor_changed)
        config_layout.addWidget(self.vendor_combo, 2, 1)

        route_label = QLabel('Mgmt Default Route:')
        route_label.setToolTip("The default gateway IP for the management network.\nThis is required for the switch configuration script.")
        config_layout.addWidget(route_label, 3, 0)
        self.net_def_route_entry = QLineEdit('1.1.1.1')
        self.net_def_route_entry.setValidator(self.ipv4_validator)
        self.net_def_route_entry.setToolTip("The default gateway IP for the management network.\nThis is required for the switch configuration script.")
        self.net_def_route_entry.textChanged.connect(self._update_mgmt_ips_from_gateway)
        # Connect signal to update Rack 1 in real-time
        self.net_def_route_entry.textChanged.connect(
            lambda: self._sync_main_config_to_rack1('mgmt_default_route', self.net_def_route_entry.text())
        )
        config_layout.addWidget(self.net_def_route_entry, 3, 1)

        cidr_label = QLabel('Network CIDR:')
        cidr_label.setToolTip("The subnet mask for the management network (e.g., 24 for 255.255.255.0).")
        config_layout.addWidget(cidr_label, 4, 0)
        self.net_cidr_combo = QComboBox()
        self.net_cidr_combo.addItems([str(i) for i in range(16, 30)])
        self.net_cidr_combo.setCurrentText('24')
        self.net_cidr_combo.setToolTip("The subnet mask for the management network (e.g., 24 for 255.255.255.0).")
        config_layout.addWidget(self.net_cidr_combo, 4, 1)

        self.switch_a_mgmt_ip_label = QLabel('FabricA Mgmt IP:')
        self.switch_a_mgmt_ip_label.setToolTip("The management IP for the first switch (Fabric A).\nThis is often auto-populated from the Mgmt Default Route.")
        config_layout.addWidget(self.switch_a_mgmt_ip_label, 5, 0)
        self.switch_a_mgmt_ip_entry = QLineEdit('1.1.1.10')
        self.switch_a_mgmt_ip_entry.setToolTip("The management IP for the first switch (Fabric A).\nThis is often auto-populated from the Mgmt Default Route.")
        self.switch_a_mgmt_ip_entry.setValidator(self.ipv4_validator)
        self.switch_a_mgmt_ip_entry.textChanged.connect(self._update_fabric_b_ip_from_a)
        # Connect signal to update Rack 1 in real-time
        self.switch_a_mgmt_ip_entry.textChanged.connect(
            lambda: self._sync_main_config_to_rack1('mgmt_ip_a', self.switch_a_mgmt_ip_entry.text())
        )
        config_layout.addWidget(self.switch_a_mgmt_ip_entry, 5, 1)

        # Column 2
        cluster_label = QLabel('Cluster name:')
        cluster_label.setToolTip("A name for the VAST cluster, used in switch configuration (e.g., for MLAG VIP).")
        config_layout.addWidget(cluster_label, 0, 2)
        self.cluster_name_entry = QLineEdit('Quota-Destroyer-001')
        self.cluster_name_entry.setToolTip("A name for the VAST cluster, used in switch configuration (e.g., for MLAG VIP).")
        self.cluster_name_entry.setValidator(self.hostname_validator)
        self.cluster_name_entry.textChanged.connect(self._update_dynamic_labels)
        # Connect signal to update Rack 1 in real-time
        self.cluster_name_entry.textChanged.connect(
            lambda: self._sync_main_config_to_rack1('cluster_name', self.cluster_name_entry.text())
        )
        self.cluster_name_entry.textChanged.connect(self._update_output_paths)
        config_layout.addWidget(self.cluster_name_entry, 0, 3)

        ntp_label = QLabel('NTP Server IP:')
        ntp_label.setToolTip("The IP address of an NTP server for time synchronization.")
        config_layout.addWidget(ntp_label, 1, 2)
        self.ntp_server_entry = QLineEdit('2.2.2.2')
        self.ntp_server_entry.setToolTip("The IP address of an NTP server for time synchronization.")
        self.ntp_server_entry.setValidator(self.ipv4_validator)
        config_layout.addWidget(self.ntp_server_entry, 1, 3)

        ls_label = QLabel('Leafs Or Spines:')
        ls_label.setToolTip("The role of these switches in the network topology (leaf or spine).")
        config_layout.addWidget(ls_label, 2, 2)
        self.leaf_spine_combo = QComboBox()
        self.leaf_spine_combo.addItems(['leaf', 'spine'])
        self.leaf_spine_combo.currentTextChanged.connect(self._update_dynamic_labels)
        self.leaf_spine_combo.currentTextChanged.connect(self._on_leaf_spine_changed)
        self.leaf_spine_combo.setToolTip("The role of these switches in the network topology (leaf or spine).")
        config_layout.addWidget(self.leaf_spine_combo, 2, 3)

        self.switch_b_mgmt_ip_label = QLabel('FabricB Mgmt IP:')
        self.switch_b_mgmt_ip_label.setToolTip("The management IP for the second switch (Fabric B).\nThis is often auto-incremented from the Fabric A IP.")
        config_layout.addWidget(self.switch_b_mgmt_ip_label, 3, 2)
        self.switch_b_mgmt_ip_entry = QLineEdit('1.1.1.11')
        self.switch_b_mgmt_ip_entry.setToolTip("The management IP for the second switch (Fabric B).\nThis is often auto-incremented from the Fabric A IP.")
        self.switch_b_mgmt_ip_entry.setValidator(self.ipv4_validator)
        config_layout.addWidget(self.switch_b_mgmt_ip_entry, 3, 3)
        # Connect signal to update Rack 1 in real-time
        self.switch_b_mgmt_ip_entry.textChanged.connect(
            lambda: self._sync_main_config_to_rack1('mgmt_ip_b', self.switch_b_mgmt_ip_entry.text())
        )

        # Advanced cluster setup fields integrated into Optional Cluster Config
        data_vlan_label = QLabel('Data Vlan:')
        data_vlan_label.setToolTip("The VLAN ID for the primary VAST data network.\nDefaults to 69.")
        config_layout.addWidget(data_vlan_label, 5, 2)
        self.data_vlan_entry = QLineEdit('69')
        self.data_vlan_entry.setToolTip(data_vlan_label.toolTip())
        self.data_vlan_entry.setValidator(self.vlan_id_validator)
        self.data_vlan_entry.setFixedWidth(40)  # 4 characters wide
        config_layout.addWidget(self.data_vlan_entry, 5, 3)

        self.use_2nd_nic_checkbox = QCheckBox('Use 2nd Nic?')
        self.use_2nd_nic_checkbox.setToolTip("Specify if the nodes will use a second network interface card.")
        self.use_2nd_nic_checkbox.stateChanged.connect(self._on_2nd_nic_changed)
        config_layout.addWidget(self.use_2nd_nic_checkbox, 5, 4, 1, 2)

        # Unified Networking checkbox - initially hidden
        self.use_converged_networking_checkbox = QCheckBox('Use Converged Networking?')
        self.use_converged_networking_checkbox.setToolTip("Enable unified networking configuration.")
        self.use_converged_networking_checkbox.setVisible(False)  # Initially hidden
        self.use_converged_networking_checkbox.stateChanged.connect(self._on_unified_networking_changed)
        config_layout.addWidget(self.use_converged_networking_checkbox, 6, 4, 1, 2)

        # Column 3
        uplink_speed_label = QLabel('Uplink Speed:')
        uplink_speed_label.setToolTip("The speed of the external-facing uplink ports (MLAG/BGP).\nIf left blank, it defaults to the switch's native port speed.")
        config_layout.addWidget(uplink_speed_label, 0, 4)
        self.uplink_speed_combo = QComboBox()
        self.uplink_speed_combo.addItems(['', '25G', '40G', '50G', '100G', '200G', '400G', '800G'])
        self.uplink_speed_combo.setCurrentIndex(0)
        self.uplink_speed_combo.setToolTip("The speed of the external-facing uplink ports (MLAG/BGP).\nIf left blank, it defaults to the switch's native port speed.")
        self.uplink_speed_combo.currentIndexChanged.connect(self._update_uplink_suggestions)
        config_layout.addWidget(self.uplink_speed_combo, 0, 5)

        # Customer Vlans
        cust_vlan_label = QLabel('Customer Vlans:')
        cust_vlan_label.setToolTip("A comma-separated list of additional VLANs to be trunked on external ports.")
        config_layout.addWidget(cust_vlan_label, 1, 4)
        self.customer_vlans_entry = QLineEdit()
        self.customer_vlans_entry.setToolTip("A comma-separated list of additional VLANs to be trunked on external ports.")
        self.customer_vlans_entry.setValidator(self.vlan_list_validator)
        config_layout.addWidget(self.customer_vlans_entry, 1, 5)

        # BGP ASNs
        bgp_asn_label = QLabel('BGP ASNs:')
        bgp_asn_label.setToolTip("Comma-separated list of BGP Autonomous System Numbers.")
        config_layout.addWidget(bgp_asn_label, 2, 4)
        self.bgp_asn_entry = QLineEdit()
        self.bgp_asn_entry.setToolTip("Comma-separated list of BGP Autonomous System Numbers.")
        self.bgp_asn_entry.setValidator(self.vlan_list_validator)
        self.bgp_asn_entry.textChanged.connect(self._on_bgp_asn_changed)
        config_layout.addWidget(self.bgp_asn_entry, 2, 5)

        bw_goal_label = QLabel('Max BW Required\nPer Cell:')
        bw_goal_label.setToolTip("Set a bandwidth target for the summary audit checks.\nThis helps validate if the design meets performance requirements.")
        config_layout.addWidget(bw_goal_label, 4, 2)
        self.peak_bw_goal_entry = QLineEdit()
        self.peak_bw_goal_entry.setValidator(self.peak_bw_validator)
        self.peak_bw_goal_entry.setToolTip("Set a bandwidth target for the summary audit checks.\nThis helps validate if the design meets performance requirements.")
        self.peak_bw_goal_entry.textChanged.connect(self._calculate_and_display_bandwidth)
        self.peak_bw_goal_entry.textChanged.connect(self._update_uplink_suggestions)
        config_layout.addWidget(self.peak_bw_goal_entry, 4, 3)
        self.peak_bw_units_combo = QComboBox()
        self.peak_bw_units_combo.addItems(['GB/s', 'GiB/s'])
        self.peak_bw_units_combo.setToolTip("Select the units for the bandwidth goal.\nGB = Gigabyte (10^9 bytes)\nGiB = Gibibyte (2^30 bytes)")
        self.peak_bw_units_combo.setFixedWidth(80)  # Reduced width
        self.peak_bw_units_combo.currentIndexChanged.connect(self._calculate_and_display_bandwidth)
        self.peak_bw_units_combo.currentIndexChanged.connect(self._update_uplink_suggestions)
        config_layout.addWidget(self.peak_bw_units_combo, 4, 4)

        main_layout.addWidget(config_group_widget)

        # --- Fabric Design & Overlay Options ---
        fabric_group_widget = QGroupBox("Fabric Design")
        fabric_layout = QVBoxLayout(fabric_group_widget)
        fabric_layout.setSpacing(6)

        fabric_intro = QLabel("Select the network fabric topology. Additional overlay options are available when using a leaf + spine fabric.")
        fabric_intro.setWordWrap(True)
        fabric_layout.addWidget(fabric_intro)

        self.fabric_single_radio = QRadioButton("Single MLAG leaf pair (direct customer handoff)")
        self.fabric_single_radio.setStyleSheet("color: white;")
        self.fabric_single_radio.setToolTip("Select for small footprints where storage nodes connect to a single MLAG-capable leaf pair with no spine layer.")
        self.fabric_spine_radio = QRadioButton("Leaf + spine fabric (two-tier)")
        self.fabric_spine_radio.setStyleSheet("color: white;")
        self.fabric_spine_radio.setToolTip("Select for scalable fabrics where multiple leaf racks uplink into a dedicated spine layer.")
        self.fabric_single_radio.setChecked(True)
        self.fabric_single_radio.toggled.connect(self._on_fabric_topology_changed)
        self.fabric_spine_radio.toggled.connect(self._on_fabric_topology_changed)
        fabric_layout.addWidget(self.fabric_single_radio)
        single_desc = QLabel("Ideal for edge or single-rack deployments. Simplifies configuration by keeping all host and gateway connectivity on one redundant leaf pair.")
        single_desc.setWordWrap(True)
        single_desc.setStyleSheet("color: #d0d8ff;")
        single_desc.setContentsMargins(24, 2, 0, 10)
        fabric_layout.addWidget(single_desc)
        fabric_layout.addWidget(self.fabric_spine_radio)
        spine_desc = QLabel("Best for multi-rack or growth-focused designs. Adds a spine tier to provide predictable east-west bandwidth and scalable fabric capacity.")
        spine_desc.setWordWrap(True)
        spine_desc.setStyleSheet("color: #d0d8ff;")
        spine_desc.setContentsMargins(24, 2, 0, 10)
        fabric_layout.addWidget(spine_desc)

        self.fabric_overlay_checkbox = QCheckBox("Use VXLAN/EVPN overlay (stretched VLANs via BGP EVPN)")
        self.fabric_overlay_checkbox.setToolTip("Enable when the fabric requires an EVPN/VXLAN overlay for multi-rack or routed leaf+spine designs.")
        self.fabric_overlay_checkbox.setEnabled(False)
        self.fabric_overlay_checkbox.toggled.connect(self._on_fabric_overlay_toggled)
        fabric_layout.addWidget(self.fabric_overlay_checkbox)
        overlay_desc = QLabel("Workloads that need or will need more than 2 Spine switches.")
        overlay_desc.setWordWrap(True)
        overlay_desc.setStyleSheet("color: #d0d8ff;")
        overlay_desc.setContentsMargins(24, 2, 0, 10)
        fabric_layout.addWidget(overlay_desc)

        pfc_tooltip = "Enable or disable Priority Flow Control (PFC) configuration.\nThis is required for Dual NIC configurations."
        self.pfc_checkbox = QCheckBox()
        pfc_label = QLabel('PFC:')
        pfc_label.setToolTip(pfc_tooltip)
        self.pfc_checkbox.setToolTip(pfc_tooltip)
        self.pfc_checkbox.clicked.connect(self._on_pfc_clicked)
        # PFC checkbox removed from visible layout (but widget and functionality remain)

        # VXLAN checkbox creation
        self.vxlan_checkbox = QCheckBox()
        self.vxlan_checkbox.setToolTip("Enable or disable VXLAN configuration in the output script.")
        self.vxlan_checkbox.clicked.connect(self._on_vxlan_clicked)
        # VXLAN checkbox removed from visible layout (but widget and functionality remain)

        main_layout.addWidget(fabric_group_widget)

        # Excuse label
        main_layout.addStretch(1)
        self.excuse_label = QLabel()
        self.excuse_label.setWordWrap(True)
        self.excuse_label.setStyleSheet("font-style: italic; color: white; background: transparent; padding: 5px;")
        self._update_excuse_label()
        main_layout.addWidget(self.excuse_label)

        self._update_vendor_options()
        self._on_vendor_changed()
        self._update_hostname_labels()
        self._update_vxlan_checkbox_state()

        # Final assembly
        scroll_area.setWidget(content_widget)
        container_layout.addWidget(scroll_area)

        # Arrow indicator for scrolling, placed below the scroll area
        self.setup_scroll_arrow = QLabel("▼")
        self.setup_scroll_arrow.setStyleSheet("color: white; font-size: 24px; background-color: transparent;")
        self.setup_scroll_arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setup_scroll_arrow.setToolTip("More content below")
        container_layout.addWidget(self.setup_scroll_arrow)

        scroll_bar = scroll_area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: self._update_scroll_arrows_visibility(scroll_area, self.setup_scroll_arrow_up, self.setup_scroll_arrow))
        scroll_bar.valueChanged.connect(lambda: self._update_scroll_arrows_visibility(scroll_area, self.setup_scroll_arrow_up, self.setup_scroll_arrow))

        return container_widget

    def _on_2nd_nic_changed(self, state):
        """Handle changes to the 'Use 2nd Nic?' checkbox."""
        if self.use_2nd_nic_checkbox.isChecked():
            self.pfc_checkbox.setChecked(True)
            # Show the unified networking checkbox
            self.use_converged_networking_checkbox.setVisible(True)
        else:
            # Hide the unified networking checkbox
            self.use_converged_networking_checkbox.setVisible(False)
            # Clear NB when 2nd NIC is disabled
            if hasattr(self, 'uplink_entries') and 'NB' in self.uplink_entries:
                self.uplink_entries['NB']['ppg'].clear()
        
        # Update NB configuration (will lock/unlock as appropriate)
        self._populate_cn_eb_nb_from_cnodes()

    def _on_unified_networking_changed(self, state):
        """Handle changes to the 'Use Unified Networking?' checkbox."""
        if self.use_2nd_nic_checkbox.isChecked() and self.use_converged_networking_checkbox.isChecked():
            # Auto-populate NB port count with CNode count as a starting point
            self._populate_cn_eb_nb_from_cnodes()
        else:
            # Clear NB when unified networking is disabled
            if hasattr(self, 'uplink_entries') and 'NB' in self.uplink_entries:
                self.uplink_entries['NB']['ppg'].clear()

    def _on_leaf_spine_changed(self, text):
        """Handle changes to the Leaf/Spine selection."""
        if not hasattr(self, 'uplink_entries'):
            return  # Uplink entries not initialized yet
            
        is_spine = text == 'spine'
        
        # Handle node type port mapping preservation
        if is_spine:
            # Switching to spine - preserve node type mappings
            self._preserve_node_mappings()
            # Node Types tab now stays visible in all modes
        else:
            # Switching to leaf - restore node type mappings
            self._restore_node_mappings()
        
        # Update uplink entry visibility and state
        self._update_uplink_entries_for_switch_type(is_spine)
        
        # Update IPL/ISL mutual exclusion logic
        self._update_ipl_isl_exclusion()

    def _preserve_node_mappings(self):
        """Preserve node type port mappings when switching to spine."""
        if not hasattr(self, 'node_entries'):
            return
            
        # Preserve the current port map (filter out uplink ports, keep only node ports)
        self.preserved_node_port_map = [
            (port_id, port_name) for port_id, port_name in self.port_map 
            if get_port_base_type(port_name) in self.node_types
        ]
        
        # Preserve node entry values
        self.preserved_node_entries = {}
        for node_type, entry in self.node_entries.items():
            self.preserved_node_entries[node_type] = {
                'count': entry['cnt'].text(),
                'split': entry['split_cb'].isChecked(),
                'factor': entry['fac'].currentText(),
                'reserved': entry['rsv'].text(),
                'manual_ports': entry['st'].text(),
                'locked': entry['lock_cb'].isChecked()
            }
        
        # Remove node type ports from the current port map (keep only uplink ports)
        self.port_map = [
            (port_id, port_name) for port_id, port_name in self.port_map 
            if get_port_base_type(port_name) not in self.node_types
        ]

    def _restore_node_mappings(self):
        """Restore node type port mappings when switching back to leaf."""
        if not hasattr(self, 'node_entries') or not self.preserved_node_entries:
            return
            
        # Restore node entry values
        for node_type, entry in self.node_entries.items():
            if node_type in self.preserved_node_entries:
                preserved = self.preserved_node_entries[node_type]
                entry['cnt'].setText(preserved['count'])
                entry['split_cb'].setChecked(preserved['split'])
                entry['fac'].setCurrentText(preserved['factor'])
                entry['rsv'].setText(preserved['reserved'])
                entry['st'].setText(preserved['manual_ports'])
                entry['lock_cb'].setChecked(preserved['locked'])
        
        # Restore node type ports to the port map
        self.port_map.extend(self.preserved_node_port_map)
        
        # Clear preserved data
        self.preserved_node_port_map = []
        self.preserved_node_entries = {}

    def _update_uplink_entries_for_switch_type(self, is_spine):
        """Update uplink entries based on switch type (leaf vs spine)."""
        if not hasattr(self, 'uplink_entries'):
            return
            
        # For spine switches, disable IPL ports
        if 'IPL' in self.uplink_entries:
            ipl_entry = self.uplink_entries['IPL']
            if is_spine:
                # Disable IPL for spine switches
                for widget_name in ['ppg', 'st', 'rsv']:
                    if widget_name in ipl_entry:
                        ipl_entry[widget_name].setEnabled(False)
                        ipl_entry[widget_name].setStyleSheet("QLineEdit:disabled { background-color: #555555; color: #AAAAAA; }")
                if 'lock_cb' in ipl_entry:
                    ipl_entry['lock_cb'].setEnabled(False)
                    ipl_entry['lock_cb'].setStyleSheet("QCheckBox:disabled { color: #AAAAAA; }")
                # Clear IPL values for spine
                ipl_entry['ppg'].setText('0')
                ipl_entry['st'].clear()
                ipl_entry['rsv'].setText('0')
            else:
                # Enable IPL for leaf switches
                for widget_name in ['ppg', 'st', 'rsv']:
                    if widget_name in ipl_entry:
                        ipl_entry[widget_name].setEnabled(True)
                        ipl_entry[widget_name].setStyleSheet("")  # Reset to default
                if 'lock_cb' in ipl_entry:
                    ipl_entry['lock_cb'].setEnabled(True)
                    ipl_entry['lock_cb'].setStyleSheet("")  # Reset to default

    def _update_ipl_isl_exclusion(self):
        """Update IPL/ISL logic for leaf switches - BOTH CAN NOW BE CONFIGURED."""
        # IPL and ISL can now coexist - no mutual exclusion
        if not hasattr(self, 'uplink_entries') or self.leaf_spine_combo.currentText() != 'leaf':
            return
            
        # Always enable both IPL and ISL entries if they exist
        if 'IPL' in self.uplink_entries:
            self._enable_uplink_entry(self.uplink_entries['IPL'])
        if 'ISL' in self.uplink_entries:
            self._enable_uplink_entry(self.uplink_entries['ISL'])

    def _disable_uplink_entry(self, entry):
        """Disable an uplink entry and grey it out."""
        for widget_name in ['ppg', 'st', 'rsv', 'gcnt']:
            if widget_name in entry:
                entry[widget_name].setEnabled(False)
                entry[widget_name].setStyleSheet("QLineEdit:disabled { background-color: #555555; color: #AAAAAA; }")
        if 'lock_cb' in entry:
            entry['lock_cb'].setEnabled(False)
            entry['lock_cb'].setStyleSheet("QCheckBox:disabled { color: #AAAAAA; }")
        if 'split_cb' in entry:
            entry['split_cb'].setEnabled(False)
            entry['split_cb'].setStyleSheet("QCheckBox:disabled { color: #AAAAAA; }")

    def _enable_uplink_entry(self, entry):
        """Enable an uplink entry and reset styling."""
        # Find which uplink type this entry belongs to
        uplink_type = None
        for ut, ent in self.uplink_entries.items():
            if ent == entry:
                uplink_type = ut
                break
        
        for widget_name in ['ppg', 'st', 'rsv', 'gcnt']:
            if widget_name in entry:
                # Never re-enable gcnt for IPL and NB (they should always be disabled)
                if widget_name == 'gcnt' and uplink_type in ['IPL', 'NB']:
                    continue
                entry[widget_name].setEnabled(True)
                entry[widget_name].setStyleSheet("")  # Reset to default
        if 'lock_cb' in entry:
            entry['lock_cb'].setEnabled(True)
            entry['lock_cb'].setStyleSheet("")  # Reset to default
        if 'split_cb' in entry:
            entry['split_cb'].setEnabled(True)
            entry['split_cb'].setStyleSheet("")  # Reset to default

    def _on_uplink_count_changed(self):
        """Handle changes to IPL or ISL port counts to trigger mutual exclusion logic."""
        # Only apply mutual exclusion logic for leaf switches
        if self.leaf_spine_combo.currentText() == 'leaf':
            self._update_ipl_isl_exclusion()

    def _update_uplink_suggestions(self):
        """Calculate and display suggested ports per group for ISL and MLAG/BGP uplinks based on bandwidth requirements."""
        if not hasattr(self, 'uplink_suggestion_labels') or not self.uplink_suggestion_labels:
            return
            
        # Get the peak BW from either the main setup or the currently selected rack in multi-rack mode
        if self.multi_rack_checkbox.isChecked() and hasattr(self, 'current_rack_name') and self.current_rack_name:
            # In multi-rack mode, get the BW goal from the currently selected rack
            rack_data = self.multi_rack_config.get(self.current_rack_name, {})
            peak_bw = safe_int(rack_data.get('peak_bw_goal', ''), 0)
            peak_bw_units = rack_data.get('peak_bw_units', 'GB/s')
        else:
            # In single-rack mode, get from the main setup tab
            peak_bw = safe_int(self.peak_bw_goal_entry.text(), 0)
            peak_bw_units = self.peak_bw_units_combo.currentText()
        
        # Convert to Gb/s for consistency (convert GB to Gb)
        if peak_bw_units == 'GiB/s':
            # 1 GiB/s = 2^30 bytes/s = (2^30 * 8) bits/s = 8.589934592 Gb/s
            peak_bw_gbps = peak_bw * 8.589934592
        else:
            # GB/s: 1 GB = 8 Gb, so 1 GB/s = 8 Gb/s
            peak_bw_gbps = peak_bw * 8
        
        # Get the native speed and uplink speed from the switch
        native_speed_str = self.layout_config.get('NATIVE_SPEED', '100G')
        native_speed_gbps = safe_int(native_speed_str.replace('G', ''), 100)
        
        uplink_speed_text = self.uplink_speed_combo.currentText()
        uplink_speed_gbps = safe_int(uplink_speed_text.replace('Gbps', '').replace('G', ''), native_speed_gbps)
        
        # Check for ISL and MLAG/BGP (stored as 'EXT' in suggestion labels)
        for display_type in ['ISL', 'EXT']:
            # Check both Node Types tab and Uplinks tab labels
            node_label_key = display_type + '_node_tab'
            uplink_label_key = display_type + '_uplink_tab'
            
            # Collect all labels that exist for this uplink type
            labels_to_update = []
            if node_label_key in self.uplink_suggestion_labels:
                labels_to_update.append(self.uplink_suggestion_labels[node_label_key])
            if uplink_label_key in self.uplink_suggestion_labels:
                labels_to_update.append(self.uplink_suggestion_labels[uplink_label_key])
            
            if not labels_to_update:
                continue
            
            # Convert display_type to the internal type for looking up entries
            # 'EXT' is displayed but stored as 'MLAG/BGP' in uplink_entries
            lookup_type = 'MLAG/BGP' if display_type == 'EXT' else display_type
            
            # In multi-rack mode, read from rack's config, otherwise from global uplink_entries
            if self.multi_rack_checkbox.isChecked() and hasattr(self, 'current_rack_name') and self.current_rack_name:
                rack_data = self.multi_rack_config.get(self.current_rack_name, {})
                uplinks_data = rack_data.get('uplinks', {})
                uplink_config = uplinks_data.get(lookup_type, {})
                groups = safe_int(uplink_config.get('groups'), 0)
                ppg = safe_int(uplink_config.get('ports_per_group'), 0)
            else:
                ent = self.uplink_entries.get(lookup_type, {})
                if 'gcnt' not in ent or 'ppg' not in ent:
                    continue
                groups = safe_int(ent['gcnt'].text(), 0)
                ppg = safe_int(ent['ppg'].text(), 0)
            
            # Generate the suggestion text once
            if groups == 0 or peak_bw <= 0:
                suggestion_text = ''
                suggestion_style = "QLabel { padding-left: 10px; min-width: 200px; }"
            else:
                # Determine the speed to use for calculation
                speed_for_calc = native_speed_gbps if display_type == 'ISL' else uplink_speed_gbps

                # Account for HA: size each group assuming only half the groups remain
                effective_groups = max(1, groups // 2) if groups > 1 else 1

                # Calculate required bandwidth per group
                required_bw_per_group_gbps = peak_bw_gbps / effective_groups
                
                # Calculate suggested ports per group
                # Each port can provide the calculated speed
                if required_bw_per_group_gbps > 0 and speed_for_calc > 0:
                    suggested_ppg = math.ceil(required_bw_per_group_gbps / speed_for_calc)
                else:
                    suggested_ppg = 0
                
                # Format the suggestion
                if suggested_ppg > 0:
                    current_ppg = ppg if ppg > 0 else suggested_ppg
                    
                    if current_ppg >= suggested_ppg:
                        suggestion_text = f'✓ Suggested: {suggested_ppg} ports/group (Current: {current_ppg})'
                        suggestion_style = "QLabel { color: green; padding-left: 10px; min-width: 250px; font-weight: bold; font-size: 9pt; }"
                    else:
                        suggestion_text = f'⚠ Suggested: {suggested_ppg} ports/group (Current: {current_ppg})'
                        suggestion_style = "QLabel { color: orange; padding-left: 10px; min-width: 250px; font-weight: bold; font-size: 9pt; }"
                else:
                    suggestion_text = ''
                    suggestion_style = "QLabel { padding-left: 10px; min-width: 200px; font-size: 9pt; }"
            
            # Update all labels for this uplink type
            for suggestion_label in labels_to_update:
                suggestion_label.setText(suggestion_text)
                suggestion_label.setStyleSheet(suggestion_style)

    def _populate_cn_eb_nb_from_cnodes(self):
        """Auto-populates NB port count based on CN + EB node counts when 2nd NIC is enabled."""
        if not hasattr(self, 'uplink_entries') or 'NB' not in self.uplink_entries:
            return
        if not hasattr(self, 'node_entries'):
            return
        
        # Get the CNode and EBox counts
        cnode_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0)
        ebox_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0)
        
        # Sum of CN and EB nodes (1 NB port per node)
        total_nb_ports = cnode_count + ebox_count
        
        # Check if both 2nd NIC and unified networking are enabled
        both_enabled = (hasattr(self, 'use_2nd_nic_checkbox') and self.use_2nd_nic_checkbox.isChecked() and
                       hasattr(self, 'use_converged_networking_checkbox') and self.use_converged_networking_checkbox.isChecked())
        
        
        if both_enabled and total_nb_ports > 0:
            # Set NB port count to match total CN + EB count
            self.uplink_entries['NB']['ppg'].setText(str(total_nb_ports))
            # Keep NB ports unlocked so they flow in priority order
            self.uplink_entries['NB']['lock_cb'].setChecked(False)
            self.uplink_entries['NB']['ppg'].setEnabled(True)
            self.uplink_entries['NB']['ppg'].setStyleSheet("")
            # Clear the manual assignment field to ensure auto-assignment is used
            self.uplink_entries['NB']['st'].clear()
        else:
            # Grey out the NB port configuration when conditions are not met
            self.uplink_entries['NB']['lock_cb'].setChecked(False)
            self.uplink_entries['NB']['ppg'].setEnabled(False)
            self.uplink_entries['NB']['ppg'].setStyleSheet("QLineEdit:disabled { background-color: #555555; color: #AAAAAA; }")
            # Clear the manual assignment when greying out
            self.uplink_entries['NB']['st'].clear()
            # Clear the port count when conditions are not met
            self.uplink_entries['NB']['ppg'].setText('0')
        
        # Update uplink suggestions after NB port changes
        self._update_uplink_suggestions()
    
    def _initialize_node_tab_uplinks(self):
        """Initialize the uplinks table in the Node Types tab to function identically to the Uplinks tab."""
        if hasattr(self, 'leaf_spine_combo') and hasattr(self, 'uplink_entries'):
            self._on_leaf_spine_changed(self.leaf_spine_combo.currentText())
        
        if hasattr(self, 'node_entries'):
            self._populate_cn_eb_nb_from_cnodes()
            self._update_uplink_suggestions()
        
        # Trigger live preview update to show assigned ports
        if self.config_started:
            QTimer.singleShot(0, self._do_live_preview)
    
    def _on_cnode_count_changed(self):
        """Updates NB port count when CNode count changes (if both 2nd NIC and unified networking are enabled)."""
        # Only auto-update if both 2nd NIC and unified networking are enabled
        if (hasattr(self, 'use_2nd_nic_checkbox') and self.use_2nd_nic_checkbox.isChecked() and
            hasattr(self, 'use_converged_networking_checkbox') and self.use_converged_networking_checkbox.isChecked()):
            self._populate_cn_eb_nb_from_cnodes()
    
    def _on_clone_to_multi_rack_go(self, mode: str = 'default'):
        """Handles cloning the current single-rack configuration to multi-rack when Go button is clicked.
        
        Args:
            mode: 'default' or 'advanced' - determines which UI widgets to read from
        """
        
        # Get the number of racks to create
        if mode == 'advanced':
            count = safe_int(self.cell_planning_advanced_clone_count_entry.text(), 1)
            base_rack_name = self.cell_planning_advanced_clone_rack_name_entry.text().strip()
            lors_type = self.cell_planning_advanced_clone_rack_type_combo.currentText()
        else:
            count = safe_int(self.clone_count_entry.text(), 1)
            base_rack_name = self.clone_rack_name_entry.text().strip()
            lors_type = self.clone_rack_type_combo.currentText()
        
        if count <= 0:
            count = 1
        
        if not base_rack_name:
            base_rack_name = "Rack"
        # Limit to 20 characters
        base_rack_name = base_rack_name[:20]
        
        # Check if we already have racks with this base name
        existing_names = list(self.multi_rack_config.keys())
        existing_base_names = [name.rsplit(' ', 1)[0] for name in existing_names]
        
        # Don't allow the same base name if racks with that name already exist
        if base_rack_name in existing_base_names:
            QMessageBox.warning(self, "Duplicate Name", 
                               f"A rack with the base name '{base_rack_name}' already exists. Please choose a different name.")
            return
        
        # Get the current configuration from setup tab
        peak_bw_goal = self.peak_bw_goal_entry.text()
        peak_bw_units = self.peak_bw_units_combo.currentText()
        
        # Collect current node and uplink data based on mode
        if mode == 'advanced':
            # Advanced mode: collect from advanced UI widgets
            nodes_data = {}
            # DN
            dn_count = safe_int(self.cell_planning_advanced_dn_count.text(), 0)
            if dn_count > 0:
                # Read starting node value from Cell Planning (default to 100 for DN)
                # Advanced mode may not have starting_node widgets yet, so use default
                dn_starting_node = 100  # Default for DN
                # Try to read from widget if it exists
                if hasattr(self, 'cell_planning_advanced_node_widgets') and 'DN' in self.cell_planning_advanced_node_widgets:
                    widget = self.cell_planning_advanced_node_widgets['DN'].get('starting_node')
                    if widget:
                        dn_starting_node = safe_int(widget.text(), 100)
                nodes_data['DN'] = {
                    'count': dn_count,
                    'split': self.cell_planning_advanced_dn_split_cb.isChecked(),
                    'factor': safe_int(self.cell_planning_advanced_dn_factor.currentText(), 2),
                    'reserved': 0,
                    'start_port': '',
                    'manual_ports': '',
                    'locked': False,
                    'starting_node': dn_starting_node
                }
            
            # Other node types
            for nt in ['CN', 'EB', 'IE', 'GN']:
                if nt in self.cell_planning_advanced_node_counts:
                    count_val = safe_int(self.cell_planning_advanced_node_counts[nt].text(), 0)
                    if count_val > 0:
                        split_cb = self.cell_planning_advanced_node_splits[nt]['split_cb']
                        factor_combo = self.cell_planning_advanced_node_splits[nt]['factor']
                        # Read starting node value from Cell Planning (default to 1)
                        nt_starting_node = 1  # Default
                        # Try to read from widget if it exists
                        if hasattr(self, 'cell_planning_advanced_node_widgets') and nt in self.cell_planning_advanced_node_widgets:
                            widget = self.cell_planning_advanced_node_widgets[nt].get('starting_node')
                            if widget:
                                nt_starting_node = safe_int(widget.text(), 1)
                        nodes_data[nt] = {
                            'count': count_val,
                            'split': split_cb.isChecked(),
                            'factor': safe_int(factor_combo.currentText(), 2),
                            'reserved': 0,
                            'start_port': '',
                            'manual_ports': '',
                            'locked': False,
                            'starting_node': nt_starting_node
                        }
            
            # Collect routing preferences
            node_routing = {}
            for nt in ['CN', 'EB', 'IE', 'GN']:
                if nt in self.cell_planning_advanced_routing_widgets:
                    nt_widgets = self.cell_planning_advanced_routing_widgets[nt]
                    if nt_widgets.get('left', QRadioButton()).isChecked():
                        node_routing[nt] = 'LEFT'
                    else:
                        node_routing[nt] = 'RIGHT'
            
            # Collect uplink data
            uplinks_data = {}
            for ut in ['IPL', 'ISL', 'EXT']:
                if ut in self.cell_planning_advanced_uplink_widgets:
                    groups_widget = self.cell_planning_advanced_uplink_widgets[ut]['groups']
                    ppg_widget = self.cell_planning_advanced_uplink_widgets[ut]['ppg']
                    groups = safe_int(groups_widget.text(), 0)
                    ppg = safe_int(ppg_widget.text(), 0)
                    # Map EXT to MLAG/BGP for consistency with default mode
                    uplink_key = 'MLAG/BGP' if ut == 'EXT' else ut
                    uplinks_data[uplink_key] = {
                        'groups': groups,
                        'ports_per_group': ppg,
                        'split': False,
                        'factor': 2,
                        'reserved': 0,
                        'start': '',
                        'manual_ports': '',
                        'locked': False
                    }
            
            # Store advanced config
            advanced_config = {
                'dbox_type': self.cell_planning_advanced_config['dbox_type'],
                'node_routing': node_routing,
                'uplinks': self.cell_planning_advanced_config['uplinks'].copy()
            }
        else:
            # Default mode: collect from default UI widgets
            nodes_data = {}
            for nt, ent in self.node_entries.items():
                is_locked = ent['lock_cb'].isChecked()
                manual_ports_str = ent['st'].text().strip() if is_locked else ''
                # Read starting node value from Cell Planning
                starting_node_val = safe_int(ent.get('starting_node', QLineEdit('1')).text(), 1)
                if nt == 'DN':
                    # DN defaults to 100
                    starting_node_val = safe_int(ent.get('starting_node', QLineEdit('100')).text(), 100)
                nodes_data[nt] = {
                    'count': safe_int(ent['cnt'].text()),
                    'split': ent['split_cb'].isChecked(),
                    'factor': safe_int(ent['fac'].currentText(), 2),
                    'reserved': safe_int(ent['rsv'].text()),
                    'start_port': manual_ports_str if is_locked else '',
                    'manual_ports': manual_ports_str if is_locked else '',
                    'locked': is_locked,
                    'starting_node': starting_node_val
                }
            
            uplinks_data = {}
            for ut, ent in self.uplink_entries.items():
                is_locked = ent['lock_cb'].isChecked()
                manual_ports_str = ent['st'].text().strip() if is_locked else ''
                uplinks_data[ut] = {
                    'groups': safe_int(ent.get('gcnt', QLineEdit('1')).text()),
                    'ports_per_group': safe_int(ent['ppg'].text()),
                    'split': ent['split_cb'].isChecked(),
                    'factor': safe_int(ent['fac'].currentText(), 2),
                    'reserved': safe_int(ent['rsv'].text()),
                    'start': manual_ports_str if is_locked else '',
                    'manual_ports': manual_ports_str if is_locked else '',
                    'locked': is_locked
                }
            advanced_config = None
        
        # Enable multi-rack mode
        self.multi_rack_checkbox.setChecked(True)
        
        # Find the highest existing rack number to start numbering from
        max_rack_num = 0
        if existing_names:
            for name in existing_names:
                # Extract number from names like "Leaf Rack 5"
                parts = name.rsplit(' ', 1)
                if len(parts) == 2 and parts[1].isdigit():
                    max_rack_num = max(max_rack_num, int(parts[1]))
        
        # Calculate starting management IPs based on setup tab values
        base_ip_a = self.switch_a_mgmt_ip_entry.text().strip()
        base_ip_b = self.switch_b_mgmt_ip_entry.text().strip()
        
        # Get base hostnames from setup tab
        base_hostname_a = self.ha_entry.text().strip()
        base_hostname_b = self.hb_entry.text().strip()
        
        # Parse and increment IPs for each new rack
        def increment_ip(ip_str, increment):
            """Increment an IP address by a given amount."""
            try:
                parts = ip_str.split('.')
                if len(parts) == 4:
                    # Increment the last octet
                    last_octet = int(parts[3]) + increment
                    return f"{parts[0]}.{parts[1]}.{parts[2]}.{last_octet}"
            except:
                pass
            return ip_str
        
        # Helper function to calculate next starting node numbers based on existing racks
        def calculate_next_starting_nodes(base_starting_nodes, rack_index):
            """Calculate starting node numbers for a rack based on previous racks' node counts."""
            next_starting = {}
            default_starting_numbers = {'DN': 100, 'CN': 1, 'EB': 1, 'IE': 1, 'GN': 1}
            
            for node_type in self.node_types:
                base_start = base_starting_nodes.get(node_type, default_starting_numbers.get(node_type, 1))
                
                # Calculate total node count from all previous racks with same base name
                total_previous_count = 0
                for existing_rack_name in sorted(self.multi_rack_config.keys()):
                    # Only count racks with the same base name
                    if existing_rack_name.startswith(base_rack_name.rsplit(' ', 1)[0] if ' ' in base_rack_name else base_rack_name):
                        existing_rack_data = self.multi_rack_config[existing_rack_name]
                        existing_node_data = existing_rack_data.get('nodes', {}).get(node_type, {})
                        total_previous_count += existing_node_data.get('count', 0)
                
                # Calculate starting node for this rack
                # For rack_index 0, use base_start. For rack_index > 0, add total_previous_count
                if rack_index == 0:
                    next_starting[node_type] = base_start
                else:
                    next_starting[node_type] = base_start + total_previous_count
                    
            return next_starting
        
        # Create the specified number of racks (APPEND, don't replace)
        racks_created = []
        
        # Extract base starting node values from nodes_data
        base_starting_nodes = {}
        for node_type in self.node_types:
            base_starting_nodes[node_type] = nodes_data.get(node_type, {}).get('starting_node', 
                {'DN': 100, 'CN': 1, 'EB': 1, 'IE': 1, 'GN': 1}.get(node_type, 1))
        
        for i in range(count):
            rack_num = max_rack_num + i + 1
            rack_name = f'{base_rack_name} {rack_num}'
            
            # Calculate starting node numbers for this rack
            next_starting_nodes = calculate_next_starting_nodes(base_starting_nodes, i)
            
            # Create a copy of nodes_data and update starting_node values
            rack_nodes_data = {}
            for node_type, node_info in nodes_data.items():
                rack_nodes_data[node_type] = node_info.copy()
                rack_nodes_data[node_type]['starting_node'] = next_starting_nodes.get(node_type, 
                    {'DN': 100, 'CN': 1, 'EB': 1, 'IE': 1, 'GN': 1}.get(node_type, 1))
            
            # Calculate management IPs for this rack
            # Each rack needs 2 IPs (A and B), so we increment by 2 per rack
            # Rack 1: base IP, base IP + 1
            # Rack 2: base IP + 2, base IP + 3
            # Rack 3: base IP + 4, base IP + 5
            offset = (rack_num - 1) * 2  # offset of 0 for first rack
            mgmt_ip_a = increment_ip(base_ip_a, offset) if base_ip_a else ''
            mgmt_ip_b = increment_ip(base_ip_b, offset) if base_ip_b else ''
            
            # Create hostnames with rack number prefix
            hostname_a = f'r{rack_num}-{base_hostname_a}' if base_hostname_a else f'r{rack_num}-sw-a'
            hostname_b = f'r{rack_num}-{base_hostname_b}' if base_hostname_b else f'r{rack_num}-sw-b'
            
            rack_config = {
                'hostname_a': hostname_a,
                'hostname_b': hostname_b,
                'switch_id': self.switch_id,
                'mgmt_ip_a': mgmt_ip_a,
                'mgmt_ip_b': mgmt_ip_b,
                'lors': lors_type,
                'peak_bw_goal': peak_bw_goal,
                'peak_bw_units': peak_bw_units,
                'nodes': rack_nodes_data,
                'uplinks': uplinks_data.copy(),
                'mapping_mode': mode  # NEW: Store mode identifier
            }
            
            # Store advanced config if in advanced mode
            if mode == 'advanced' and advanced_config:
                rack_config['advanced_config'] = advanced_config.copy()
            
            self.multi_rack_config[rack_name] = rack_config
            
            self.rack_list_widget.addItem(rack_name)
            self._create_rack_detail_widget(rack_name)
            self._calculate_and_store_rack_port_map(rack_name)  # Calculate port map for the rack
            racks_created.append(rack_name)
        
        # Select the first newly created rack
        if racks_created:
            for i in range(self.rack_list_widget.count()):
                if self.rack_list_widget.item(i).text() == racks_created[0]:
                    self.rack_list_widget.setCurrentRow(i)
                    break
        
        # Switch to multi-rack tab
        self.notebook.setCurrentIndex(self.multi_rack_tab_index)
        
        QMessageBox.information(self, "Racks Added", 
                               f"Added {count} {lors_type} rack(s) to the multi-rack design.")
    
    def _on_pfc_clicked(self):
        """Handle clicks on the PFC checkbox to prevent unchecking when required."""
        if self.use_2nd_nic_checkbox.isChecked() and not self.pfc_checkbox.isChecked():
            QMessageBox.information(self, "PFC Required", "This must be applied to the Northbound NICs in a Dual NIC system running Split networking.")
            self.pfc_checkbox.setChecked(True)

    def _on_vxlan_clicked(self):
        """Handle clicks on the VXLAN checkbox."""
        # VXLAN checkbox can be freely toggled
        # It will be automatically enabled if BGP ASNs are defined
        pass

    def _on_fabric_topology_changed(self):
        """Handle selection between single MLAG pair and leaf+spine fabric."""
        if not hasattr(self, 'fabric_single_radio'):
            return

        if self.fabric_single_radio.isChecked():
            self.fabric_topology = 'single_pair'
            # Disable and reset overlay option
            if hasattr(self, 'fabric_overlay_checkbox'):
                self.fabric_overlay_checkbox.setEnabled(False)
                if self.fabric_overlay_checkbox.isChecked():
                    self.fabric_overlay_checkbox.blockSignals(True)
                    self.fabric_overlay_checkbox.setChecked(False)
                    self.fabric_overlay_checkbox.blockSignals(False)
            self.use_vxlan_overlay = False
        else:
            self.fabric_topology = 'leaf_spine'
            if hasattr(self, 'fabric_overlay_checkbox'):
                self.fabric_overlay_checkbox.setEnabled(True)

        self._sync_main_config_to_rack1('fabric_topology', self.fabric_topology)
        self._update_vxlan_checkbox_state()

    def _on_fabric_overlay_toggled(self, checked: bool):
        """Handle VXLAN overlay enablement from the fabric design section."""
        self.use_vxlan_overlay = bool(checked)
        self._sync_main_config_to_rack1('use_vxlan_overlay', self.use_vxlan_overlay)
        if self.use_vxlan_overlay and not self._has_bgp_asns():
            self.statusBar().showMessage("VXLAN overlay requires at least one BGP ASN.", 4000)
        self._update_vxlan_checkbox_state()

    def _has_bgp_asns(self) -> bool:
        if not hasattr(self, 'bgp_asn_entry'):
            return False
        bgp_asn_raw = self.bgp_asn_entry.text().strip()
        cleaned_asns = re.sub(r',+', ',', bgp_asn_raw.replace(' ', ',')).strip(',')
        return bool(cleaned_asns)

    def _update_vxlan_checkbox_state(self):
        """Keep the hidden VXLAN checkbox in sync with fabric overlay + BGP ASN requirements."""
        if not hasattr(self, 'vxlan_checkbox'):
            return
        should_enable = self.use_vxlan_overlay and self._has_bgp_asns()
        self.vxlan_checkbox.blockSignals(True)
        self.vxlan_checkbox.setChecked(should_enable)
        self.vxlan_checkbox.blockSignals(False)
    
    def _on_bgp_asn_changed(self, text: str):
        """Handle changes to BGP ASN entry - automatically enable VXLAN if ASNs are defined."""
        cleaned_asns = re.sub(r',+', ',', text.strip().replace(' ', ',')).strip(',')
        has_bgp_asns = bool(cleaned_asns)
        if not has_bgp_asns and hasattr(self, 'fabric_overlay_checkbox') and self.use_vxlan_overlay:
            # Keep overlay checkbox visually enabled, but remind user that ASNs are required
            self.statusBar().showMessage("VXLAN overlay requires at least one BGP ASN.", 4000)
        self._update_vxlan_checkbox_state()

    def _show_timed_messagebox(self, title: str, text: str, icon=QMessageBox.Icon.Information, timeout: int = 2000):
        """Shows a QMessageBox that automatically closes after a timeout."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.setStandardButtons(QMessageBox.StandardButton.NoButton)
        QTimer.singleShot(timeout, msg_box.accept)
        msg_box.exec()

    def _ensure_status_dialog(self, title: str):
        """Ensure a single, reusable non-blocking status dialog exists for progress and logs."""
        if not hasattr(self, '_status_dialog') or self._status_dialog is None:
            dlg = QDialog(self)
            dlg.setWindowTitle(title)
            dlg.setMinimumSize(900, 520)
            layout = QVBoxLayout(dlg)
            title_label = QLabel(title)
            title_label.setWordWrap(True)
            log = QTextEdit()
            log.setReadOnly(True)
            log.setMinimumHeight(400)
            # Button row fixed at the bottom so it's always visible
            button_row = QHBoxLayout()
            ok_btn = QPushButton("OK")
            ok_btn.clicked.connect(dlg.close)
            button_row.addStretch(1)
            button_row.addWidget(ok_btn)
            layout.addWidget(title_label)
            layout.addWidget(log, 1)
            layout.addLayout(button_row)
            self._status_dialog = dlg
            self._status_log_widget = log
            self._status_title_label = title_label
        else:
            self._status_dialog.setWindowTitle(title)
            self._status_title_label.setText(title)
        self._status_dialog.show()
        self._status_dialog.raise_()
        self._status_dialog.activateWindow()

    def _status_append(self, text: str):
        if not hasattr(self, '_status_dialog') or self._status_dialog is None:
            self._ensure_status_dialog("Status")
        self._status_log_widget.append(text)

    def _status_close(self):
        if hasattr(self, '_status_dialog') and self._status_dialog is not None:
            self._status_dialog.close()

    def _switch_selected(self, text):
        for k, v in SWITCH_LAYOUTS.items():
            if v['NAME'] == text:
                self.switch_id, self.layout_config = k, v
                self._load_default_switch_image()
                self._update_vendor_options()
                self._update_switch_preview_image()
                
                # Update switch type labels in Node and Uplink tabs
                if hasattr(self, 'node_switch_label'):
                    self.node_switch_label.setText(f"Switch Model: {text}")
                if hasattr(self, 'uplink_switch_label'):
                    self.uplink_switch_label.setText(f"Switch Model: {text}")
                if hasattr(self, 'cell_planning_advanced_switch_label'):
                    self.cell_planning_advanced_switch_label.setText(f"Switch Model: {text}")
                
                # If switch is already assigned, reload the base image and update previews
                if self.config_started:
                    path = resource_path(self.layout_config['IMAGE'])
                    try:
                        self.base_image = Image.open(path).convert('RGBA')
                        # Force update both Node Types and Uplinks tabs regardless of which tab is currently visible
                        QTimer.singleShot(100, lambda: self._draw_preview(self.node_canvas_a, 'A', include_uplinks=True))
                        QTimer.singleShot(100, lambda: self._draw_preview(self.node_canvas_b, 'B', include_uplinks=True))
                    except FileNotFoundError:
                        QMessageBox.critical(self, 'Error', f'Base image "{path}" not found')
                break

    def _create_port_config_row(self, grid: QGridLayout, row: int, type_name: str, description: str, is_node_tab: bool):
        """Creates and places all widgets for a single port configuration row in the given grid. The description is used for tooltips."""
        entries_dict = self.node_entries if is_node_tab else self.uplink_entries
        update_scheduler = self._sched_both_node_updates if is_node_tab else self._sched_both_uplink_updates
        widgets = {}
        col = 0

        # Connect node/uplink changes to the Rack 1 sync
        sync_connection = lambda *_: self._sync_main_config_to_rack1(None, None)


        # Column 0: Type Name
        # *** CRITICAL: DO NOT CHANGE THIS LABEL MAPPING ***
        # Display 'EXT' instead of 'MLAG/BGP' in the UI
        # Internal storage uses 'MLAG/BGP', but UI must display 'EXT'
        display_name = 'EXT' if type_name == 'MLAG/BGP' else type_name
        type_label = QLabel(display_name)
        type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        type_label.setToolTip(description)
        grid.addWidget(type_label, row, col); col += 1

        # Column 1: Uplink Groups (Uplink tab only)
        if not is_node_tab:
            gcnt = QLineEdit()
            gcnt.setValidator(self.port_validator)
            gcnt.setToolTip("Number of uplink destinations being spines (ISLs) or customer switches (MLAG or BGP). Each uplink gets its ports defined in 'Ports/Group'")
            gcnt.setFixedWidth(40)
            grid.addWidget(gcnt, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
            widgets['gcnt'] = gcnt

        # Column 1/2: Node Count / Ports Per Group
        # Add tooltips to the column headers
        if row == 1: grid.itemAtPosition(0, col).widget().setToolTip("Node Tab: The number of logical nodes of this type.\n\nUplink Tab: The number of physical ports in EACH group.")

        count_widget = QLineEdit()
        count_widget.setValidator(self.port_validator)
        if is_node_tab:
            count_widget.setToolTip("The number of logical nodes of this type.")
        else:
            count_widget.setToolTip("The number of physical ports in EACH group.")

        count_widget.setFixedWidth(40)
        grid.addWidget(count_widget, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
        widgets['cnt' if is_node_tab else 'ppg'] = count_widget

        # Columns for Split, Factor, Reserved, Lock, Assigned Ports
        if row == 1: grid.itemAtPosition(0, col).widget().setToolTip("Check this if a single physical switch port will be split\n(using a breakout cable) to serve multiple logical connections.")
        split_cb = QCheckBox()
        split_cb.setToolTip("Check this if a single physical switch port will be split\n(using a breakout cable) to serve multiple logical connections.")
        grid.addWidget(split_cb, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
        widgets['split_cb'] = split_cb

        if row == 1: grid.itemAtPosition(0, col).widget().setToolTip("If splitting, select how many ways the port is split (e.g., 2 for 1:2, 4 for 1:4).")
        fac = QComboBox()
        fac.addItems(['2', '4'])
        fac.setToolTip("If splitting, select how many ways the port is split (e.g., 2 for 1:2, 4 for 1:4).")
        fac.setFixedWidth(50)
        grid.addWidget(fac, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
        widgets['fac'] = fac

        if row == 1: grid.itemAtPosition(0, col).widget().setToolTip("The number of extra physical ports to reserve alongside the assigned ports.\nThese are labeled as 'RSVD' in the diagram.")
        rsv = QLineEdit()
        rsv.setValidator(self.port_validator)
        rsv.setToolTip("The number of extra physical ports to reserve alongside the assigned ports.\nThese are labeled as 'RSVD' in the diagram.")
        rsv.setFixedWidth(40)
        grid.addWidget(rsv, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
        widgets['rsv'] = rsv

        if row == 1: grid.itemAtPosition(0, col).widget().setToolTip("Check this to manually assign specific port numbers instead of letting the tool auto-assign them.")
        lock_cb = QCheckBox()
        lock_cb.setToolTip("Check this to manually assign specific port numbers instead of letting the tool auto-assign them.")
        grid.addWidget(lock_cb, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
        widgets['lock_cb'] = lock_cb
        
        node_tooltip = "Mode 1 (Auto): Enter a SINGLE number for the LOWEST port in the auto-assigned range.\nMode 2 (Manual): Enter a full comma-separated list or range for precise control (e.g., 1-8,10)."
        uplink_tooltip = "Mode 1 (Auto): Enter a SINGLE number for the HIGHEST port in the auto-assigned range.\nMode 2 (Manual): Enter a full comma-separated list or range for precise control. Ports are assigned from high to low."
        if row == 1: grid.itemAtPosition(0, col).widget().setToolTip(f"Node Tab:\n{node_tooltip}\n\nUplink Tab:\n{uplink_tooltip}")
        st = QLineEdit()
        st.setValidator(self.port_list_validator)
        if is_node_tab:
            st.setToolTip(node_tooltip)
        else:
            st.setToolTip(uplink_tooltip)

        st.setEnabled(False)
        st.setFixedWidth(77) # Narrowed by 3 characters (was 80)
        grid.addWidget(st, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
        widgets['st'] = st
        
        # Column: Starting Node # (only for node types)
        if is_node_tab:
            # Create a container widget with prefix label and entry box
            starting_node_container = QWidget()
            starting_node_layout = QHBoxLayout(starting_node_container)
            starting_node_layout.setContentsMargins(2, 0, 2, 0)
            starting_node_layout.setSpacing(0)
            
            # Prefix label (fixed, unchangeable)
            prefix_label = QLabel(type_name)
            prefix_label.setFixedWidth(20) # 2 characters
            prefix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            prefix_label.setStyleSheet("QLabel { background-color: #555555; color: white; padding: 2px; font-weight: bold; }")
            starting_node_layout.addWidget(prefix_label)
            
            # Entry box for the number
            starting_node_entry = QLineEdit('')
            starting_node_entry.setValidator(self.port_validator)
            
            # Set default starting numbers based on node type
            default_starting_numbers = {
                'DN': '100',
                'CN': '1',
                'EB': '1',
                'IE': '1',
                'GN': '1'
            }
            starting_node_entry.setText(default_starting_numbers.get(type_name, '1'))
            starting_node_entry.setToolTip(f"Starting node number for {type_name} (e.g., {default_starting_numbers.get(type_name, '1')} for {type_name}-{default_starting_numbers.get(type_name, '1')}, {type_name}-{int(default_starting_numbers.get(type_name, '1'))+1}...)")
            starting_node_entry.setFixedWidth(25) # 3 characters for the number
            starting_node_entry.setEnabled(True)
            starting_node_layout.addWidget(starting_node_entry)
            
            starting_node_container.setFixedWidth(47) # Total width: 20 (prefix) + 25 (entry) + 2 (margins)
            grid.addWidget(starting_node_container, row, col, Qt.AlignmentFlag.AlignCenter); col += 1
            widgets['starting_node'] = starting_node_entry
            widgets['starting_node_prefix'] = prefix_label

        # Only store widgets if they don't already exist (prevent overwriting widgets from different UI tables)
        new_widgets = type_name not in entries_dict
        if new_widgets:
            entries_dict[type_name] = widgets

        # Connect signals - auto-assignment happens as you type (debounced via update_scheduler)
        # Only connect signals if these are new widgets (not already connected)
        if new_widgets:
            for w_key, w in widgets.items():
                if isinstance(w, QLineEdit):
                    w.textChanged.connect(lambda *_,
                                          func=update_scheduler: func())
                    if is_node_tab:
                        w.textChanged.connect(lambda *_,
                                              func=sync_connection: func())
                        w.textChanged.connect(lambda *_,
                                              func=self._schedule_auto_assign_nodes: func())
                    else:
                        w.textChanged.connect(lambda *_,
                                              func=self._schedule_auto_assign_uplinks: func())
                        # Update suggestions for ISL and MLAG/BGP when their fields change
                        # Also connect to uplink speed changes
                        if type_name in ['ISL', 'MLAG/BGP'] and w_key in ['gcnt', 'ppg']:
                            w.textChanged.connect(lambda *_,
                                                  func=self._update_uplink_suggestions: func())
                elif isinstance(w, QCheckBox) and w_key != 'lock_cb':
                    w.stateChanged.connect(lambda *_,
                                            func=update_scheduler: func())
                    if is_node_tab:
                        w.stateChanged.connect(lambda *_,
                                                func=sync_connection: func())
                        w.stateChanged.connect(lambda *_,
                                                func=self._schedule_auto_assign_nodes: func())
                    else:
                        w.stateChanged.connect(lambda *_,
                                               func=self._schedule_auto_assign_uplinks: func())
                elif isinstance(w, QComboBox):
                    w.currentIndexChanged.connect(lambda *_,
                                                  func=update_scheduler: func())
                    if is_node_tab:
                        w.currentIndexChanged.connect(lambda *_,
                                                       func=sync_connection: func())
                        w.currentIndexChanged.connect(lambda *_,
                                                       func=self._schedule_auto_assign_nodes: func())
                    else:
                        w.currentIndexChanged.connect(lambda *_,
                                                       func=self._schedule_auto_assign_uplinks: func())

            lock_cb.stateChanged.connect(lambda _, tn=type_name, node=is_node_tab: self._on_manual_toggle(tn, is_node_tab=node))

    def _build_node_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("DarkTab")
        main_layout = QVBoxLayout(main_widget)

        # Mode toggle section
        mode_group = QGroupBox('Mapping Mode')
        mode_layout = QHBoxLayout(mode_group)
        mode_layout.setContentsMargins(10, 5, 10, 5)
        
        mode_label = QLabel('Select Mapping Mode:')
        mode_layout.addWidget(mode_label)
        
        self.cell_planning_mode_default_radio = QRadioButton('Default Mapping')
        self.cell_planning_mode_advanced_radio = QRadioButton('Advanced Mapping')
        self.cell_planning_mode_default_radio.setChecked(True)  # Default selected
        self.cell_planning_mode_default_radio.setToolTip('Port layout logic as defined by Vast Engineering')
        self.cell_planning_mode_advanced_radio.setToolTip('Allows cables to flow into switch via Left or Right sides with user preference, prevents cable overlapping')
        
        mode_layout.addWidget(self.cell_planning_mode_default_radio)
        mode_layout.addWidget(self.cell_planning_mode_advanced_radio)
        mode_layout.addStretch()
        
        # Connect mode toggle
        self.cell_planning_mode_default_radio.toggled.connect(self._on_cell_planning_mode_changed)
        self.cell_planning_mode_advanced_radio.toggled.connect(self._on_cell_planning_mode_changed)
        
        main_layout.addWidget(mode_group)
        
        # Create stacked widget to switch between Default and Advanced modes
        self.cell_planning_stacked = QStackedWidget()
        main_layout.addWidget(self.cell_planning_stacked)
        
        # Default mode widget (existing UI)
        default_mode_widget = QWidget()
        default_mode_layout = QVBoxLayout(default_mode_widget)
        default_mode_layout.setContentsMargins(0, 0, 0, 0)
        
        input_group = QGroupBox('Configure Node Types Per Cell')
        input_group_layout = QVBoxLayout(input_group)
        
        # Switch type label will be displayed over the preview images below
        
        # Add permanent help message
        help_label = QLabel("ℹ️  Detail the # of device type NODES that will connect to each A/B switch in each cell. Ex: Ceres V1 Dboxes have 4 ports per switch, Ceres V2 & Mavericks have 2. Compute Nodes have 1.")
        help_label.setWordWrap(True)
        help_label.setMaximumWidth(500)  # Constrain width to match table
        help_label.setStyleSheet("""
            QLabel {
                background-color: #E3F2FD;
                color: #1565C0;
                padding: 4px;
                border-radius: 3px;
                border: 1px solid #90CAF9;
                font-size: 11pt;
            }
        """)
        input_group_layout.addWidget(help_label)
        
        # Create the grid for the configuration table
        grid = QGridLayout()
        grid.setColumnMinimumWidth(6, 77) # Set minimum width for manual port entry column
        grid.setColumnMinimumWidth(7, 47) # Set minimum width for starting node # column (prefix + entry box)
        # Don't add stretch to keep columns compact
        input_group_layout.addLayout(grid)

        node_descriptions = {
            'DN': 'The number of DNodes per fabric.',
            'CN': 'The number of CNodes per fabric.',
            'EB': 'The number of Eboxes per fabric.',
            'IE': 'The number of Insight Engine Nodes per fabric.',
            'GN': 'The number of GPU Nodes per fabric.'
        }

        headers = ['Node\nTypes', 'Node\nCount', 'Split\nPorts?', 'Split\nValue', 'Reserved\nPort Count', 'Manual\nInput', 'Manual\nPort Entry', 'Starting\nNode #']
        for i, h in enumerate(headers):
            label = QLabel(h)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setToolTip(node_descriptions.get(h.split('\n')[0], '')) # Simple tooltip for headers
            grid.addWidget(label, 0, i)

        self.node_types = ['DN', 'CN', 'EB', 'IE', 'GN']

        for r, nt in enumerate(self.node_types, 1):
            self._create_port_config_row(grid, r, nt, node_descriptions.get(nt, ''), is_node_tab=True)
        
        # Connect CN and EB node count changes to auto-update NB when 2nd NIC is enabled
        if 'CN' in self.node_entries:
            self.node_entries['CN']['cnt'].textChanged.connect(self._on_cnode_count_changed)
        if 'EB' in self.node_entries:
            self.node_entries['EB']['cnt'].textChanged.connect(self._on_cnode_count_changed)

        # Create horizontal container for side-by-side Node Types and Uplink tables
        tables_container = QWidget()
        tables_layout = QHBoxLayout(tables_container)
        tables_layout.setContentsMargins(0, 0, 0, 0)
        tables_layout.setSpacing(5)  # Add small spacing between tables
        
        # Reduce margins on both input groups to bring tables closer together
        input_group.setContentsMargins(10, 10, 10, 10)  # Reduce default QGroupBox margins
        
        # Left side: Node Types table
        tables_layout.addWidget(input_group, 1)
        
        # Right side: Uplink table
        uplink_input_group = QGroupBox('Configure Uplinks To/From Per Cell')
        uplink_input_group.setContentsMargins(10, 5, 10, 5)  # Reduce top/bottom margins
        uplink_input_group_layout = QVBoxLayout(uplink_input_group)
        uplink_input_group_layout.setSpacing(5)  # Reduce spacing between widgets
        
        # No switch type label needed for uplink table (only Node Types needs it)
        
        # Add help label for uplinks
        uplink_help_label = QLabel("ℹ️  This table configures Uplink ports. For ISL and Customer uplinks, set the number of Port Channels to use, and then the number of ports PER channel they should contain.")
        uplink_help_label.setWordWrap(True)
        uplink_help_label.setMaximumWidth(600)  # Constrain width to match uplink table
        uplink_help_label.setMaximumHeight(50)  # Limit height to 2 rows of text
        uplink_help_label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)  # Don't stretch vertically
        uplink_help_label.setStyleSheet("""
            QLabel {
                background-color: #E3F2FD;
                color: #1565C0;
                padding: 2px 4px;
                border-radius: 3px;
                border: 1px solid #90CAF9;
                font-size: 11pt;
            }
        """)
        uplink_input_group_layout.addWidget(uplink_help_label)
        
        uplink_grid = QGridLayout()
        uplink_input_group_layout.addLayout(uplink_grid)
        
        uplink_descriptions = {
            'IPL': 'The number of Inter-Peer Link ports between leaf pairs.',
            'ISL': 'The number of Inter-Switch Link groups, and ports per group to/from Leafs And Spines.',
            'MLAG/BGP': 'The number of uplink groups and ports per group to customer gear.',
            'NB': 'The number of Cnode/Ebox 2nd NIC Northbound ports per fabric.'
        }
        
        uplink_headers = ['Uplink\nType', '# Of Uplink\nChannels', 'Ports\nPer Group', 'Split\nPorts?', 'Split\nValue', 'Reserved\nPort Count', 'Manual\nInput', 'Assigned\nPorts', 'Suggestion']
        for i, h in enumerate(uplink_headers):
            label = QLabel(h)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if h == '# Of Uplink\nChannels':
                label.setToolTip('Number of uplink destinations being spines (ISLs) or customer switches (MLAG or BGP). Each uplink gets its ports defined in \'Ports/Group\'')
            elif h == 'Suggestion':
                label.setToolTip('Recommended ports per group for non-blocking fabric based on Max BW Required Per Cell')
            else:
                label.setToolTip(uplink_descriptions.get(h.split('\n')[0], ''))
            uplink_grid.addWidget(label, 0, i)
        
        self.uplink_types = ['IPL', 'ISL', 'MLAG/BGP', 'NB']
        # Initialize uplink_suggestion_labels before creating any rows
        if not hasattr(self, 'uplink_suggestion_labels'):
            self.uplink_suggestion_labels = {}  # Store suggestion labels for each uplink type - only initialize once
        
        for r, ut in enumerate(self.uplink_types, 1):
            self._create_port_config_row(uplink_grid, r, ut, uplink_descriptions.get(ut, ''), is_node_tab=False)
            # For IPL and NB, the group count is always 1 and should be disabled.
            if ut in ['IPL', 'NB']:
                gcnt_widget = self.uplink_entries[ut]['gcnt']
                gcnt_widget.setText('1')
                gcnt_widget.setEnabled(False)
                # Style disabled field to appear grey so user knows not to edit it
                gcnt_widget.setStyleSheet("QLineEdit:disabled { background-color: #555555; color: #AAAAAA; }")
            
            # Add event handlers for IPL/ISL mutual exclusion
            if ut in ['IPL', 'ISL']:
                self.uplink_entries[ut]['ppg'].textChanged.connect(self._on_uplink_count_changed)
            
            # Add suggestion label for ISL and MLAG/BGP (shown as EXT in UI)
            if ut in ['ISL', 'MLAG/BGP']:
                suggestion_label = QLabel('')
                suggestion_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                suggestion_label.setWordWrap(False)
                suggestion_label.setStyleSheet("QLabel { padding-left: 10px; min-width: 200px; }")
                uplink_grid.addWidget(suggestion_label, r, 8)
                # Store with suffix to differentiate from Node Types tab labels
                # Use EXT as the key for MLAG/BGP in the suggestion labels dictionary
                key_suffix = 'EXT' if ut == 'MLAG/BGP' else ut
                self.uplink_suggestion_labels[key_suffix + '_node_tab'] = suggestion_label
        
        # Don't add stretch to keep columns compact
        
        # Add uplink table to the right side
        tables_layout.addWidget(uplink_input_group, 1)
        
        # Add the combined tables container to main layout
        default_mode_layout.addWidget(tables_container)
        
        # IMPORTANT: After the entire Node Types UI is built, initialize uplink table
        # This is deferred because leaf_spine_combo and node_entries may not be ready yet
        # We'll trigger this initialization after the full UI is built
        QTimer.singleShot(0, self._initialize_node_tab_uplinks)
        
        # Clone to Multi-Rack section
        clone_group = QGroupBox("Clone to Multi-Rack Design")
        clone_layout = QHBoxLayout(clone_group)
        
        clone_question_label = QLabel("Clone this cell and add to a Multi Rack Design? How many times:")
        clone_question_label.setToolTip("Number of racks to create in the multi-rack design.")
        clone_layout.addWidget(clone_question_label)
        
        self.clone_count_entry = QLineEdit()
        self.clone_count_entry.setValidator(self.numeric_validator)
        self.clone_count_entry.setText("1")
        self.clone_count_entry.setFixedWidth(40)
        self.clone_count_entry.setToolTip("Number of racks to create in the multi-rack design.")
        clone_layout.addWidget(self.clone_count_entry)
        
        # Add rack name entry
        name_label = QLabel("Rack Name:")
        name_label.setToolTip("Base name for racks (max 10 characters, will be suffixed with 1, 2, etc.)")
        clone_layout.addWidget(name_label)
        
        self.clone_rack_name_entry = QLineEdit()
        self.clone_rack_name_entry.setMaxLength(20)
        self.clone_rack_name_entry.setText("Leaf Rack")
        self.clone_rack_name_entry.setFixedWidth(120)
        self.clone_rack_name_entry.setToolTip("Base name for racks (max 20 characters, will be suffixed with 1, 2, etc.)")
        clone_layout.addWidget(self.clone_rack_name_entry)
        
        # Add leaf/spine type dropdown
        type_label = QLabel("Type:")
        type_label.setToolTip("Design type: Leaf or Spine")
        clone_layout.addWidget(type_label)
        
        self.clone_rack_type_combo = QComboBox()
        self.clone_rack_type_combo.addItems(['leaf', 'spine'])
        self.clone_rack_type_combo.setToolTip("Design type: Leaf or Spine")
        clone_layout.addWidget(self.clone_rack_type_combo)
        
        clone_go_button = QPushButton("Go")
        clone_go_button.setToolTip("Add racks to the multi-rack design.")
        clone_go_button.clicked.connect(self._on_clone_to_multi_rack_go)
        clone_layout.addWidget(clone_go_button)
        
        clone_layout.addStretch()
        default_mode_layout.addWidget(clone_group)
        
        self.clone_count_entry_for_button = self.clone_count_entry
        
        # Initialize the clone rack type to match the current leaf/spine setting
        if hasattr(self, 'leaf_spine_combo'):
            self.clone_rack_type_combo.setCurrentText(self.leaf_spine_combo.currentText())
        else:
            self.clone_rack_type_combo.setCurrentText('leaf')

        # Live Preview Area (Assign button removed - auto-assignment happens as you type)
        self.node_live_preview_label = QLabel()
        default_mode_layout.addWidget(self.node_live_preview_label)
        
        # Add plain centered switch type label above preview images
        switch_label = QLabel()
        switch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        switch_label.setStyleSheet("font-size: 12pt; font-weight: bold; padding: 5px;")
        default_mode_layout.addWidget(switch_label)
        self.node_switch_label = switch_label
        
        self.node_canvas_a = ScalableLabel("Fabric A Preview")
        self.node_canvas_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.node_canvas_a.setFrameShape(QFrame.Shape.StyledPanel)
        self.node_canvas_a.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.node_canvas_b = ScalableLabel("Fabric B Preview")
        self.node_canvas_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.node_canvas_b.setFrameShape(QFrame.Shape.StyledPanel)
        self.node_canvas_b.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # Create a container widget for the vertically stacked previews
        previews_container = QWidget()
        previews_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        previews_vbox = QVBoxLayout(previews_container)
        previews_vbox.setContentsMargins(0, 0, 0, 0)
        previews_vbox.addWidget(self.node_canvas_b)
        previews_vbox.addWidget(self.node_canvas_a)

        # Use a horizontal layout to constrain the width of the container to 95%
        previews_hbox = QHBoxLayout()
        previews_hbox.addStretch(5)  # 2.5% margin
        previews_hbox.addWidget(previews_container, 190)  # Container takes 95%
        previews_hbox.addStretch(5)  # 2.5% margin
        default_mode_layout.addLayout(previews_hbox)
        
        # Add default mode widget to stacked widget
        self.cell_planning_stacked.addWidget(default_mode_widget)
        
        # Advanced mode widget (will be created in helper method)
        advanced_mode_widget = self._build_cell_planning_advanced_mode_ui()
        self.cell_planning_stacked.addWidget(advanced_mode_widget)
        
        # Set initial mode
        self.cell_planning_stacked.setCurrentIndex(0)  # Default mode

        return main_widget

    def _on_cell_planning_mode_changed(self):
        """Handle mode toggle between Default and Advanced mapping."""
        if self.cell_planning_mode_default_radio.isChecked():
            self.cell_planning_mode = 'default'
            self.cell_planning_stacked.setCurrentIndex(0)
            # Sync data from advanced mode to default mode
            self._sync_advanced_to_default()
        else:
            self.cell_planning_mode = 'advanced'
            self.cell_planning_stacked.setCurrentIndex(1)
            # Sync data from default mode to advanced mode
            self._sync_default_to_advanced()
            # Trigger recalculation for advanced mode
            self._on_cell_planning_advanced_recalculate()

    def _sync_default_to_advanced(self):
        """Sync node and uplink data from Default mode UI to Advanced mode UI."""
        if not hasattr(self, 'cell_planning_advanced_dn_count'):
            return
        
        # Sync DN count
        if 'DN' in self.node_entries:
            dn_count = self.node_entries['DN']['cnt'].text()
            self.cell_planning_advanced_dn_count.setText(dn_count)
            if 'DN' in self.node_entries:
                ent = self.node_entries['DN']
                self.cell_planning_advanced_dn_split_cb.setChecked(ent['split_cb'].isChecked())
                self.cell_planning_advanced_dn_factor.setCurrentText(ent['fac'].currentText())
                # Sync starting node for DN
                if hasattr(self, 'cell_planning_advanced_node_widgets') and 'DN' in self.cell_planning_advanced_node_widgets:
                    dn_starting_widget = self.cell_planning_advanced_node_widgets['DN'].get('starting_node')
                    if dn_starting_widget and 'starting_node' in ent:
                        dn_starting_widget.setText(ent['starting_node'].text())
        
        # Sync other node types
        for nt in ['CN', 'EB', 'IE', 'GN']:
            if nt in self.node_entries and nt in self.cell_planning_advanced_node_counts:
                ent = self.node_entries[nt]
                self.cell_planning_advanced_node_counts[nt].setText(ent['cnt'].text())
                if nt in self.cell_planning_advanced_node_splits:
                    self.cell_planning_advanced_node_splits[nt]['split_cb'].setChecked(ent['split_cb'].isChecked())
                    self.cell_planning_advanced_node_splits[nt]['factor'].setCurrentText(ent['fac'].currentText())
                # Sync starting node
                if hasattr(self, 'cell_planning_advanced_node_widgets') and nt in self.cell_planning_advanced_node_widgets:
                    nt_starting_widget = self.cell_planning_advanced_node_widgets[nt].get('starting_node')
                    if nt_starting_widget and 'starting_node' in ent:
                        nt_starting_widget.setText(ent['starting_node'].text())
        
        # Sync uplinks
        for ut in ['IPL', 'ISL', 'MLAG/BGP']:
            if ut in self.uplink_entries:
                ent = self.uplink_entries[ut]
                # Map MLAG/BGP to EXT for advanced UI
                lookup_key = 'EXT' if ut == 'MLAG/BGP' else ut
                if lookup_key in self.cell_planning_advanced_uplink_widgets:
                    groups_widget = self.cell_planning_advanced_uplink_widgets[lookup_key]['groups']
                    ppg_widget = self.cell_planning_advanced_uplink_widgets[lookup_key]['ppg']
                    gcnt_val = ent.get('gcnt', QLineEdit('1')).text() if ut not in ['IPL', 'NB'] else '1'
                    groups_widget.setText(gcnt_val)
                    ppg_widget.setText(ent['ppg'].text())
                    # Update config
                    self.cell_planning_advanced_config['uplinks'][lookup_key] = {
                        'groups': safe_int(gcnt_val, 1 if ut == 'IPL' else 0),
                        'ports_per_group': safe_int(ent['ppg'].text(), 0)
                    }

    def _sync_advanced_to_default(self):
        """Sync node and uplink data from Advanced mode UI to Default mode UI."""
        if not hasattr(self, 'cell_planning_advanced_dn_count'):
            return
        
        # Sync DN count
        if 'DN' in self.node_entries:
            dn_count = self.cell_planning_advanced_dn_count.text()
            self.node_entries['DN']['cnt'].setText(dn_count)
            self.node_entries['DN']['split_cb'].setChecked(self.cell_planning_advanced_dn_split_cb.isChecked())
            self.node_entries['DN']['fac'].setCurrentText(self.cell_planning_advanced_dn_factor.currentText())
            # Sync starting node for DN
            if hasattr(self, 'cell_planning_advanced_node_widgets') and 'DN' in self.cell_planning_advanced_node_widgets:
                dn_starting_widget = self.cell_planning_advanced_node_widgets['DN'].get('starting_node')
                if dn_starting_widget and 'DN' in self.node_entries and 'starting_node' in self.node_entries['DN']:
                    self.node_entries['DN']['starting_node'].setText(dn_starting_widget.text())
        
        # Sync other node types
        for nt in ['CN', 'EB', 'IE', 'GN']:
            if nt in self.node_entries and nt in self.cell_planning_advanced_node_counts:
                self.node_entries[nt]['cnt'].setText(self.cell_planning_advanced_node_counts[nt].text())
                if nt in self.cell_planning_advanced_node_splits:
                    self.node_entries[nt]['split_cb'].setChecked(
                        self.cell_planning_advanced_node_splits[nt]['split_cb'].isChecked())
                    self.node_entries[nt]['fac'].setCurrentText(
                        self.cell_planning_advanced_node_splits[nt]['factor'].currentText())
                # Sync starting node
                if hasattr(self, 'cell_planning_advanced_node_widgets') and nt in self.cell_planning_advanced_node_widgets:
                    nt_starting_widget = self.cell_planning_advanced_node_widgets[nt].get('starting_node')
                    if nt_starting_widget and nt in self.node_entries and 'starting_node' in self.node_entries[nt]:
                        self.node_entries[nt]['starting_node'].setText(nt_starting_widget.text())
        
        # Sync uplinks
        for ut in ['IPL', 'ISL', 'MLAG/BGP']:
            if ut in self.uplink_entries:
                # Map MLAG/BGP to EXT for advanced UI lookup
                lookup_key = 'EXT' if ut == 'MLAG/BGP' else ut
                if lookup_key in self.cell_planning_advanced_uplink_widgets:
                    groups_widget = self.cell_planning_advanced_uplink_widgets[lookup_key]['groups']
                    ppg_widget = self.cell_planning_advanced_uplink_widgets[lookup_key]['ppg']
                    ent = self.uplink_entries[ut]
                    if 'gcnt' in ent and ut not in ['IPL', 'NB']:
                        ent['gcnt'].setText(groups_widget.text())
                    ent['ppg'].setText(ppg_widget.text())

    def _build_cell_planning_advanced_mode_ui(self):
        """Builds the Advanced mode UI for Cell Planning tab."""
        main_widget = QWidget()
        main_widget.setObjectName("DarkTab")
        main_layout = QVBoxLayout(main_widget)
        
        # Switch model display (read-only from Setup tab) - compact single line
        switch_info_layout = QHBoxLayout()
        switch_info_layout.setContentsMargins(0, 0, 0, 5)
        self.cell_planning_advanced_switch_label = QLabel('Switch Model: Not loaded - configure on Setup tab')
        self.cell_planning_advanced_switch_label.setStyleSheet("font-weight: bold; color: #4a90e2;")
        switch_info_layout.addWidget(self.cell_planning_advanced_switch_label)
        switch_info_layout.addStretch()
        main_layout.addLayout(switch_info_layout)
        
        # DBox type selector
        dbox_group = QGroupBox('DBox Type')
        dbox_layout = QHBoxLayout(dbox_group)
        self.cell_planning_advanced_dbox_mav = QRadioButton('Mav')
        self.cell_planning_advanced_dbox_ceresv1 = QRadioButton('CeresV1')
        self.cell_planning_advanced_dbox_ceresv2 = QRadioButton('CeresV2')
        # Connect signals BEFORE setting checked to avoid premature handler calls
        self.cell_planning_advanced_dbox_mav.toggled.connect(self._on_cell_planning_advanced_dbox_changed)
        self.cell_planning_advanced_dbox_ceresv1.toggled.connect(self._on_cell_planning_advanced_dbox_changed)
        self.cell_planning_advanced_dbox_ceresv2.toggled.connect(self._on_cell_planning_advanced_dbox_changed)
        # Set default AFTER connecting signals
        self.cell_planning_advanced_dbox_ceresv1.setChecked(True)  # Default
        dbox_layout.addWidget(QLabel('Select DBox Type:'))
        dbox_layout.addWidget(self.cell_planning_advanced_dbox_mav)
        dbox_layout.addWidget(self.cell_planning_advanced_dbox_ceresv1)
        dbox_layout.addWidget(self.cell_planning_advanced_dbox_ceresv2)
        dbox_layout.addStretch()
        main_layout.addWidget(dbox_group)
        
        # Combined configuration section: Node config and Uplink config side-by-side
        config_group = QGroupBox('Configuration')
        config_layout = QHBoxLayout(config_group)
        
        # Left side: Node counts and routing configuration
        node_counts_group = QWidget()
        node_counts_group.setMaximumWidth(450)
        node_counts_layout = QGridLayout(node_counts_group)
        node_counts_layout.setColumnStretch(0, 0)
        node_counts_layout.setColumnStretch(1, 0)
        node_counts_layout.setColumnStretch(2, 0)
        node_counts_layout.setColumnStretch(3, 0)
        node_counts_layout.setColumnStretch(4, 0)
        node_counts_layout.setColumnStretch(5, 0)
        
        # Headers
        node_counts_layout.addWidget(QLabel('<b>Type</b>'), 0, 0)
        node_counts_layout.addWidget(QLabel('<b>Count</b>'), 0, 1)
        node_counts_layout.addWidget(QLabel('<b>Split</b>'), 0, 2)
        node_counts_layout.addWidget(QLabel('<b>Factor</b>'), 0, 3)
        node_counts_layout.addWidget(QLabel('<b>Route</b>'), 0, 4)
        node_counts_layout.addWidget(QLabel('<b>Starting\nNode #</b>'), 0, 5)
        
        # DN row
        node_counts_layout.addWidget(QLabel('DN:'), 1, 0)
        self.cell_planning_advanced_dn_count = QLineEdit('')
        self.cell_planning_advanced_dn_count.setValidator(self.port_validator)
        self.cell_planning_advanced_dn_count.setToolTip('Number of Data Nodes (must be even - 2 per DBox)')
        self.cell_planning_advanced_dn_count.setFixedWidth(40)
        self.cell_planning_advanced_dn_count.editingFinished.connect(self._validate_cell_planning_dn_count_even)
        self.cell_planning_advanced_dn_count.returnPressed.connect(self._validate_cell_planning_dn_count_even)
        node_counts_layout.addWidget(self.cell_planning_advanced_dn_count, 1, 1)
        
        # DN split options
        self.cell_planning_advanced_dn_split_cb = QCheckBox()
        self.cell_planning_advanced_dn_split_cb.setToolTip('Check if using breakout cables to split DN ports')
        self.cell_planning_advanced_dn_split_cb.toggled.connect(self._on_cell_planning_advanced_recalculate)
        node_counts_layout.addWidget(self.cell_planning_advanced_dn_split_cb, 1, 2)
        
        self.cell_planning_advanced_dn_factor = QComboBox()
        self.cell_planning_advanced_dn_factor.addItems(['2', '4'])
        self.cell_planning_advanced_dn_factor.setToolTip('Split factor: 2 for 1:2, 4 for 1:4')
        self.cell_planning_advanced_dn_factor.setFixedWidth(50)
        self.cell_planning_advanced_dn_factor.currentTextChanged.connect(self._on_cell_planning_advanced_recalculate)
        node_counts_layout.addWidget(self.cell_planning_advanced_dn_factor, 1, 3)
        
        # DN is fixed (Even=LEFT, Odd=RIGHT)
        dn_route_label = QLabel('(fixed)')
        dn_route_label.setStyleSheet("color: #888888; font-size: 9pt;")
        node_counts_layout.addWidget(dn_route_label, 1, 4)
        
        # DN Starting Node # widget
        self.cell_planning_advanced_node_widgets = {}
        dn_starting_node_container = QWidget()
        dn_starting_node_layout = QHBoxLayout(dn_starting_node_container)
        dn_starting_node_layout.setContentsMargins(2, 0, 2, 0)
        dn_starting_node_layout.setSpacing(0)
        
        dn_prefix_label = QLabel('DN')
        dn_prefix_label.setFixedWidth(20)
        dn_prefix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dn_prefix_label.setStyleSheet("QLabel { background-color: #555555; color: white; padding: 2px; font-weight: bold; }")
        dn_starting_node_layout.addWidget(dn_prefix_label)
        
        self.cell_planning_advanced_dn_starting_node = QLineEdit('100')
        self.cell_planning_advanced_dn_starting_node.setValidator(self.port_validator)
        self.cell_planning_advanced_dn_starting_node.setToolTip("Starting node number for DN (e.g., 100 for DN-100, DN-101...)")
        self.cell_planning_advanced_dn_starting_node.setFixedWidth(25)
        self.cell_planning_advanced_dn_starting_node.setEnabled(True)
        self.cell_planning_advanced_dn_starting_node.textChanged.connect(self._on_cell_planning_advanced_recalculate)
        dn_starting_node_layout.addWidget(self.cell_planning_advanced_dn_starting_node)
        
        dn_starting_node_container.setFixedWidth(47)
        node_counts_layout.addWidget(dn_starting_node_container, 1, 5)
        self.cell_planning_advanced_node_widgets['DN'] = {
            'starting_node': self.cell_planning_advanced_dn_starting_node,
            'starting_node_prefix': dn_prefix_label
        }
        
        node_types_to_add = ['CN', 'EB', 'IE', 'GN']
        self.cell_planning_advanced_node_counts = {}
        self.cell_planning_advanced_node_splits = {}
        self.cell_planning_advanced_routing_widgets = {}
        
        for i, nt in enumerate(node_types_to_add, 2):
            node_counts_layout.addWidget(QLabel(f'{nt}:'), i, 0)
            count_entry = QLineEdit('')
            count_entry.setValidator(self.port_validator)
            count_entry.setFixedWidth(40)
            self.cell_planning_advanced_node_counts[nt] = count_entry
            node_counts_layout.addWidget(count_entry, i, 1)
            
            # Split checkbox
            split_cb = QCheckBox()
            split_cb.setToolTip('Check if using breakout cables to split ports')
            self.cell_planning_advanced_node_splits[nt] = {'split_cb': split_cb, 'factor': None}
            node_counts_layout.addWidget(split_cb, i, 2)
            
            # Factor combo
            factor_combo = QComboBox()
            factor_combo.addItems(['2', '4'])
            factor_combo.setToolTip('Split factor: 2 for 1:2, 4 for 1:4')
            factor_combo.setFixedWidth(50)
            self.cell_planning_advanced_node_splits[nt]['factor'] = factor_combo
            node_counts_layout.addWidget(factor_combo, i, 3)
            
            # L/R routing radio buttons (compact, inline)
            routing_container = QWidget()
            routing_hbox = QHBoxLayout(routing_container)
            routing_hbox.setContentsMargins(0, 0, 0, 0)
            routing_hbox.setSpacing(2)
            
            left_radio = QRadioButton('L')
            right_radio = QRadioButton('R')
            right_radio.setChecked(True)  # Default to RIGHT
            left_radio.setFixedWidth(22)
            right_radio.setFixedWidth(22)
            routing_hbox.addWidget(left_radio)
            routing_hbox.addWidget(right_radio)
            self.cell_planning_advanced_routing_widgets[nt] = {'left': left_radio, 'right': right_radio}
            
            left_radio.toggled.connect(self._on_cell_planning_advanced_recalculate)
            right_radio.toggled.connect(self._on_cell_planning_advanced_recalculate)
            node_counts_layout.addWidget(routing_container, i, 4)
            
            # Starting Node # widget
            default_starting_numbers = {
                'CN': '1',
                'EB': '1',
                'IE': '1',
                'GN': '1'
            }
            starting_node_container = QWidget()
            starting_node_layout = QHBoxLayout(starting_node_container)
            starting_node_layout.setContentsMargins(2, 0, 2, 0)
            starting_node_layout.setSpacing(0)
            
            prefix_label = QLabel(nt)
            prefix_label.setFixedWidth(20)
            prefix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            prefix_label.setStyleSheet("QLabel { background-color: #555555; color: white; padding: 2px; font-weight: bold; }")
            starting_node_layout.addWidget(prefix_label)
            
            starting_node_entry = QLineEdit(default_starting_numbers.get(nt, '1'))
            starting_node_entry.setValidator(self.port_validator)
            starting_node_entry.setToolTip(f"Starting node number for {nt} (e.g., {default_starting_numbers.get(nt, '1')} for {nt}-{default_starting_numbers.get(nt, '1')}, {nt}-{int(default_starting_numbers.get(nt, '1'))+1}...)")
            starting_node_entry.setFixedWidth(25)
            starting_node_entry.setEnabled(True)
            starting_node_entry.textChanged.connect(self._on_cell_planning_advanced_recalculate)
            starting_node_layout.addWidget(starting_node_entry)
            
            starting_node_container.setFixedWidth(47)
            node_counts_layout.addWidget(starting_node_container, i, 5)
            
            if nt not in self.cell_planning_advanced_node_widgets:
                self.cell_planning_advanced_node_widgets[nt] = {}
            self.cell_planning_advanced_node_widgets[nt]['starting_node'] = starting_node_entry
            self.cell_planning_advanced_node_widgets[nt]['starting_node_prefix'] = prefix_label
            
            # Connect signals
            count_entry.textChanged.connect(self._on_cell_planning_advanced_counts_changed)
            split_cb.toggled.connect(self._on_cell_planning_advanced_recalculate)
            factor_combo.currentTextChanged.connect(self._on_cell_planning_advanced_recalculate)
        
        # Add node counts table to config layout (left side)
        config_layout.addWidget(node_counts_group)
        
        # Right side: Uplink configuration
        uplink_group = QGroupBox('Uplink Configuration')
        uplink_layout = QGridLayout(uplink_group)
        uplink_layout.setHorizontalSpacing(5)
        uplink_layout.setColumnStretch(0, 0)
        uplink_layout.setColumnStretch(1, 0)
        uplink_layout.setColumnStretch(2, 0)
        uplink_types = ['IPL', 'ISL', 'EXT']
        self.cell_planning_advanced_uplink_widgets = {}
        
        uplink_layout.addWidget(QLabel('Uplink Type'), 0, 0)
        uplink_layout.addWidget(QLabel('Groups'), 0, 1)
        uplink_layout.addWidget(QLabel('Ports/Group'), 0, 2)
        
        for i, ut in enumerate(uplink_types, 1):
            ut_label = QLabel(ut)
            ut_label.setFixedWidth(30)
            uplink_layout.addWidget(ut_label, i, 0)
            groups_entry = QLineEdit(str(self.cell_planning_advanced_config['uplinks'][ut]['groups']) if self.cell_planning_advanced_config['uplinks'][ut]['groups'] > 0 else '')
            groups_entry.setValidator(self.port_validator)
            
            # IPL groups is fixed at 1 and should be disabled/greyed out
            if ut == 'IPL':
                groups_entry.setEnabled(False)
                groups_entry.setText('1')
                groups_entry.setStyleSheet("background-color: #555555; color: #AAAAAA;")
                groups_entry.setToolTip('IPL is always a single group (fixed)')
            else:
                groups_entry.textChanged.connect(self._on_cell_planning_advanced_recalculate)
            
            ppg_val = self.cell_planning_advanced_config['uplinks'][ut]['ports_per_group']
            ppg_entry = QLineEdit(str(ppg_val) if ppg_val > 0 else '')
            ppg_entry.setValidator(self.port_validator)
            ppg_entry.setFixedWidth(40)
            groups_entry.setFixedWidth(40)
            self.cell_planning_advanced_uplink_widgets[ut] = {'groups': groups_entry, 'ppg': ppg_entry}
            uplink_layout.addWidget(groups_entry, i, 1)
            uplink_layout.addWidget(ppg_entry, i, 2)
            ppg_entry.textChanged.connect(self._on_cell_planning_advanced_recalculate)
        
        config_layout.addWidget(uplink_group)
        main_layout.addWidget(config_group)
        
        # Clone to Multi-Rack section
        clone_group = QGroupBox("Clone to Multi-Rack Design")
        clone_layout = QHBoxLayout(clone_group)
        
        clone_question_label = QLabel("Clone this cell and add to a Multi Rack Design? How many times:")
        clone_question_label.setToolTip("Number of racks to create in the multi-rack design.")
        clone_layout.addWidget(clone_question_label)
        
        self.cell_planning_advanced_clone_count_entry = QLineEdit()
        self.cell_planning_advanced_clone_count_entry.setValidator(self.numeric_validator)
        self.cell_planning_advanced_clone_count_entry.setText("1")
        self.cell_planning_advanced_clone_count_entry.setFixedWidth(40)
        self.cell_planning_advanced_clone_count_entry.setToolTip("Number of racks to create in the multi-rack design.")
        clone_layout.addWidget(self.cell_planning_advanced_clone_count_entry)
        
        name_label = QLabel("Rack Name:")
        name_label.setToolTip("Base name for racks (max 20 characters, will be suffixed with 1, 2, etc.)")
        clone_layout.addWidget(name_label)
        
        self.cell_planning_advanced_clone_rack_name_entry = QLineEdit()
        self.cell_planning_advanced_clone_rack_name_entry.setMaxLength(20)
        self.cell_planning_advanced_clone_rack_name_entry.setText("Leaf Rack")
        self.cell_planning_advanced_clone_rack_name_entry.setFixedWidth(120)
        self.cell_planning_advanced_clone_rack_name_entry.setToolTip("Base name for racks (max 20 characters, will be suffixed with 1, 2, etc.)")
        clone_layout.addWidget(self.cell_planning_advanced_clone_rack_name_entry)
        
        type_label = QLabel("Type:")
        type_label.setToolTip("Design type: Leaf or Spine")
        clone_layout.addWidget(type_label)
        
        self.cell_planning_advanced_clone_rack_type_combo = QComboBox()
        self.cell_planning_advanced_clone_rack_type_combo.addItems(['leaf', 'spine'])
        self.cell_planning_advanced_clone_rack_type_combo.setToolTip("Design type: Leaf or Spine")
        clone_layout.addWidget(self.cell_planning_advanced_clone_rack_type_combo)
        
        clone_go_button = QPushButton("Go")
        clone_go_button.setToolTip("Add racks to the multi-rack design.")
        clone_go_button.clicked.connect(self._on_cell_planning_advanced_clone_to_multi_rack_go)
        clone_layout.addWidget(clone_go_button)
        
        clone_layout.addStretch()
        main_layout.addWidget(clone_group)
        
        # Initialize the clone rack type to match the current leaf/spine setting
        if hasattr(self, 'leaf_spine_combo'):
            self.cell_planning_advanced_clone_rack_type_combo.setCurrentText(self.leaf_spine_combo.currentText())
        else:
            self.cell_planning_advanced_clone_rack_type_combo.setCurrentText('leaf')
        
        # Live preview section
        preview_group = QGroupBox('Live Preview')
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(5, 5, 5, 5)
        preview_layout.setSpacing(5)
        
        self.cell_planning_advanced_canvas_a = ScalableLabel("Fabric A Preview")
        self.cell_planning_advanced_canvas_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cell_planning_advanced_canvas_a.setFrameShape(QFrame.Shape.StyledPanel)
        self.cell_planning_advanced_canvas_a.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cell_planning_advanced_canvas_b = ScalableLabel("Fabric B Preview")
        self.cell_planning_advanced_canvas_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cell_planning_advanced_canvas_b.setFrameShape(QFrame.Shape.StyledPanel)
        self.cell_planning_advanced_canvas_b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        previews_container = QWidget()
        previews_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        previews_hbox = QHBoxLayout(previews_container)
        previews_hbox.setContentsMargins(0, 0, 0, 0)
        previews_hbox.setSpacing(3)
        previews_hbox.addWidget(self.cell_planning_advanced_canvas_b, 1)
        previews_hbox.addWidget(self.cell_planning_advanced_canvas_a, 1)
        
        preview_layout.addWidget(previews_container)
        main_layout.addWidget(preview_group)
        
        main_layout.addStretch()
        
        return main_widget

    def _on_cell_planning_advanced_dbox_changed(self):
        """Handle DBox type radio button changes in Cell Planning Advanced mode."""
        # Only process when a button is actually checked (not when unchecked)
        if self.cell_planning_advanced_dbox_mav.isChecked():
            self.cell_planning_advanced_config['dbox_type'] = 'Mav'
        elif self.cell_planning_advanced_dbox_ceresv1.isChecked():
            self.cell_planning_advanced_config['dbox_type'] = 'CeresV1'
        elif self.cell_planning_advanced_dbox_ceresv2.isChecked():
            self.cell_planning_advanced_config['dbox_type'] = 'CeresV2'
        else:
            return  # No button checked, skip recalculation
        
        # Recalculate immediately with the new DBox type
        self._on_cell_planning_advanced_recalculate()

    def _on_cell_planning_advanced_counts_changed(self):
        """Handle node count changes in Cell Planning Advanced mode."""
        self._on_cell_planning_advanced_recalculate()

    def _validate_cell_planning_dn_count_even(self):
        """Ensure DN count is always even in Cell Planning Advanced mode."""
        dn_count = safe_int(self.cell_planning_advanced_dn_count.text(), 0)
        if dn_count > 0 and dn_count % 2 != 0:
            # Round down to nearest even number
            even_count = dn_count - 1
            self.cell_planning_advanced_dn_count.setText(str(even_count))

    def _on_cell_planning_advanced_recalculate(self):
        """Recalculate port assignments and update live preview for Cell Planning Advanced mode."""
        if not self.config_started or not self.base_image:
            if hasattr(self, 'cell_planning_advanced_canvas_a'):
                self.cell_planning_advanced_canvas_a.setText('⬅ Load switch on Setup tab first')
                self.cell_planning_advanced_canvas_b.setText('⬅ Load switch on Setup tab first')
            return
        
        port_map = self._calculate_cell_planning_advanced_ports()
        self.cell_planning_advanced_port_map = port_map
        self._draw_cell_planning_advanced_preview()

    def _get_dnode_groups_by_dbox_type(self, dn_count: int, dbox_type: str) -> tuple[list[int], list[int]]:
        """
        Returns lists of DNode numbers for LEFT and RIGHT sides based on DBox type.
        
        CeresV1: ODD → RIGHT, EVEN → LEFT
          RIGHT: DNodes 1,3,5,7,9,11,...
          LEFT: DNodes 2,4,6,8,10,12,...
        
        CeresV2/Mav: Groups of 2 DNodes, alternating RIGHT/LEFT
          RIGHT: DNodes 1,2, 5,6, 9,10, ...
          LEFT: DNodes 3,4, 7,8, 11,12, ...
        """
        right_dns = []
        left_dns = []
        
        if dbox_type == 'CeresV1':
            # CeresV1: ODD → RIGHT, EVEN → LEFT
            for dn_num in range(1, dn_count + 1):
                if dn_num % 2 == 1:  # ODD → RIGHT
                    right_dns.append(dn_num)
                else:  # EVEN → LEFT
                    left_dns.append(dn_num)
        else:
            # CeresV2 or Mav: Groups of 2, alternating RIGHT/LEFT
            # Group 1 (1,2) → RIGHT, Group 2 (3,4) → LEFT, Group 3 (5,6) → RIGHT, etc.
            for dn_num in range(1, dn_count + 1):
                # Group number (1-based): (dn_num - 1) // 2 + 1
                group_num = (dn_num - 1) // 2 + 1
                if group_num % 2 == 1:  # Odd groups (1,3,5...) → RIGHT
                    right_dns.append(dn_num)
                else:  # Even groups (2,4,6...) → LEFT
                    left_dns.append(dn_num)
        
        return left_dns, right_dns

    def _calculate_cell_planning_advanced_ports(self) -> list[tuple[int, str]]:
        """
        Calculate port assignments for Cell Planning Advanced mode.
        """
        # Get port count from current switch
        port_count = self.layout_config.get('PORT_COUNT', 64)
        left_ports, right_ports = self._get_left_right_ports_mellanox(port_count)
        
        port_map = []
        assigned = set()
        
        # Get node counts
        dn_count = safe_int(self.cell_planning_advanced_dn_count.text(), 0)
        node_counts = {}
        for nt, widget in self.cell_planning_advanced_node_counts.items():
            node_counts[nt] = safe_int(widget.text(), 0)
        
        # Get starting node values
        dn_starting_node = 100  # Default
        if hasattr(self, 'cell_planning_advanced_node_widgets') and 'DN' in self.cell_planning_advanced_node_widgets:
            dn_starting_widget = self.cell_planning_advanced_node_widgets['DN'].get('starting_node')
            if dn_starting_widget:
                dn_starting_node = safe_int(dn_starting_widget.text(), 100)
        
        node_starting_nodes = {}
        for nt in ['CN', 'EB', 'IE', 'GN']:
            node_starting_nodes[nt] = 1  # Default
            if hasattr(self, 'cell_planning_advanced_node_widgets') and nt in self.cell_planning_advanced_node_widgets:
                nt_starting_widget = self.cell_planning_advanced_node_widgets[nt].get('starting_node')
                if nt_starting_widget:
                    node_starting_nodes[nt] = safe_int(nt_starting_widget.text(), 1)
        
        # Track current indices for left and right sides
        left_current_index = 0
        right_current_index = 0
        
        # DN assignment: Based on DBox type
        dbox_type = self.cell_planning_advanced_config['dbox_type']
        if dn_count > 0:
            dn_split = self.cell_planning_advanced_dn_split_cb.isChecked()
            dn_factor = safe_int(self.cell_planning_advanced_dn_factor.currentText(), 2)
            
            # Get DNode groups based on DBox type
            left_dns, right_dns = self._get_dnode_groups_by_dbox_type(dn_count, dbox_type)
            
            # Assign DNs to LEFT side
            if dn_split and dn_factor > 1:
                # Port splitting: take first N DNs from left_dns list for each port
                left_idx = 0
                while left_idx < len(left_dns) and left_current_index < len(left_ports):
                    # Take next dn_factor DNs from the left_dns list
                    dns_for_port = left_dns[left_idx:left_idx + dn_factor]
                    if len(dns_for_port) == 1:
                        # Calculate actual node number: starting_node + dn_num - 1 (since dn_num is 1-based)
                        actual_node = dn_starting_node + dns_for_port[0] - 1
                        label = f'DN-{actual_node}'
                    else:
                        # Calculate actual node numbers for range
                        start_actual = dn_starting_node + dns_for_port[0] - 1
                        end_actual = dn_starting_node + dns_for_port[-1] - 1
                        label = f'DN-{start_actual}/{end_actual}'
                    
                    port = left_ports[left_current_index]
                    port_map.append((port, label))
                    assigned.add(port)
                    left_current_index += 1
                    left_idx += len(dns_for_port)
            else:
                # No splitting: one DN per port
                for dn_num in left_dns:
                    if left_current_index < len(left_ports):
                        # Calculate actual node number: starting_node + dn_num - 1 (since dn_num is 1-based)
                        actual_node = dn_starting_node + dn_num - 1
                        port = left_ports[left_current_index]
                        port_map.append((port, f'DN-{actual_node}'))
                        assigned.add(port)
                        left_current_index += 1
            
            # Assign DNs to RIGHT side
            if dn_split and dn_factor > 1:
                # Port splitting: take first N DNs from right_dns list for each port
                right_idx = 0
                while right_idx < len(right_dns) and right_current_index < len(right_ports):
                    # Take next dn_factor DNs from the right_dns list
                    dns_for_port = right_dns[right_idx:right_idx + dn_factor]
                    if len(dns_for_port) == 1:
                        # Calculate actual node number: starting_node + dn_num - 1 (since dn_num is 1-based)
                        actual_node = dn_starting_node + dns_for_port[0] - 1
                        label = f'DN-{actual_node}'
                    else:
                        # Calculate actual node numbers for range
                        start_actual = dn_starting_node + dns_for_port[0] - 1
                        end_actual = dn_starting_node + dns_for_port[-1] - 1
                        label = f'DN-{start_actual}/{end_actual}'
                    
                    port = right_ports[right_current_index]
                    port_map.append((port, label))
                    assigned.add(port)
                    right_current_index += 1
                    right_idx += len(dns_for_port)
            else:
                # No splitting: one DN per port
                for dn_num in right_dns:
                    if right_current_index < len(right_ports):
                        # Calculate actual node number: starting_node + dn_num - 1 (since dn_num is 1-based)
                        actual_node = dn_starting_node + dn_num - 1
                        port = right_ports[right_current_index]
                        port_map.append((port, f'DN-{actual_node}'))
                        assigned.add(port)
                        right_current_index += 1
        
        # Assign other node types based on routing preferences
        for nt in ['CN', 'EB', 'IE', 'GN']:
            count = node_counts.get(nt, 0)
            if count == 0:
                continue
            
            # Get routing preference
            routing_pref = 'RIGHT'  # Default
            if nt in self.cell_planning_advanced_routing_widgets:
                nt_widgets = self.cell_planning_advanced_routing_widgets[nt]
                if nt_widgets.get('left', QRadioButton()).isChecked():
                    routing_pref = 'LEFT'
            
            # Get split settings
            split_cb = self.cell_planning_advanced_node_splits[nt]['split_cb']
            split = split_cb.isChecked()
            factor = safe_int(self.cell_planning_advanced_node_splits[nt]['factor'].currentText(), 2)
            
            # Choose port list based on routing preference
            if routing_pref == 'LEFT':
                current_index = left_current_index
                port_list = left_ports
                index_ref = 'left_current_index'
            else:
                current_index = right_current_index
                port_list = right_ports
                index_ref = 'right_current_index'
            
            # Assign ports
            nt_starting = node_starting_nodes.get(nt, 1)
            for i in range(count):
                if split:
                    # Port splitting
                    if i % factor == 0:
                        end_idx = min(i + factor - 1, count - 1)
                        # Calculate actual node numbers: starting_node + i (since i is 0-based)
                        start_actual = nt_starting + i
                        end_actual = nt_starting + end_idx
                        label = f'{nt}-{start_actual}/{end_actual}'
                    else:
                        continue  # Skip intermediate nodes in split groups
                else:
                    # Calculate actual node number: starting_node + i (since i is 0-based)
                    actual_node = nt_starting + i
                    label = f'{nt}-{actual_node}'
                
                if current_index < len(port_list):
                    port = port_list[current_index]
                    port_map.append((port, label))
                    assigned.add(port)
                    current_index += 1
            
            # Update the appropriate index
            if routing_pref == 'LEFT':
                left_current_index = current_index
            else:
                right_current_index = current_index
        
        # Assign uplinks (from right side, remaining ports)
        # Preferred starting ports: 56, 52, 48, 44, 40, 36, 32, 28, 24, 18, 14, or 10
        # But only if the LOW end doesn't conflict with LEFT-side CN/DN ports
        # Try to balance open ports on BOTH sides of the uplink ports for better layout
        uplink_labels = []
        
        # Collect all left-side assigned ports (CN/DN on LEFT)
        left_assigned_ports = set()
        for port, label in port_map:
            if port in left_ports:
                left_assigned_ports.add(port)
        
        # Find the highest and lowest node ports (DN, CN, NB, etc.) on BOTH sides
        # This helps us balance spacing on both sides of the uplink GROUP
        all_node_ports = []
        for port, label in port_map:
            # Check if it's a node port (DN, CN, NB, etc.) on either side
            if any(label.startswith(f'{nt}-') for nt in ['DN', 'CN', 'NB', 'EB', 'IE', 'GN']):
                all_node_ports.append(port)
        
        highest_node_port = max(all_node_ports) if all_node_ports else None
        lowest_node_port = min(all_node_ports) if all_node_ports else None
        
        # Calculate total uplink ports needed
        total_uplink_ports = 0
        uplink_configs = []
        for ut in ['IPL', 'ISL', 'EXT']:
            groups_widget = self.cell_planning_advanced_uplink_widgets[ut]['groups']
            ppg_widget = self.cell_planning_advanced_uplink_widgets[ut]['ppg']
            
            groups = safe_int(groups_widget.text(), 0)
            ppg = safe_int(ppg_widget.text(), 0)
            
            if groups == 0 or ppg == 0:
                continue
            
            # IPL is always 1 group
            if ut == 'IPL':
                groups = 1
            
            total_ports_for_type = groups * ppg
            total_uplink_ports += total_ports_for_type
            uplink_configs.append((ut, groups, ppg))
        
        # Preferred starting ports (high to low)
        preferred_start_ports = [56, 52, 48, 44, 40, 36, 32, 28, 24, 18, 14, 10]
        
        # Strategy: Try to balance spacing on both sides of uplinks
        # If we have node ports on both sides, try to center the uplinks between them
        if total_uplink_ports > 0:
            balanced_start_port = None
            
            # Calculate balanced placement if we have node ports on both sides
            if highest_node_port is not None and lowest_node_port is not None:
                # Calculate the center point between highest and lowest node ports
                center_between_nodes = (highest_node_port + lowest_node_port) / 2.0
                
                # Calculate where uplinks should start to be centered around this point
                # The center of the uplink block should be at center_between_nodes
                # If we have N uplink ports, the center port is at start_port - (N-1)/2
                # So: start_port - (N-1)/2 = center_between_nodes
                # Therefore: start_port = center_between_nodes + (N-1)/2
                ideal_start_port = int(round(center_between_nodes + (total_uplink_ports - 1) / 2.0))
                
                # First, try to find the best balanced position (not just from preferred ports)
                # Search around the ideal position to find the best balance
                best_balance_score = None
                best_start_port = None
                best_gap_high = None
                best_gap_low = None
                
                # Get port count to know max port number
                port_count = self.layout_config.get('PORT_COUNT', 64)
                max_port = port_count
                
                # Search in a reasonable range around ideal position
                search_range = max(30, total_uplink_ports * 5)  # Search very wide range
                for candidate_start in range(max(1, ideal_start_port - search_range), min(max_port + 1, ideal_start_port + search_range + 1)):
                    candidate_lowest = candidate_start - total_uplink_ports + 1
                    if candidate_lowest < 1:
                        continue
                    
                    # Check if all ports in range are available and don't conflict with left-side
                    all_available = True
                    conflicts_with_left = False
                    for i in range(total_uplink_ports):
                        port = candidate_start - i
                        if port in assigned:
                            all_available = False
                            break
                        if port in left_assigned_ports:
                            conflicts_with_left = True
                            break
                    
                    if all_available and not conflicts_with_left:
                        # Calculate gaps on both sides of the uplink GROUP
                        # Gap above: count unassigned ports between highest node port and highest uplink port
                        gap_high_side = 0
                        if candidate_start < highest_node_port:
                            # Uplink GROUP is below highest node port - count unassigned ports between them
                            for p in range(candidate_start + 1, highest_node_port):
                                if p not in assigned and p not in left_assigned_ports:
                                    gap_high_side += 1
                        elif candidate_start > highest_node_port:
                            # Uplink GROUP is above highest node port - count unassigned ports in between
                            for p in range(highest_node_port + 1, candidate_start):
                                if p not in assigned and p not in left_assigned_ports:
                                    gap_high_side += 1
                        
                        # Gap below: count unassigned ports between lowest uplink port and lowest node port
                        gap_low_side = 0
                        if candidate_lowest > lowest_node_port:
                            # Uplink GROUP is above lowest node port - count unassigned ports between them
                            for p in range(lowest_node_port + 1, candidate_lowest):
                                if p not in assigned and p not in left_assigned_ports:
                                    gap_low_side += 1
                        elif candidate_lowest < lowest_node_port:
                            # Uplink GROUP is below lowest node port - count unassigned ports in between
                            for p in range(candidate_lowest + 1, lowest_node_port):
                                if p not in assigned and p not in left_assigned_ports:
                                    gap_low_side += 1
                        
                        # Calculate balance score: lower difference = more balanced
                        # This balances unassigned ports between the uplink GROUP and node ports on both sides
                        balance_score = abs(gap_high_side - gap_low_side)
                        
                        # Also factor in distance from ideal (but balance is more important)
                        distance_from_ideal = abs(candidate_start - ideal_start_port)
                        
                        # Combined score: balance is MUCH more important (weight it heavily)
                        combined_score = balance_score * 1000 + distance_from_ideal
                        
                        if best_balance_score is None or combined_score < best_balance_score:
                            best_balance_score = combined_score
                            best_start_port = candidate_start
                            best_gap_high = gap_high_side
                            best_gap_low = gap_low_side
                
                # ALWAYS use the best balanced position if found (don't filter it out)
                if best_start_port is not None:
                    balanced_start_port = best_start_port
                    # Debug: We found the best balanced position
                    # It will be used regardless of gap ratios
            
            # If we found a balanced placement, use it
            if balanced_start_port is not None:
                uplink_port_list = []
                for i in range(total_uplink_ports):
                    uplink_port_list.append(balanced_start_port - i)
                
                port_idx = 0
                for ut, groups, ppg in uplink_configs:
                    for group_num in range(1, groups + 1):
                        for port_num in range(1, ppg + 1):
                            if port_idx < len(uplink_port_list):
                                port = uplink_port_list[port_idx]
                                label = f'{ut}{group_num}-{port_num}'
                                uplink_labels.append((port, label))
                                assigned.add(port)
                                port_idx += 1
            
            # If balanced placement didn't work, try preferred ports (but still check balance)
            if len(uplink_labels) == 0:
                # Try preferred ports, but prioritize balance
                best_preferred_score = None
                best_preferred_port = None
                
                for preferred_port in preferred_start_ports:
                    if preferred_port in assigned:
                        continue
                    
                    # Calculate the lowest port we'll use
                    lowest_uplink_port = preferred_port - total_uplink_ports + 1
                    # Check if lowest port conflicts with left-side CN/DN ports
                    conflicts_with_left = False
                    if lowest_uplink_port in left_assigned_ports:
                        conflicts_with_left = True
                    else:
                        # Check all ports in the range for conflicts with left-side ports
                        for i in range(total_uplink_ports):
                            port = preferred_port - i
                            if port in left_assigned_ports:
                                conflicts_with_left = True
                                break
                    
                    if not conflicts_with_left:
                        # Check if all ports in the range are available (not already assigned)
                        all_available = True
                        uplink_port_list = []
                        for i in range(total_uplink_ports):
                            port = preferred_port - i
                            if port in assigned:
                                all_available = False
                                break
                            uplink_port_list.append(port)
                        
                        if all_available:
                            # Calculate balance score for this preferred port
                            if highest_node_port is not None and lowest_node_port is not None:
                                # Count unassigned ports in gaps
                                gap_high = 0
                                if preferred_port < highest_node_port:
                                    for p in range(preferred_port + 1, highest_node_port):
                                        if p not in assigned and p not in left_assigned_ports:
                                            gap_high += 1
                                elif preferred_port > highest_node_port:
                                    for p in range(highest_node_port + 1, preferred_port):
                                        if p not in assigned and p not in left_assigned_ports:
                                            gap_high += 1
                                
                                gap_low = 0
                                if lowest_uplink_port > lowest_node_port:
                                    for p in range(lowest_node_port + 1, lowest_uplink_port):
                                        if p not in assigned and p not in left_assigned_ports:
                                            gap_low += 1
                                elif lowest_uplink_port < lowest_node_port:
                                    for p in range(lowest_uplink_port + 1, lowest_node_port):
                                        if p not in assigned and p not in left_assigned_ports:
                                            gap_low += 1
                                
                                balance_score = abs(gap_high - gap_low)
                            else:
                                balance_score = 0
                            
                            if best_preferred_score is None or balance_score < best_preferred_score:
                                best_preferred_score = balance_score
                                best_preferred_port = preferred_port
                
                # Use the best balanced preferred port if found
                if best_preferred_port is not None:
                    port_idx = 0
                    for ut, groups, ppg in uplink_configs:
                        for group_num in range(1, groups + 1):
                            for port_num in range(1, ppg + 1):
                                if port_idx < total_uplink_ports:
                                    port = best_preferred_port - port_idx
                                    label = f'{ut}{group_num}-{port_num}'
                                    uplink_labels.append((port, label))
                                    assigned.add(port)
                                    port_idx += 1
        
        # If preferred ports couldn't be used, fall back to sequential assignment
        # Try to balance spacing when possible, but assign anyway if can't
        if len(uplink_labels) == 0:
            # Try to find a balanced placement in available ports
            if highest_node_port is not None and lowest_node_port is not None:
                # Calculate ideal balanced position - center the uplink GROUP between node ports
                center_between_nodes = (highest_node_port + lowest_node_port) / 2.0
                ideal_start_port = int(round(center_between_nodes + (total_uplink_ports - 1) / 2.0))
                
                # Try ideal position first
                ideal_lowest = ideal_start_port - total_uplink_ports + 1
                ideal_available = True
                
                # Check if ideal position is available
                if ideal_start_port in assigned or ideal_lowest in assigned:
                    ideal_available = False
                else:
                    for i in range(total_uplink_ports):
                        port = ideal_start_port - i
                        if port in assigned or port in left_assigned_ports:
                            ideal_available = False
                            break
                
                if ideal_available:
                    # Use balanced placement at ideal position
                    port_idx = 0
                    for ut, groups, ppg in uplink_configs:
                        for group_num in range(1, groups + 1):
                            for port_num in range(1, ppg + 1):
                                if port_idx < total_uplink_ports:
                                    port = ideal_start_port - port_idx
                                    label = f'{ut}{group_num}-{port_num}'
                                    uplink_labels.append((port, label))
                                    assigned.add(port)
                                    port_idx += 1
                else:
                    # Try ports near ideal position for balanced placement
                    best_balance_score = None
                    best_port = None
                    
                    # Search in a range around ideal position
                    search_range = max(10, total_uplink_ports * 2)  # Search reasonable range
                    for candidate_start in range(ideal_start_port - search_range, ideal_start_port + search_range + 1):
                        if candidate_start in assigned:
                            continue
                        
                        candidate_lowest = candidate_start - total_uplink_ports + 1
                        if candidate_lowest < 1:
                            continue
                        
                        # Check if all ports in range are available
                        all_available = True
                        for i in range(total_uplink_ports):
                            port = candidate_start - i
                            if port in assigned or port in left_assigned_ports:
                                all_available = False
                                break
                        
                        if all_available:
                            # Calculate balance score - count unassigned ports in gaps
                            gap_high = 0
                            if candidate_start < highest_node_port:
                                for p in range(candidate_start + 1, highest_node_port):
                                    if p not in assigned and p not in left_assigned_ports:
                                        gap_high += 1
                            elif candidate_start > highest_node_port:
                                for p in range(highest_node_port + 1, candidate_start):
                                    if p not in assigned and p not in left_assigned_ports:
                                        gap_high += 1
                            
                            gap_low = 0
                            if candidate_lowest > lowest_node_port:
                                for p in range(lowest_node_port + 1, candidate_lowest):
                                    if p not in assigned and p not in left_assigned_ports:
                                        gap_low += 1
                            elif candidate_lowest < lowest_node_port:
                                for p in range(candidate_lowest + 1, lowest_node_port):
                                    if p not in assigned and p not in left_assigned_ports:
                                        gap_low += 1
                            
                            balance_score = abs(gap_high - gap_low)
                            distance_from_ideal = abs(candidate_start - ideal_start_port)
                            combined_score = balance_score * 1000 + distance_from_ideal
                            
                            if best_balance_score is None or combined_score < best_balance_score:
                                best_balance_score = combined_score
                                best_port = candidate_start
                    
                    if best_port is not None:
                        # Use best balanced position found
                        port_idx = 0
                        for ut, groups, ppg in uplink_configs:
                            for group_num in range(1, groups + 1):
                                for port_num in range(1, ppg + 1):
                                    if port_idx < total_uplink_ports:
                                        port = best_port - port_idx
                                        label = f'{ut}{group_num}-{port_num}'
                                        uplink_labels.append((port, label))
                                        assigned.add(port)
                                        port_idx += 1
            
            # If balanced placement didn't work, assign sequentially
            if len(uplink_labels) == 0:
                for ut, groups, ppg in uplink_configs:
                    for group_num in range(1, groups + 1):
                        for port_num in range(1, ppg + 1):
                            # Find next available port from right side
                            while right_current_index < len(right_ports) and right_ports[right_current_index] in assigned:
                                right_current_index += 1
                            
                            if right_current_index < len(right_ports):
                                port = right_ports[right_current_index]
                                label = f'{ut}{group_num}-{port_num}'
                                uplink_labels.append((port, label))
                                assigned.add(port)
                                right_current_index += 1
        
        port_map.extend(uplink_labels)
        
        return sorted(port_map, key=lambda x: x[0])

    def _draw_cell_planning_advanced_preview(self):
        """Draw live preview for Cell Planning Advanced mode."""
        if not self.cell_planning_advanced_port_map:
            if hasattr(self, 'cell_planning_advanced_canvas_a'):
                self.cell_planning_advanced_canvas_a.setText('No ports assigned')
                self.cell_planning_advanced_canvas_b.setText('No ports assigned')
            return
        
        try:
            df_raw = pd.DataFrame(self.cell_planning_advanced_port_map, columns=['Port ID', 'Port Name'])
            df_agg = df_raw.groupby('Port ID')['Port Name'].apply(lambda s: s.iloc[0]).reset_index()
            
            scale_a = self.cell_planning_advanced_canvas_a.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.cell_planning_advanced_canvas_a.width() > 0 else 1.0
            dfA = df_agg.copy()
            dfA['Fabric ID'] = 'A'
            dfA['Hostname'] = 'SwitchA'
            imgA = self._draw_overlay(dfA, self.base_image, self.layout_config, display_scale=scale_a)
            self.cell_planning_advanced_canvas_a.setPixmap(pil_to_qpixmap(imgA))
            
            scale_b = self.cell_planning_advanced_canvas_b.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.cell_planning_advanced_canvas_b.width() > 0 else 1.0
            dfB = df_agg.copy()
            dfB['Fabric ID'] = 'B'
            dfB['Hostname'] = 'SwitchB'
            imgB = self._draw_overlay(dfB, self.base_image, self.layout_config, display_scale=scale_b)
            self.cell_planning_advanced_canvas_b.setPixmap(pil_to_qpixmap(imgB))
        except Exception as e:
            if hasattr(self, 'cell_planning_advanced_canvas_a'):
                self.cell_planning_advanced_canvas_a.setText(f'Error: {str(e)}')
                self.cell_planning_advanced_canvas_b.setText(f'Error: {str(e)}')

    def _on_cell_planning_advanced_clone_to_multi_rack_go(self):
        """Clone Advanced mode configuration to multi-rack design."""
        # This will be implemented in step 3 - for now, just call the main clone function with mode flag
        # We'll modify _on_clone_to_multi_rack_go to handle both modes
        self._on_clone_to_multi_rack_go(mode='advanced')

    def _build_uplink_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("DarkTab")
        main_layout = QVBoxLayout(main_widget)

        input_group = QGroupBox('Configure Uplink Groups')
        input_group_layout = QVBoxLayout(input_group)
        
        # Add switch type label at the top
        switch_label = QLabel()
        switch_label.setWordWrap(True)
        switch_label.setStyleSheet("""
            QLabel {
                background-color: #FFF3E0;
                color: #E65100;
                padding: 4px;
                border-radius: 3px;
                border: 1px solid #FFB74D;
                font-size: 10pt;
                font-weight: bold;
            }
        """)
        input_group_layout.addWidget(switch_label)
        self.uplink_switch_label = switch_label
        
        grid = QGridLayout()
        input_group_layout.addLayout(grid)

        uplink_descriptions = {
            'IPL': 'The number of Inter-Peer Link ports between leaf pairs.',
            'ISL': 'The number of Inter-Switch Link groups, and ports per group to/from Leafs And Spines.',
            'MLAG/BGP': 'The number of uplink groups and ports per group to customer gear.',
            'NB': 'The number of Cnode/Ebox 2nd NIC Northbound ports per fabric.'
        }

        headers = ['Uplink\nType', '# Of Uplink\nChannels', 'Ports\nPer Group', 'Split\nPorts?', 'Split\nValue', 'Reserved\nPort Count', 'Manual\nInput', 'Assigned\nPorts', 'Suggestion']
        for i, h in enumerate(headers):
            label = QLabel(h)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Set tooltip for each header
            if h == '# Of Uplink\nChannels':
                label.setToolTip('Number of uplink destinations being spines (ISLs) or customer switches (MLAG or BGP). Each uplink gets its ports defined in \'Ports/Group\'')
            elif h == 'Suggestion':
                label.setToolTip('Recommended ports per group for non-blocking fabric based on Max BW Required Per Cell')
            else:
                # Use uplink type descriptions for other headers
                label.setToolTip(uplink_descriptions.get(h.split('\n')[0], ''))
            grid.addWidget(label, 0, i)

        self.uplink_types = ['IPL', 'ISL', 'MLAG/BGP', 'NB']
        if not hasattr(self, 'uplink_suggestion_labels'):
            self.uplink_suggestion_labels = {}  # Store suggestion labels for each uplink type

        for r, ut in enumerate(self.uplink_types, 1):
            self._create_port_config_row(grid, r, ut, uplink_descriptions.get(ut, ''), is_node_tab=False)
            # For IPL and NB, the group count is always 1 and should be disabled.
            if ut in ['IPL', 'NB']:
                gcnt_widget = self.uplink_entries[ut]['gcnt']
                gcnt_widget.setText('1')
                gcnt_widget.setEnabled(False)
                # Style disabled field to appear grey so user knows not to edit it
                gcnt_widget.setStyleSheet("QLineEdit:disabled { background-color: #555555; color: #AAAAAA; }")
            
            # Add event handlers for IPL/ISL mutual exclusion
            if ut in ['IPL', 'ISL']:
                self.uplink_entries[ut]['ppg'].textChanged.connect(self._on_uplink_count_changed)
            
            # Add suggestion label for ISL and MLAG/BGP (shown as EXT in UI)
            if ut in ['ISL', 'MLAG/BGP']:
                suggestion_label = QLabel('')
                suggestion_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                suggestion_label.setWordWrap(False)
                suggestion_label.setStyleSheet("QLabel { padding-left: 10px; min-width: 200px; }")
                grid.addWidget(suggestion_label, r, 8)
                # Store with suffix to differentiate from Uplinks tab labels
                # Use EXT as the key for MLAG/BGP in the suggestion labels dictionary
                key_suffix = 'EXT' if ut == 'MLAG/BGP' else ut
                self.uplink_suggestion_labels[key_suffix + '_uplink_tab'] = suggestion_label

        grid.setColumnStretch(9, 1) # Add stretch to the right of all content (was column 8, now 9)

        main_layout.addWidget(input_group)
        
        # Initialize leaf/spine logic after uplink entries are created
        self._on_leaf_spine_changed(self.leaf_spine_combo.currentText())
        
        # Initialize NB port configuration based on 2nd NIC and unified networking settings
        self._populate_cn_eb_nb_from_cnodes()

        # Live Preview Area (Assign button removed - auto-assignment happens as you type)
        self.uplink_live_preview_label = QLabel()
        main_layout.addWidget(self.uplink_live_preview_label)
        self.uplink_canvas_a = ScalableLabel("Fabric A Preview")
        self.uplink_canvas_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uplink_canvas_a.setFrameShape(QFrame.Shape.StyledPanel)
        self.uplink_canvas_a.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.uplink_canvas_b = ScalableLabel("Fabric B Preview")
        self.uplink_canvas_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.uplink_canvas_b.setFrameShape(QFrame.Shape.StyledPanel)
        self.uplink_canvas_b.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # Create a container widget for the vertically stacked previews
        previews_container = QWidget()
        previews_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        previews_vbox = QVBoxLayout(previews_container)
        previews_vbox.setContentsMargins(0, 0, 0, 0)
        previews_vbox.addWidget(self.uplink_canvas_b)
        previews_vbox.addWidget(self.uplink_canvas_a)

        # Use a horizontal layout to constrain the width of the container to 95%
        previews_hbox = QHBoxLayout()
        previews_hbox.addStretch(5)  # 2.5% margin
        previews_hbox.addWidget(previews_container, 190)  # Container takes 95%
        previews_hbox.addStretch(5)  # 2.5% margin
        main_layout.addLayout(previews_hbox)

        return main_widget

    def _build_help_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(convert_help_to_html(HELP_TEXT))
        layout.addWidget(text_edit)
        return main_widget

    def _build_multi_rack_ui(self):
        """Builds the UI for the new Multi-Rack tab."""
        main_widget = QWidget()
        main_widget.setObjectName("DarkTab")
        main_layout = QHBoxLayout(main_widget)

        # --- Left Panel: Rack List and Controls ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(200)

        rack_list_label = QLabel("Racks, Click To Edit")
        self.rack_list_widget = QListWidget()
        self.rack_list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)  # Allow multiple selection
        self.rack_list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.rack_list_widget.itemDoubleClicked.connect(self._on_rack_item_double_clicked)
        self.rack_list_widget.currentItemChanged.connect(self._on_rack_selected)
        # Connect a handler to commit the data when the editor closes (e.g., on Enter or focus loss)
        self.rack_list_widget.itemDelegate().commitData.connect(self._on_rack_rename_committed)


        button_layout = QHBoxLayout()
        self.add_rack_button = QPushButton("Add")
        self.add_rack_button.clicked.connect(self._on_add_rack_clicked)
        self.remove_rack_button = QPushButton("Remove")
        self.remove_rack_button.clicked.connect(self._on_remove_rack_clicked)
        self.clone_rack_button = QPushButton("Clone Rack")
        self.clone_rack_button.clicked.connect(self._on_clone_rack_clicked)

        button_layout.addWidget(self.add_rack_button)
        button_layout.addWidget(self.remove_rack_button)

        left_layout.addWidget(rack_list_label)
        left_layout.addWidget(self.rack_list_widget)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(self.clone_rack_button)

        # --- Right Panel: Configuration Details + Preview ---
        right_panel_container = QWidget()
        right_panel_main_layout = QVBoxLayout(right_panel_container)

        # --- Right Panel: Configuration Details ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.rack_details_stack = QStackedLayout()

        # Create a default empty widget for when no rack is selected
        self.empty_details_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_details_widget)
        empty_label = QLabel("Select or add a rack to configure it.")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(empty_label)
        self.rack_details_stack.addWidget(self.empty_details_widget)

        right_layout.addLayout(self.rack_details_stack)

        # --- Right Panel: Preview Area ---
        preview_group = QGroupBox("Live Rack Preview")
        preview_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        preview_layout = QHBoxLayout(preview_group)

        self.multi_rack_canvas_a = ScalableLabel("Fabric A Preview")
        self.multi_rack_canvas_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.multi_rack_canvas_a.setFrameShape(QFrame.Shape.StyledPanel)
        self.multi_rack_canvas_a.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.multi_rack_canvas_b = ScalableLabel("Fabric B Preview")
        self.multi_rack_canvas_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.multi_rack_canvas_b.setFrameShape(QFrame.Shape.StyledPanel)
        self.multi_rack_canvas_b.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        preview_layout.addWidget(self.multi_rack_canvas_b)
        preview_layout.addWidget(self.multi_rack_canvas_a)

        # Assemble the right panel
        right_panel_main_layout.addWidget(right_panel)
        right_panel_main_layout.addWidget(preview_group)
        # The preview group should take up most of the vertical space
        right_panel_main_layout.setStretch(0, 2) # Config section (taller)
        right_panel_main_layout.setStretch(1, 1) # Preview section (shorter)

        # --- Assembly --- (Assign Racks button removed - racks auto-save as you configure)
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel_container)

        return main_widget

    def _add_rack(self, new_rack_name=None, source_rack_data=None):
        """Adds a new rack to the list and data model."""
        # If a specific name is provided (from cloning), use it. Otherwise, generate one.
        if new_rack_name is None:
            new_rack_name = self._get_next_rack_name()

        if source_rack_data:
            # Deep copy the source data for the new rack
            import copy
            self.multi_rack_config[new_rack_name] = copy.deepcopy(source_rack_data)
        else:
            # Create default data for a new rack
            nodes_data = {nt: self._get_default_node_data() for nt in self.node_types}
            
            # Calculate starting node numbers based on existing racks
            default_starting_numbers = {'DN': 100, 'CN': 1, 'EB': 1, 'IE': 1, 'GN': 1}
            
            # Extract base rack name (without number)
            base_rack_name = new_rack_name.rsplit(' ', 1)[0] if ' ' in new_rack_name else new_rack_name
            
            # Calculate total node counts from previous racks with same base name
            for node_type in self.node_types:
                total_previous_count = 0
                for existing_rack_name in sorted(self.multi_rack_config.keys()):
                    # Only count racks with the same base name
                    if existing_rack_name.startswith(base_rack_name):
                        existing_rack_data = self.multi_rack_config[existing_rack_name]
                        existing_node_data = existing_rack_data.get('nodes', {}).get(node_type, {})
                        total_previous_count += existing_node_data.get('count', 0)
                
                # Set starting node number
                base_start = default_starting_numbers.get(node_type, 1)
                nodes_data[node_type]['starting_node'] = base_start + total_previous_count
            
            uplinks_data = {ut: self._get_default_uplink_data(ut) for ut in self.uplink_types}
            # Extract the number from the new rack name for default hostnames
            rack_num_str = ''.join(filter(str.isdigit, new_rack_name)) or str(self.rack_list_widget.count() + 1)
            rack_num = int(rack_num_str)
            
            # Get base hostnames from setup tab
            base_hostname_a = self.ha_entry.text().strip()
            base_hostname_b = self.hb_entry.text().strip()
            
            # Get switch_id and peak BW settings from the first rack if it exists, otherwise use global/setup values
            first_rack_switch_id = self.switch_id  # Default fallback
            first_rack_peak_bw_goal = ''
            first_rack_peak_bw_units = 'GB/s'
            
            if self.multi_rack_config:
                # Get the first rack's settings
                first_rack_name = next(iter(self.multi_rack_config))
                first_rack_data = self.multi_rack_config[first_rack_name]
                first_rack_switch_id = first_rack_data.get('switch_id', self.switch_id)
                first_rack_peak_bw_goal = first_rack_data.get('peak_bw_goal', '')
                first_rack_peak_bw_units = first_rack_data.get('peak_bw_units', 'GB/s')
            
            # Create hostnames with rack number prefix
            hostname_a = f'r{rack_num}-{base_hostname_a}' if base_hostname_a else f'r{rack_num}-sw-a'
            hostname_b = f'r{rack_num}-{base_hostname_b}' if base_hostname_b else f'r{rack_num}-sw-b'
            
            self.multi_rack_config[new_rack_name] = {
                'hostname_a': hostname_a,
                'hostname_b': hostname_b,
                'switch_id': first_rack_switch_id, # Use first rack's switch ID
                'mgmt_ip_a': '',
                'mgmt_ip_b': '',
                'peak_bw_goal': first_rack_peak_bw_goal, # Use first rack's peak BW goal
                'peak_bw_units': first_rack_peak_bw_units, # Use first rack's peak BW units
                 'fabric_topology': self.fabric_topology,
                 'use_vxlan_overlay': self.use_vxlan_overlay,
                'nodes': nodes_data,
                'uplinks': uplinks_data
            }
        
        # Update the UI
        self.rack_list_widget.addItem(new_rack_name)
        self._create_rack_detail_widget(new_rack_name)
        self._calculate_and_store_rack_port_map(new_rack_name) # Calculate ports for the new rack
        self.rack_list_widget.setCurrentRow(self.rack_list_widget.count() - 1)

    def _on_rack_double_clicked(self, item: QListWidgetItem):
        """DEPRECATED: This was the old, buggy implementation. It is now replaced by
        _on_rack_item_double_clicked and _on_rack_rename_committed."""
        pass

    def _on_rack_item_double_clicked(self, item: QListWidgetItem):
        """Prepares an item for renaming by storing its original name."""
        self.rack_name_before_edit = item.text()
        # Explicitly make the item editable. This flag is required for the editor to appear.
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.rack_list_widget.editItem(item)

    def _on_rack_rename_committed(self, editor: QWidget):
        """
        Handles the actual rename logic after the editor has finished.
        This is connected to the item delegate's commitData signal.
        """
        if self.rack_name_before_edit is None:
            return # Not in a renaming state

        old_name = self.rack_name_before_edit
        self.rack_name_before_edit = None  # Reset state immediately

        # The editor that just closed is passed as an argument.
        # The new name is its current text.
        new_name = editor.text().strip()
        # The currently selected item in the list is the one that was just edited.
        item = self.rack_list_widget.currentItem()

        # --- Validation ---
        if not new_name:
            QMessageBox.warning(self, "Invalid Name", "Rack name cannot be empty.")
            if item: item.setText(old_name) # Revert UI
            return

        if new_name == old_name:
            return # No change

        if new_name in self.multi_rack_config:
            QMessageBox.warning(self, "Invalid Name", f"A rack named '{new_name}' already exists.")
            if item: item.setText(old_name) # Revert UI
            return

        # --- Update Data Structures ---
        # Update the main configuration dictionary
        self.multi_rack_config[new_name] = self.multi_rack_config.pop(old_name)

        # Remove the old widget from the cache and stacked layout
        if old_name in self.rack_widgets:
            old_widget_data = self.rack_widgets.pop(old_name)
            # Remove the old widget from the stacked layout if it exists
            if old_widget_data and 'widget' in old_widget_data:
                old_widget = old_widget_data['widget']
                self.rack_details_stack.removeWidget(old_widget)
                old_widget.deleteLater()

        # Recreate the widget with the new rack name
        self._create_rack_detail_widget(new_name)

        # If the renamed rack was the currently selected one, update the tracking variable
        if self.current_rack_name == old_name:
            self.current_rack_name = new_name
            # Force the stacked widget to show the new widget
            if new_name in self.rack_widgets:
                new_widget = self.rack_widgets[new_name]['widget']
                self.rack_details_stack.setCurrentWidget(new_widget)

    def _on_assign_racks_clicked(self):
        """Finalizes all rack configurations and switches to the Output tab (deprecated - racks auto-save now)."""
        # Racks now auto-save as you configure, so this just navigates to output
        # Recalculate and store the final port map for every rack
        for rack_name in self.multi_rack_config:
            self._calculate_and_store_rack_port_map(rack_name)

        # Clear dirty state and update indicators
        self.multi_rack_dirty = False
        if self.multi_rack_tab_index != -1:
            self._update_tab_badge(self.multi_rack_tab_index, False, 'Multi-Rack')
        
        self._show_timed_messagebox('Success', f'✓ All {len(self.multi_rack_config)} rack configurations ready', timeout=1000)

        # Switch to the output tab to view the results
        self.notebook.setCurrentIndex(self.notebook.indexOf(self.output_tab))

    def _get_next_rack_name(self) -> str:
        """Generates the next available default rack name based on the leaf/spine setting."""
        rack_type = self.leaf_spine_combo.currentText().capitalize() # "Leaf" or "Spine"
        rack_num = 1
        # Find the next available number for this rack type
        while f"{rack_type} Rack {rack_num}" in self.multi_rack_config:
            rack_num += 1
        return f"{rack_type} Rack {rack_num}"

    def _get_default_node_data(self):
        """Returns default node data including starting_node defaults."""
        default_starting_numbers = {
            'DN': 100,
            'CN': 1,
            'EB': 1,
            'IE': 1,
            'GN': 1
        }
        # Note: starting_node should be set per node type when creating racks
        return {'count': 0, 'split': False, 'factor': 2, 'reserved': 0, 'start': 1, 'starting_node': 1}

    def _get_default_uplink_data(self, uplink_type: str):
        # IPL and NB are always single groups
        groups = 1 if uplink_type in ['IPL', 'NB'] else 0
        return {'groups': groups, 'ports_per_group': 0, 'split': False, 'factor': 2, 'reserved': 0}


    def _sync_main_config_to_rack1(self, field_key: Optional[str], new_value: any):
        """
        Keeps Rack 1's data and UI in sync with the main Setup and Node tabs.
        This method is connected to the signals of the main config widgets.
        """
        # If there are no racks, there's nothing to sync.
        if self.rack_list_widget.count() == 0:
            return

        # Identify the first rack by its position in the list, not by a hardcoded name.
        first_rack_name = self.rack_list_widget.item(0).text()

        # Ensure the identified first rack exists in the data model and widget cache.
        if first_rack_name not in self.multi_rack_config or first_rack_name not in self.rack_widgets:
            return

        # Block signals from the Rack 1 widgets to prevent infinite loops
        # where a change here would trigger the _on_rack_detail_changed signal.
        for widget_group in self.rack_widgets[first_rack_name]['fields'].values():
            if isinstance(widget_group, dict): # This is the 'nodes' group
                for node_widgets in widget_group.values():
                    for widget in node_widgets.values():
                        widget.blockSignals(True)
            else: # Top-level fields
                widget_group.blockSignals(True)

        # Update the data model and UI for Rack 1
        if field_key: # A single field from the Setup tab changed
            self.multi_rack_config[first_rack_name][field_key] = new_value
            if field_key in self.rack_widgets[first_rack_name]['fields']:
                self.rack_widgets[first_rack_name]['fields'][field_key].setText(str(new_value))
        else: # A field on the Node Types tab changed, so we re-sync all node data
            self._initialize_first_rack_from_main_config(force_update=True)

        # Unblock signals
        for widget_group in self.rack_widgets[first_rack_name]['fields'].values():
            if isinstance(widget_group, dict):
                for node_widgets in widget_group.values():
                    for widget in node_widgets.values():
                        widget.blockSignals(False)
            else:
                widget_group.blockSignals(False)

    def _initialize_first_rack_from_main_config(self, force_update=False):
        """Creates the first rack by copying settings from the Setup and Node tabs."""
        # Check if any racks exist
        if self.rack_list_widget.count() > 0:
            if not force_update:
                return # Already initialized
            else:
                # Force update: update the first rack instead of creating a new one
                first_rack_name = self.rack_list_widget.item(0).text()
                if first_rack_name in self.multi_rack_config:
                    # Just update the nodes and uplinks data, keep the rest of the rack config
                    first_rack_data = self.multi_rack_config[first_rack_name]
                    
                    # Gather updated data from the main UI tabs
                    nodes_data = {}
                    for nt, ent in self.node_entries.items():
                        is_locked = ent['lock_cb'].isChecked()
                        manual_ports_str = ent['st'].text().strip() if is_locked else ''
                        nodes_data[nt] = {
                            'count': safe_int(ent['cnt'].text()),
                            'split': ent['split_cb'].isChecked(),
                            'factor': safe_int(ent['fac'].currentText(), 2),
                            'reserved': safe_int(ent['rsv'].text()),
                            'start': 1,
                            'start_port': manual_ports_str if is_locked else '',
                            'manual_ports': manual_ports_str if is_locked else '',
                            'locked': is_locked
                        }

                    uplinks_data = {}
                    for ut, ent in self.uplink_entries.items():
                        is_locked = ent['lock_cb'].isChecked()
                        manual_ports_str = ent['st'].text().strip() if is_locked else ''
                        uplinks_data[ut] = {
                            'groups': safe_int(ent.get('gcnt', QLineEdit('1')).text()),
                            'ports_per_group': safe_int(ent['ppg'].text()),
                            'split': ent['split_cb'].isChecked(),
                            'factor': safe_int(ent['fac'].currentText(), 2),
                            'reserved': safe_int(ent['rsv'].text()),
                            'start': manual_ports_str if is_locked else '',
                            'manual_ports': manual_ports_str if is_locked else '',
                            'locked': is_locked
                        }
                    
                    # Update only nodes and uplinks data
                    first_rack_data['nodes'] = nodes_data
                    first_rack_data['uplinks'] = uplinks_data
                    first_rack_data['fabric_topology'] = self.fabric_topology
                    first_rack_data['use_vxlan_overlay'] = self.use_vxlan_overlay
                    
                    # Recalculate port map for the rack
                    self._calculate_and_store_rack_port_map(first_rack_name)
                    
                    # Refresh the preview if this rack is currently selected
                    if self.current_rack_name == first_rack_name:
                        self._draw_multi_rack_preview()
                    return
        
        # No racks exist, create the first one
        # Gather data from the main UI tabs
        nodes_data = {}
        for nt, ent in self.node_entries.items():
            is_locked = ent['lock_cb'].isChecked()
            manual_ports_str = ent['st'].text().strip() if is_locked else ''
            # Store as start_port for nodes
            nodes_data[nt] = {
                'count': safe_int(ent['cnt'].text()),
                'split': ent['split_cb'].isChecked(),
                'factor': safe_int(ent['fac'].currentText(), 2),
                'reserved': safe_int(ent['rsv'].text()),
                'start': 1, # Start at 1 for the first rack
                'start_port': manual_ports_str if is_locked else '',
                'manual_ports': manual_ports_str if is_locked else '',
                'locked': is_locked
            }

        uplinks_data = {}
        for ut, ent in self.uplink_entries.items():
            is_locked = ent['lock_cb'].isChecked()
            manual_ports_str = ent['st'].text().strip() if is_locked else ''
            # Store as start for uplinks
            uplinks_data[ut] = {
                'groups': safe_int(ent.get('gcnt', QLineEdit('1')).text()),
                'ports_per_group': safe_int(ent['ppg'].text()),
                'split': ent['split_cb'].isChecked(),
                'factor': safe_int(ent['fac'].currentText(), 2),
                'reserved': safe_int(ent['rsv'].text()),
                'start': manual_ports_str if is_locked else '',
                'manual_ports': manual_ports_str if is_locked else '',
                'locked': is_locked
            }

        first_rack_data = {
            'hostname_a': self._generate_rack_hostname(self.ha_entry.text(), 1),
            'hostname_b': self._generate_rack_hostname(self.hb_entry.text(), 1),
            'mgmt_ip_a': self.switch_a_mgmt_ip_entry.text(),
            'mgmt_ip_b': self.switch_b_mgmt_ip_entry.text(),
            'switch_id': self.switch_id, # Inherit from global setting
            'peak_bw_goal': self.peak_bw_goal_entry.text(),
            'peak_bw_units': self.peak_bw_units_combo.currentText(),
            'fabric_topology': self.fabric_topology,
            'use_vxlan_overlay': self.use_vxlan_overlay,
            'nodes': nodes_data,
            'uplinks': uplinks_data
        }

        first_rack_name = self._get_next_rack_name()
        self.multi_rack_config[first_rack_name] = first_rack_data
        self.rack_list_widget.addItem(first_rack_name)
        self._create_rack_detail_widget(first_rack_name)
        self._calculate_and_store_rack_port_map(first_rack_name) # Calculate ports for the initial rack
        self.rack_list_widget.setCurrentRow(0)

    def _on_add_rack_clicked(self):
        """Handles the 'Add Rack' button click."""
        self._add_rack()

    def _on_remove_rack_clicked(self):
        """Removes the selected rack(s)."""
        selected_items = self.rack_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Rack Selected", "Please select rack(s) to remove.")
            return

        # Ensure at least one rack remains
        if self.rack_list_widget.count() - len(selected_items) < 1:
            QMessageBox.warning(self, "Cannot Remove", "At least one rack must exist.")
            return

        # Confirmation message
        if len(selected_items) == 1:
            rack_name = selected_items[0].text()
            msg = f"Are you sure you want to remove '{rack_name}'?"
        else:
            msg = f"Are you sure you want to remove {len(selected_items)} rack(s)?"
        
        reply = QMessageBox.question(self, "Confirm Removal", msg,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            # Process all selected racks
            for item in selected_items:
                rack_name = item.text()
            # Remove from UI list
                self.rack_list_widget.takeItem(self.rack_list_widget.row(item))
            # Remove from data model
            if rack_name in self.multi_rack_config:
                del self.multi_rack_config[rack_name]
            # Remove from widget cache
            if rack_name in self.rack_widgets:
                widget_to_remove = self.rack_widgets[rack_name]['widget']
                self.rack_details_stack.removeWidget(widget_to_remove)
                widget_to_remove.deleteLater()
                del self.rack_widgets[rack_name]

    def _on_rack_selected(self, current_item, previous_item):
        """Shows the detail view for the selected rack."""
        if not current_item:
            self.rack_details_stack.setCurrentWidget(self.empty_details_widget)
            self.current_rack_name = None
            return

        rack_name = current_item.text()
        if rack_name in self.rack_widgets:
            self.rack_details_stack.setCurrentWidget(self.rack_widgets[rack_name]['widget'])
            self.current_rack_name = rack_name
            self._draw_multi_rack_preview()

    def _create_rack_detail_widget(self, rack_name: str):
        """Creates the right-hand panel widget for a specific rack."""
        rack_data = self.multi_rack_config[rack_name]

        # Main container widget for this rack's details
        detail_widget = QWidget()
        detail_widget.setObjectName("DarkTab") # Inherit dark theme
        # Use a scroll area for the details in case they overflow
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; border: none; }")
        detail_content_widget = QWidget()
        layout = QGridLayout(detail_content_widget)
        detail_content_widget.setObjectName("DarkTab") # Inherit dark theme

        # --- General Details ---
        fields = {}
        # Use font metrics to estimate a reasonable pixel width from character count
        avg_char_width = QFontMetrics(self.font()).averageCharWidth()
        hostname_width = avg_char_width * 22 # A bit more than 20 for padding
        ip_width = avg_char_width * 18       # A bit more than 15 for padding

        # Row 0: Hostname A and Mgmt IP A
        layout.addWidget(QLabel("Switch Hostname A:"), 0, 0)
        hostname_a_entry = QLineEdit(str(rack_data.get('hostname_a', '')))
        hostname_a_entry.setFixedWidth(hostname_width)        
        hostname_a_entry.textChanged.connect(lambda text, rn=rack_name, w=hostname_a_entry: self._on_rack_data_changed(rn, ['hostname_a'], w))
        layout.addWidget(hostname_a_entry, 0, 1)
        fields['hostname_a'] = hostname_a_entry

        layout.addWidget(QLabel("Management IP A:"), 0, 2)
        mgmt_ip_a_entry = QLineEdit(str(rack_data.get('mgmt_ip_a', '')))
        mgmt_ip_a_entry.setFixedWidth(ip_width)        
        mgmt_ip_a_entry.textChanged.connect(lambda text, rn=rack_name, w=mgmt_ip_a_entry: self._on_rack_data_changed(rn, ['mgmt_ip_a'], w))
        layout.addWidget(mgmt_ip_a_entry, 0, 3)
        fields['mgmt_ip_a'] = mgmt_ip_a_entry

        # Row 1: Hostname B and Mgmt IP B
        layout.addWidget(QLabel("Switch Hostname B:"), 1, 0)
        hostname_b_entry = QLineEdit(str(rack_data.get('hostname_b', '')))
        hostname_b_entry.setFixedWidth(hostname_width)        
        hostname_b_entry.textChanged.connect(lambda text, rn=rack_name, w=hostname_b_entry: self._on_rack_data_changed(rn, ['hostname_b'], w))
        layout.addWidget(hostname_b_entry, 1, 1)
        fields['hostname_b'] = hostname_b_entry

        layout.addWidget(QLabel("Management IP B:"), 1, 2)
        mgmt_ip_b_entry = QLineEdit(str(rack_data.get('mgmt_ip_b', '')))
        mgmt_ip_b_entry.setFixedWidth(ip_width)        
        mgmt_ip_b_entry.textChanged.connect(lambda text, rn=rack_name, w=mgmt_ip_b_entry: self._on_rack_data_changed(rn, ['mgmt_ip_b'], w))
        layout.addWidget(mgmt_ip_b_entry, 1, 3)
        fields['mgmt_ip_b'] = mgmt_ip_b_entry

        # Row 2: Switch Model and BW Goal
        layout.addWidget(QLabel("Switch Model:"), 2, 0)
        switch_model_combo = QComboBox()
        models = [v['NAME'] for v in SWITCH_LAYOUTS.values()]
        switch_model_combo.addItems(models)
        # Set the current model based on the rack's specific data, falling back to global
        rack_switch_id = rack_data.get('switch_id', self.switch_id)
        rack_switch_name = SWITCH_LAYOUTS[rack_switch_id]['NAME']
        switch_model_combo.setCurrentText(rack_switch_name)
        switch_model_combo.currentTextChanged.connect(lambda text, rn=rack_name: self._on_rack_switch_model_changed(rn, text))
        layout.addWidget(switch_model_combo, 2, 1)
        fields['switch_model'] = switch_model_combo

        layout.addWidget(QLabel("Max BW Required Per Rack/Cell:"), 2, 2)
        bw_goal_layout = QHBoxLayout()
        bw_goal_layout.setSpacing(5)  # Tight spacing between widgets
        bw_goal_entry = QLineEdit(str(rack_data.get('peak_bw_goal', '')))
        bw_goal_entry.setValidator(self.peak_bw_validator)
        bw_goal_entry.setFixedWidth(60)  # Limit to 6 characters
        bw_goal_entry.textChanged.connect(lambda text, rn=rack_name, w=bw_goal_entry: self._on_rack_data_changed(rn, ['peak_bw_goal'], w))
        bw_goal_entry.textChanged.connect(self._update_uplink_suggestions)
        bw_goal_layout.addWidget(bw_goal_entry)
        bw_units_combo = QComboBox()
        bw_units_combo.addItems(['GB/s', 'GiB/s'])
        bw_units_combo.setCurrentText(rack_data.get('peak_bw_units', 'GB/s'))
        bw_units_combo.currentTextChanged.connect(lambda text, rn=rack_name, w=bw_units_combo: self._on_rack_data_changed(rn, ['peak_bw_units'], w))
        bw_units_combo.currentTextChanged.connect(self._update_uplink_suggestions)
        bw_goal_layout.addWidget(bw_units_combo)
        
        # Add Type (Leaf/Spine) dropdown close to the BW fields
        bw_goal_layout.addSpacing(15)  # Small space between BW and Type
        type_label = QLabel("Type:")
        bw_goal_layout.addWidget(type_label)
        type_combo = QComboBox()
        type_combo.addItems(['leaf', 'spine'])
        type_combo.setCurrentText(rack_data.get('lors', 'leaf'))
        type_combo.currentTextChanged.connect(lambda text, rn=rack_name, w=type_combo: self._on_rack_data_changed(rn, ['lors'], w))
        bw_goal_layout.addWidget(type_combo, 0)  # 0 stretch to keep it close to the label
        fields['lors'] = type_combo
        
        layout.addLayout(bw_goal_layout, 2, 3)
        fields['peak_bw_goal'] = bw_goal_entry
        fields['peak_bw_units'] = bw_units_combo

        # --- Node Details ---
        node_group = QGroupBox("Node Configuration")
        node_grid = QGridLayout(node_group)

        headers = [
            ('Node\nType', "The type of server node (e.g., DN, CN)."),
            ('Node\nCount', "The number of logical nodes of this type for this rack."),
            ('Split\nPorts?', "Check this if a single physical switch port will be split (using a breakout cable) to serve multiple logical nodes."),
            ('Split\nValue', "If splitting, select how many ways the port is split (e.g., 2 for 1:2, 4 for 1:4)."),
            ('Reserved\nPorts', "The number of extra physical ports to reserve alongside the assigned node ports.\nThese are labeled `RSVD-<NodeType>`."),
            ('Starting\nNode #', "The starting node number for this node type in this rack (e.g., DN100, CN1)."),
            ('Starting\nPort #', "The starting port number for this node type in this rack. Leave blank for auto-assignment.")
        ]
        for i, (header_text, tooltip_text) in enumerate(headers):
            header_label = QLabel(header_text)
            header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_label.setToolTip(tooltip_text)
            node_grid.addWidget(header_label, 0, i)

        fields['nodes'] = {}
        for i, node_type in enumerate(self.node_types, 1):
            node_data = rack_data.get('nodes', {}).get(node_type, self._get_default_node_data())
            node_grid.addWidget(QLabel(node_type), i, 0, Qt.AlignmentFlag.AlignCenter)

            count_entry = QLineEdit(str(node_data.get('count', 0)))
            count_entry.setValidator(self.port_validator)
            count_entry.setFixedWidth(40)
            count_entry.textChanged.connect(lambda text, rn=rack_name, nt=node_type, w=count_entry: self._on_rack_data_changed(rn, ['nodes', nt, 'count'], w))
            node_grid.addWidget(count_entry, i, 1, Qt.AlignmentFlag.AlignCenter)

            split_cb = QCheckBox()
            split_cb.setChecked(node_data.get('split', False))
            split_cb.toggled.connect(lambda checked, rn=rack_name, nt=node_type, w=split_cb: self._on_rack_data_changed(rn, ['nodes', nt, 'split'], w))
            node_grid.addWidget(split_cb, i, 2, Qt.AlignmentFlag.AlignCenter)

            factor_combo = QComboBox()
            factor_combo.addItems(['2', '4'])
            factor_combo.setCurrentText(str(node_data.get('factor', 2)))
            factor_combo.setFixedWidth(50)
            factor_combo.currentTextChanged.connect(lambda text, rn=rack_name, nt=node_type, w=factor_combo: self._on_rack_data_changed(rn, ['nodes', nt, 'factor'], w))
            node_grid.addWidget(factor_combo, i, 3, Qt.AlignmentFlag.AlignCenter)

            reserved_entry = QLineEdit(str(node_data.get('reserved', 0)))
            reserved_entry.setValidator(self.port_validator)
            reserved_entry.setFixedWidth(40)
            reserved_entry.textChanged.connect(lambda text, rn=rack_name, nt=node_type, w=reserved_entry: self._on_rack_data_changed(rn, ['nodes', nt, 'reserved'], w))
            node_grid.addWidget(reserved_entry, i, 4, Qt.AlignmentFlag.AlignCenter)

            # Starting Node # column with prefix label and entry box
            starting_node_container = QWidget()
            starting_node_layout = QHBoxLayout(starting_node_container)
            starting_node_layout.setContentsMargins(2, 0, 2, 0)
            starting_node_layout.setSpacing(0)
            
            # Prefix label (fixed, unchangeable)
            prefix_label = QLabel(node_type)
            prefix_label.setFixedWidth(20) # 2 characters
            prefix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            prefix_label.setStyleSheet("QLabel { background-color: #555555; color: white; padding: 2px; font-weight: bold; }")
            starting_node_layout.addWidget(prefix_label)
            
            # Entry box for the number
            starting_node_entry = QLineEdit('')
            starting_node_entry.setValidator(self.port_validator)
            
            # Set default starting numbers based on node type
            default_starting_numbers = {
                'DN': '100',
                'CN': '1',
                'EB': '1',
                'IE': '1',
                'GN': '1'
            }
            starting_node_value = str(node_data.get('starting_node', default_starting_numbers.get(node_type, '1')))
            starting_node_entry.setText(starting_node_value)
            starting_node_entry.setToolTip(f"Starting node number for {node_type} (e.g., {starting_node_value} for {node_type}-{starting_node_value}, {node_type}-{int(starting_node_value)+1}...)")
            starting_node_entry.setFixedWidth(25) # 3 characters for the number
            starting_node_entry.setEnabled(True)
            starting_node_entry.textChanged.connect(lambda text, rn=rack_name, nt=node_type, w=starting_node_entry: self._on_rack_data_changed(rn, ['nodes', nt, 'starting_node'], w))
            starting_node_layout.addWidget(starting_node_entry)
            
            starting_node_container.setFixedWidth(47) # Total width: 20 (prefix) + 25 (entry) + 2 (margins)
            node_grid.addWidget(starting_node_container, i, 5, Qt.AlignmentFlag.AlignCenter)

            start_port_entry = QLineEdit(str(node_data.get('start_port', '')))
            start_port_entry.setValidator(self.port_validator)
            start_port_entry.setFixedWidth(40)
            start_port_entry.setToolTip("The starting port number for this node type in this rack. Leave blank for auto-assignment.")
            start_port_entry.textChanged.connect(lambda text, rn=rack_name, nt=node_type, w=start_port_entry: self._on_rack_data_changed(rn, ['nodes', nt, 'start_port'], w))
            node_grid.addWidget(start_port_entry, i, 6, Qt.AlignmentFlag.AlignCenter)
            fields['nodes'][node_type] = {'count': count_entry, 'split': split_cb, 'factor': factor_combo, 'reserved': reserved_entry, 'starting_node': starting_node_entry, 'start_port': start_port_entry}

        # --- Uplink Details ---
        uplink_group = QGroupBox("Uplink Configuration")
        uplink_group.setToolTip("Define the uplink port layout for this specific rack.")
        uplink_grid = QGridLayout(uplink_group)
        uplink_headers = [
            ('Uplink\nType', "The type of uplink (e.g., ISL, MLAG/BGP)."),
            ('Uplink\nChannels', "The number of distinct Link Aggregation Groups (LAGs) for this uplink type."),
            ('Ports Per\nGroup', "The number of physical ports in EACH group."),
            ('Split\nPorts?', "Check this if a single physical switch port will be split (using a breakout cable)."),
            ('Split\nValue', "If splitting, select how many ways the port is split (e.g., 2 for 1:2, 4 for 1:4)."),
            ('Reserved\nPorts', "The number of extra physical ports to reserve alongside the assigned uplink ports."),
            ('Starting\nPort #', "The starting port number for this uplink type in this rack. Uplinks are typically assigned from the highest port numbers downwards.")
        ]
        for i, (header_text, tooltip_text) in enumerate(uplink_headers):
            label = QLabel(header_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setToolTip(tooltip_text)
            uplink_grid.addWidget(label, 0, i)

        fields['uplinks'] = {}
        for i, uplink_type in enumerate(self.uplink_types, 1):
            uplink_data = rack_data.get('uplinks', {}).get(uplink_type, self._get_default_uplink_data(uplink_type))
            uplink_grid.addWidget(QLabel(uplink_type), i, 0, Qt.AlignmentFlag.AlignCenter)

            groups_entry = QLineEdit(str(uplink_data.get('groups', 0)))
            groups_entry.setValidator(self.port_validator)
            groups_entry.setFixedWidth(40)
            groups_entry.setToolTip("The number of distinct Link Aggregation Groups (LAGs) for this uplink type.")
            if uplink_type in ['IPL', 'NB']: groups_entry.setEnabled(False)
            groups_entry.textChanged.connect(lambda text, rn=rack_name, ut=uplink_type, w=groups_entry: self._on_rack_data_changed(rn, ['uplinks', ut, 'groups'], w))
            uplink_grid.addWidget(groups_entry, i, 1, Qt.AlignmentFlag.AlignCenter)

            ppg_entry = QLineEdit(str(uplink_data.get('ports_per_group', 0)))
            ppg_entry.setValidator(self.port_validator)
            ppg_entry.setFixedWidth(40)
            ppg_entry.setToolTip("The number of physical ports in EACH group.")
            ppg_entry.textChanged.connect(lambda text, rn=rack_name, ut=uplink_type, w=ppg_entry: self._on_rack_data_changed(rn, ['uplinks', ut, 'ports_per_group'], w))
            uplink_grid.addWidget(ppg_entry, i, 2, Qt.AlignmentFlag.AlignCenter)
            
            split_cb = QCheckBox()
            split_cb.setChecked(uplink_data.get('split', False))
            split_cb.setToolTip("Check this if a single physical switch port will be split (using a breakout cable).")
            split_cb.toggled.connect(lambda checked, rn=rack_name, ut=uplink_type, w=split_cb: self._on_rack_data_changed(rn, ['uplinks', ut, 'split'], w))
            uplink_grid.addWidget(split_cb, i, 3, Qt.AlignmentFlag.AlignCenter)

            factor_combo = QComboBox()
            factor_combo.addItems(['2', '4'])
            factor_combo.setCurrentText(str(uplink_data.get('factor', 2)))
            factor_combo.setToolTip("If splitting, select how many ways the port is split (e.g., 2 for 1:2, 4 for 1:4).")
            factor_combo.setFixedWidth(50)
            factor_combo.currentTextChanged.connect(lambda text, rn=rack_name, ut=uplink_type, w=factor_combo: self._on_rack_data_changed(rn, ['uplinks', ut, 'factor'], w))
            uplink_grid.addWidget(factor_combo, i, 4, Qt.AlignmentFlag.AlignCenter)

            reserved_entry = QLineEdit(str(uplink_data.get('reserved', 0)))
            reserved_entry.setValidator(self.port_validator)
            reserved_entry.setToolTip("The number of extra physical ports to reserve alongside the assigned uplink ports.")
            reserved_entry.setFixedWidth(40)
            reserved_entry.textChanged.connect(lambda text, rn=rack_name, ut=uplink_type, w=reserved_entry: self._on_rack_data_changed(rn, ['uplinks', ut, 'reserved'], w))
            uplink_grid.addWidget(reserved_entry, i, 5, Qt.AlignmentFlag.AlignCenter)

            start_entry = QLineEdit(str(uplink_data.get('start', '')))
            start_entry.setValidator(self.port_validator)
            start_entry.setToolTip("The starting port number for this uplink type in this rack. Uplinks are typically assigned from the highest port numbers downwards.")
            start_entry.setFixedWidth(40)
            start_entry.textChanged.connect(lambda text, rn=rack_name, ut=uplink_type, w=start_entry: self._on_rack_data_changed(rn, ['uplinks', ut, 'start'], w))
            uplink_grid.addWidget(start_entry, i, 6, Qt.AlignmentFlag.AlignCenter)

            fields['uplinks'][uplink_type] = {
                'groups': groups_entry,
                'ports_per_group': ppg_entry,
                'split': split_cb,
                'factor': factor_combo,
                'reserved': reserved_entry,
                'start': start_entry
            }
        layout.addWidget(node_group, 3, 0, 1, 4) # Span all 4 columns (moved up from row 4)
        layout.addWidget(uplink_group, 4, 0, 1, 4) # Span all 4 columns (moved up from row 5)

        # Final assembly of the detail widget
        scroll_area.setWidget(detail_content_widget)

        # Use a QVBoxLayout to place the arrow below the scroll area
        main_detail_layout = QVBoxLayout(detail_widget)
        main_detail_layout.setContentsMargins(0, 0, 0, 0)

        # Add scroll arrow for up
        scroll_arrow_up = QLabel("▲")
        scroll_arrow_up.setStyleSheet("color: white; font-size: 20px; background-color: transparent;")
        scroll_arrow_up.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_detail_layout.addWidget(scroll_arrow_up)
        main_detail_layout.addWidget(scroll_area)

        # Add scroll arrow
        scroll_arrow = QLabel("▼")
        scroll_arrow.setStyleSheet("color: white; font-size: 20px; background-color: transparent;")
        scroll_arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_detail_layout.addWidget(scroll_arrow)
        
        scroll_bar = scroll_area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: self._update_scroll_arrows_visibility(scroll_area, scroll_arrow_up, scroll_arrow))
        scroll_bar.valueChanged.connect(lambda: self._update_scroll_arrows_visibility(scroll_area, scroll_arrow_up, scroll_arrow))

        # Store widgets for later access and add to the stack
        self.rack_widgets[rack_name] = {'widget': detail_widget, 'fields': fields}
        self.rack_details_stack.addWidget(detail_widget)

    def _build_legacy_installs_ui(self):
        """Builds the UI for the new Legacy Installs tab."""
        main_widget = QWidget()
        main_widget.setObjectName("DarkTab") # Use the same dark theme

        # Main layout for the tab
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Use a scroll area to handle many input fields
        scroll_area = QScrollArea()
        self.legacy_scroll_area = scroll_area # Store reference
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        # Add the scroll arrow for up, above the scroll area
        self.legacy_scroll_arrow_up = QLabel("▲")
        self.legacy_scroll_arrow_up.setStyleSheet("color: white; font-size: 20px; background-color: transparent;")
        self.legacy_scroll_arrow_up.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.legacy_scroll_arrow_up)


        scroll_content = QWidget()
        scroll_content.setObjectName("DarkTab")
        layout = QVBoxLayout(scroll_content)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # --- Group 1: Cluster & Build Information ---
        cluster_group = QGroupBox("Cluster & Build Information")
        cluster_layout = QGridLayout(cluster_group)

        cluster_layout.addWidget(QLabel("Customer Name:"), 0, 0)
        self.legacy_customer = QLineEdit()
        self.legacy_customer.textChanged.connect(self._update_legacy_hostname_example)
        cluster_layout.addWidget(self.legacy_customer, 0, 1)

        cluster_layout.addWidget(QLabel("Cluster Name:"), 1, 0)
        self.legacy_cluster_name = QLineEdit()
        self.legacy_cluster_name.textChanged.connect(self._update_legacy_hostname_example)
        self.legacy_cluster_name.setPlaceholderText("e.g., major-cluster")
        cluster_layout.addWidget(self.legacy_cluster_name, 1, 1)
        self.legacy_cluster_name.setToolTip("The name of the VAST cluster.")

        cluster_layout.addWidget(QLabel("Rack Identifier:"), 2, 0)
        self.legacy_rack_identifier = QLineEdit()
        self.legacy_rack_identifier.textChanged.connect(self._update_legacy_hostname_example)
        self.legacy_rack_identifier.setPlaceholderText("e.g., r1 (optional)")
        cluster_layout.addWidget(self.legacy_rack_identifier, 2, 1)
        self.legacy_rack_identifier.setToolTip("An optional rack identifier, available as the {rack} placeholder in the hostname template.")

        cluster_layout.addWidget(QLabel("Release Version:"), 0, 2)
        self.legacy_release = QLineEdit(); self.legacy_release.setPlaceholderText("e.g., 5.2.0-sp4-1559887"); cluster_layout.addWidget(self.legacy_release, 0, 3); self.legacy_release.setToolTip("The VAST Data software release version.")

        cluster_layout.addWidget(QLabel("Buildfile Name:"), 1, 2); self.legacy_buildfile = QLineEdit(); self.legacy_buildfile.setPlaceholderText("e.g., release-5.2.0-sp4-1559887.vast.tar.gz"); cluster_layout.addWidget(self.legacy_buildfile, 1, 3); self.legacy_buildfile.setToolTip("The full filename of the software build tarball.")

        cluster_layout.addWidget(QLabel("Cluster PSNT:"), 2, 2)
        self.legacy_cluster_label = QLineEdit()
        self.legacy_cluster_label.setPlaceholderText("e.g., VA24432251")
        cluster_layout.addWidget(self.legacy_cluster_label, 2, 3)

        layout.addWidget(cluster_group)

        # --- Group 2: Device Counts ---
        device_group = QGroupBox("Device Counts")
        device_layout = QGridLayout(device_group)

        # Use font metrics to set fixed widths based on character count
        font_metrics = self.fontMetrics()
        char_width = font_metrics.averageCharWidth()
        ten_char_width = char_width * 10

        self.legacy_cnode_label = QLabel("Number of Cnodes:")
        device_layout.addWidget(self.legacy_cnode_label, 1, 0)
        self.legacy_cnode_count = QLineEdit()
        self.legacy_cnode_count.setValidator(self.numeric_validator)
        self.legacy_cnode_count.setFixedWidth(ten_char_width)
        device_layout.addWidget(self.legacy_cnode_count, 1, 1)
        self.legacy_cnode_count.setToolTip("The total number of C-nodes or E-boxes in the cluster.")

        dbox_type_tooltip = "The model of the D-Box (Data Box)."
        self.legacy_dbox_type_label = QLabel("DBOX Type:")
        device_layout.addWidget(self.legacy_dbox_type_label, 3, 2)
        self.legacy_dbox_type = QComboBox()
        self.legacy_dbox_type.addItems(["Ceres", "Mavericks"])
        self.legacy_dbox_type.setFixedWidth(ten_char_width)
        device_layout.addWidget(self.legacy_dbox_type, 3, 3)
        self.legacy_dbox_type_label.setToolTip(dbox_type_tooltip)
        self.legacy_dbox_type.setToolTip(dbox_type_tooltip)

        ceres_version_tooltip = "The hardware revision of the Ceres D-Box."
        self.legacy_ceres_version_label = QLabel("Ceres Version:")
        device_layout.addWidget(self.legacy_ceres_version_label, 3, 4)
        self.legacy_ceres_version = QComboBox()
        self.legacy_ceres_version.addItems(["v1", "v2"])
        device_layout.addWidget(self.legacy_ceres_version, 3, 5)
        self.legacy_ceres_version_label.setToolTip(ceres_version_tooltip)
        self.legacy_ceres_version.setToolTip(ceres_version_tooltip)

        dbox_count_tooltip = "The total number of D-Boxes in the cluster."
        self.legacy_dbox_count_label = QLabel("Number of DBOXes:")
        device_layout.addWidget(self.legacy_dbox_count_label, 3, 0)
        self.legacy_dbox_count = QLineEdit()
        self.legacy_dbox_count.setFixedWidth(ten_char_width)
        self.legacy_dbox_count.setValidator(self.numeric_validator)
        device_layout.addWidget(self.legacy_dbox_count, 3, 1)
        self.legacy_dbox_count_label.setToolTip(dbox_count_tooltip)
        self.legacy_dbox_count.setToolTip(dbox_count_tooltip)

        self.legacy_ebox_count_label = QLabel("Number of Eboxes:")
        device_layout.addWidget(self.legacy_ebox_count_label, 4, 0)
        self.legacy_ebox_count = QLineEdit()
        self.legacy_ebox_count.setFixedWidth(ten_char_width)
        self.legacy_ebox_count.setValidator(self.numeric_validator)
        device_layout.addWidget(self.legacy_ebox_count, 4, 1)

        device_layout.setColumnStretch(6, 1) # Add stretch to the right

        layout.addWidget(device_group)

        # --- Group for Hostname Templating ---
        hostname_group = QGroupBox("Hostname Template Configuration")
        hostname_layout = QGridLayout(hostname_group)

        hostname_layout.addWidget(QLabel("Hostname Template:"), 0, 0)
        self.legacy_hostname_template = QLineEdit()
        self.legacy_hostname_template.setText("{customer}-{cluster}-{rack}-{type}{num}")
        self.legacy_hostname_template.setToolTip("Define a flexible hostname format.\n"
                                                 "\n"
                                                 "<b>Available placeholders:</b>\n"
                                                 "  {type}     - Node type (e.g., 'cn', 'dn', 'eb')\n"
                                                 "  {num}      - Node number (e.g., 1, 101)\n"
                                                 "  {cluster}  - Cluster name from above\n"
                                                 "  {rack}     - Rack Identifier from above\n"
                                                 "  {customer} - The customer name from the field above\n"
                                                 "\n"
                                                 "You can also add your own user-definable fields.\n"
                                                 "If left blank, default hostnames will be used (e.g., cnode1, dnode100).")
        hostname_layout.addWidget(self.legacy_hostname_template, 0, 1)

        # Add a label to show an example of the output
        self.legacy_hostname_example_label = QLabel()
        self.legacy_hostname_example_label.setStyleSheet("font-style: italic; color: #AAAAAA;")
        hostname_layout.addWidget(self.legacy_hostname_example_label, 1, 1)

        self.legacy_hostname_template.textChanged.connect(self._update_legacy_hostname_example)
        self._update_legacy_hostname_example()

        # --- Group 3: Management Network ---        
        mgmt_group = QGroupBox("Management Network")
        mgmt_layout = QGridLayout(mgmt_group)

        self.legacy_mgmt_ip_cnode_label = QLabel("First CNode MGMT IP:")
        mgmt_layout.addWidget(self.legacy_mgmt_ip_cnode_label, 0, 0)
        self.legacy_mgmt_ip_cnode = QLineEdit()
        self.legacy_mgmt_ip_cnode.setToolTip("The management IP address of the first C-node or E-box.")
        mgmt_layout.addWidget(self.legacy_mgmt_ip_cnode, 0, 1)

        self.legacy_mgmt_ip_dnode_label = QLabel("First DNode MGMT IP:")
        mgmt_layout.addWidget(self.legacy_mgmt_ip_dnode_label, 1, 0)
        self.legacy_mgmt_ip_dnode = QLineEdit()
        self.legacy_mgmt_ip_dnode.setToolTip("The management IP address of the first D-node.")
        mgmt_layout.addWidget(self.legacy_mgmt_ip_dnode, 1, 1)

        self.legacy_mgmt_ip_ebox_label = QLabel("First Ebox MGMT IP:")
        mgmt_layout.addWidget(self.legacy_mgmt_ip_ebox_label, 2, 0)
        self.legacy_mgmt_ip_ebox = QLineEdit()
        mgmt_layout.addWidget(self.legacy_mgmt_ip_ebox, 2, 1)

        mgmt_layout.addWidget(QLabel("MGMT Netmask:"), 3, 0)
        self.legacy_mgmt_netmask = QLineEdit()
        mgmt_layout.addWidget(self.legacy_mgmt_netmask, 3, 1)

        dns_tooltip = "A space-separated list of DNS server IP addresses."
        mgmt_layout.addWidget(QLabel("DNS Servers:"), 0, 2)
        self.legacy_dns = QLineEdit()
        self.legacy_dns.setPlaceholderText("Separated by spaces")
        mgmt_layout.addWidget(self.legacy_dns, 0, 3)
        self.legacy_dns.setToolTip(dns_tooltip)

        ntp_tooltip = "A space-separated list of NTP server IP addresses."
        mgmt_layout.addWidget(QLabel("NTP Servers:"), 1, 2)
        self.legacy_ntp = QLineEdit()
        self.legacy_ntp.setPlaceholderText("Separated by spaces")
        mgmt_layout.addWidget(self.legacy_ntp, 1, 3)
        self.legacy_ntp.setToolTip(ntp_tooltip)

        gateway_tooltip = "The default gateway for the management network."
        mgmt_layout.addWidget(QLabel("MGMT Gateway:"), 2, 2)
        self.legacy_ext_gateway = QLineEdit()
        mgmt_layout.addWidget(self.legacy_ext_gateway, 2, 3)
        self.legacy_ext_gateway.setToolTip(gateway_tooltip)
        
        self.legacy_b2b_ipmi = QCheckBox("B2B IPMI")
        self.legacy_b2b_ipmi.setToolTip("Include the --b2b-ipmi flag in the configure_network.py command.")
        self.legacy_b2b_ipmi.setChecked(True)
        mgmt_layout.addWidget(self.legacy_b2b_ipmi, 3, 3)

        vms_vip_tooltip = "The Virtual IP address for the VMS (VAST Management Service)."
        mgmt_layout.addWidget(QLabel("VMS VIP:"), 4, 0)
        self.legacy_vm_vip = QLineEdit()
        mgmt_layout.addWidget(self.legacy_vm_vip, 4, 1)
        self.legacy_vm_vip.setToolTip(vms_vip_tooltip)
        
        switch1_tooltip = "The management IP address of the first backend switch (Fabric A)."
        mgmt_layout.addWidget(QLabel("Backend Switch 1 IP:"), 5, 0)
        self.legacy_switch1 = QLineEdit()
        mgmt_layout.addWidget(self.legacy_switch1, 5, 1)
        self.legacy_switch1.setToolTip(switch1_tooltip)
        
        switch2_tooltip = "The management IP address of the second backend switch (Fabric B)."
        mgmt_layout.addWidget(QLabel("Backend Switch 2 IP:"), 5, 2)
        self.legacy_switch2 = QLineEdit()
        mgmt_layout.addWidget(self.legacy_switch2, 5, 3)

        layout.addWidget(hostname_group)

        layout.addWidget(mgmt_group)

        # --- Group 4: Switches & Networking ---
        switch_net_group = QGroupBox("Switches & Networking")
        switch_net_layout = QGridLayout(switch_net_group)

        mellanox_tooltip = "Check if using Mellanox/NVIDIA switches."
        self.legacy_mellanox_switches = QCheckBox("Using Mellanox Switches?")
        switch_net_layout.addWidget(self.legacy_mellanox_switches, 0, 0, 1, 2)
        self.legacy_mellanox_switches.setToolTip(mellanox_tooltip)

        switch_os_tooltip = "The operating system of the switches (e.g., Onyx, Cumulus)."
        switch_net_layout.addWidget(QLabel("Switch OS:"), 0, 2)
        self.legacy_switch_os = QComboBox()
        self.legacy_switch_os.addItems(["Onyx", "Cumulus"])
        switch_net_layout.addWidget(self.legacy_switch_os, 0, 3)
        self.legacy_switch_os.setToolTip(switch_os_tooltip)

        skip_nic_tooltip = "Check to skip configuration of the secondary NIC on C-nodes."
        self.legacy_skip_nic = QCheckBox("Skip Secondary NIC?")
        switch_net_layout.addWidget(self.legacy_skip_nic, 1, 0, 1, 2)
        self.legacy_skip_nic.setToolTip(skip_nic_tooltip)

        rdma_pfc_tooltip = "Check if RDMA over Converged Ethernet (RoCE) and Priority Flow Control (PFC) are supported and should be enabled."
        self.legacy_rdma_pfc = QCheckBox("RDMA/PFC Support?")
        switch_net_layout.addWidget(self.legacy_rdma_pfc, 1, 2, 1, 2)
        self.legacy_rdma_pfc.setToolTip(rdma_pfc_tooltip)

        auto_ports_tooltip = "Select the auto-port configuration mode for network interfaces."
        switch_net_layout.addWidget(QLabel("Auto-Ports Config:"), 2, 0)
        self.legacy_auto_ports = QComboBox()
        self.legacy_auto_ports.addItems(["int_eth_ext_ib", "int_eth_ext_ib_eth", "eth", "ib"])
        self.legacy_auto_ports.setCurrentText("eth")
        self.legacy_auto_ports.setFixedWidth(ten_char_width)
        switch_net_layout.addWidget(self.legacy_auto_ports, 2, 1)
        self.legacy_auto_ports.setToolTip(auto_ports_tooltip)

        ib_mode_tooltip = "The mode for InfiniBand connections."
        self.legacy_change_ib_mode = QCheckBox("IB Mode")
        switch_net_layout.addWidget(self.legacy_change_ib_mode, 2, 2)
        self.legacy_ib_mode = QComboBox()
        self.legacy_ib_mode.addItems(["datagram"])
        switch_net_layout.addWidget(self.legacy_ib_mode, 2, 3)
        self.legacy_ib_mode.setToolTip(ib_mode_tooltip)
        self.legacy_change_ib_mode.setToolTip(ib_mode_tooltip)

        ib_mtu_tooltip = "The Maximum Transmission Unit (MTU) for northbound InfiniBand interfaces."
        switch_net_layout.addWidget(QLabel("Northbound IB MTU:"), 3, 0)
        self.legacy_ib_mtu = QLineEdit()
        self.legacy_ib_mtu.setText("2044")
        self.legacy_ib_mtu.setValidator(self.mtu_validator)
        self.legacy_ib_mtu.setFixedWidth(char_width * 5)
        switch_net_layout.addWidget(self.legacy_ib_mtu, 3, 1)
        self.legacy_ib_mtu.setToolTip(ib_mtu_tooltip)

        eth_mtu_tooltip = "The Maximum Transmission Unit (MTU) for northbound Ethernet interfaces."
        switch_net_layout.addWidget(QLabel("Northbound ETH MTU:"), 3, 2)
        self.legacy_eth_mtu = QLineEdit()
        self.legacy_eth_mtu.setText("9000")
        self.legacy_eth_mtu.setValidator(self.mtu_validator)
        self.legacy_eth_mtu.setFixedWidth(char_width * 5)
        switch_net_layout.addWidget(self.legacy_eth_mtu, 3, 3)
        self.legacy_eth_mtu.setToolTip(eth_mtu_tooltip)

        vxlan_tooltip = "Check if VXLAN is supported and should be enabled."
        self.legacy_vxlan = QCheckBox("VXLAN Support?")
        switch_net_layout.addWidget(self.legacy_vxlan, 4, 0, 1, 2)
        self.legacy_vxlan.setToolTip(vxlan_tooltip)

        switch_net_layout.setColumnStretch(4, 1) # Add stretch to the right

        layout.addWidget(switch_net_group)

        # --- Group 5: Advanced & Optional Settings ---
        advanced_group = QGroupBox("Advanced & Optional Settings")
        advanced_layout = QGridLayout(advanced_group)
        # Use font metrics to set fixed widths based on character count
        font_metrics = self.fontMetrics()
        char_width = font_metrics.averageCharWidth()

        # Column 1
        self.legacy_change_vlan = QCheckBox("Change Data Vlan")
        advanced_layout.addWidget(self.legacy_change_vlan, 0, 0)
        self.legacy_vlan_id = QLineEdit()
        self.legacy_vlan_id.setValidator(self.vlan_id_validator)
        self.legacy_vlan_id.setFixedWidth(char_width * 5)
        advanced_layout.addWidget(self.legacy_vlan_id, 0, 1)

        self.legacy_change_docker_bip = QCheckBox("Change Docker Bridge IP /16")
        advanced_layout.addWidget(self.legacy_change_docker_bip, 1, 0)
        self.legacy_docker_bip = QLineEdit()
        self.legacy_docker_bip.setFixedWidth(char_width * 8)
        advanced_layout.addWidget(self.legacy_docker_bip, 1, 1)

        # Column 2
        self.legacy_change_template = QCheckBox("Change Template /16")
        self.legacy_change_template.setToolTip("Check to override the default internal IP address template (172.16).")
        # This is the template field for the internal IP address, moved from the hostname group
        self.legacy_template = QLineEdit()
        self.legacy_template.setPlaceholderText("e.g., 172.16")

        advanced_layout.addWidget(self.legacy_change_template, 0, 2)
        self.legacy_template.setFixedWidth(char_width * 8)
        advanced_layout.addWidget(self.legacy_template, 0, 3)

        self.legacy_change_isolcpu = QCheckBox("Change ISOLCPU Values")
        self.legacy_isolcpu = QLineEdit()
        self.legacy_isolcpu.setPlaceholderText("e.g., 1-3,5")
        self.legacy_isolcpu.setToolTip("Specify CPU cores to isolate from the general-purpose scheduler (e.g., for performance-critical tasks).")
        self.legacy_isolcpu.setFixedWidth(char_width * 5)
        self.legacy_isolcpu.setEnabled(False)

        advanced_layout.addWidget(self.legacy_change_isolcpu, 1, 2)
        advanced_layout.addWidget(self.legacy_isolcpu, 1, 3)

        # Row 2: MGMT Inner VIP
        advanced_layout.addWidget(QLabel("MGMT Inner VIP:"), 2, 0)
        self.legacy_mgmt_inner_vip = QLineEdit()
        self.legacy_mgmt_inner_vip.setFixedWidth(char_width * 15)
        self.legacy_mgmt_inner_vip.setToolTip("The inner management VIP address for the cluster.")
        advanced_layout.addWidget(self.legacy_mgmt_inner_vip, 2, 1)

        # Add stretch to the right of the second column
        advanced_layout.setColumnStretch(4, 1)

        # Connect signals
        self.legacy_change_vlan.toggled.connect(self._on_legacy_vlan_toggled)
        self.legacy_change_template.toggled.connect(self._on_legacy_template_toggled)
        self.legacy_change_docker_bip.toggled.connect(self._on_legacy_docker_bip_toggled)
        self.legacy_change_isolcpu.toggled.connect(self._on_legacy_manual_isolcpu_toggled)
        self.legacy_change_ib_mode.toggled.connect(self._on_legacy_ib_mode_toggled)
        layout.addWidget(advanced_group)
        
        # Set initial state of disabled fields
        self._on_legacy_template_toggled(self.legacy_change_template.isChecked())
        self._on_legacy_vlan_toggled(self.legacy_change_vlan.isChecked())
        self._on_legacy_ib_mode_toggled(self.legacy_change_ib_mode.isChecked())
        self._on_legacy_docker_bip_toggled(self.legacy_change_docker_bip.isChecked())        
        self._on_legacy_manual_isolcpu_toggled(self.legacy_change_isolcpu.isChecked())

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # Add the scroll arrow below the scroll area
        self.legacy_scroll_arrow = QLabel("▼")
        self.legacy_scroll_arrow.setStyleSheet("color: white; font-size: 20px; background-color: transparent;")
        self.legacy_scroll_arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.legacy_scroll_arrow)

        # --- Action Buttons and Output Area ---        
        button_layout = QHBoxLayout()
        self.legacy_generate_button = QPushButton("Generate Legacy Commands")
        self.legacy_generate_button.clicked.connect(self._generate_legacy_commands)
        self.legacy_save_button = QPushButton("Save Output to File")
        self.legacy_save_button.clicked.connect(self._save_legacy_output)
        self.legacy_save_button.setEnabled(False) # Disabled until there is output
        button_layout.addStretch()
        button_layout.addWidget(self.legacy_generate_button)
        button_layout.addWidget(self.legacy_save_button)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.legacy_output_text = QTextEdit()
        self.legacy_output_text.setReadOnly(True)
        self.legacy_output_text.setPlaceholderText("Generated commands will appear here...")
        main_layout.addWidget(self.legacy_output_text)
        # When text is added, enable the save button
        self.legacy_output_text.textChanged.connect(lambda: self.legacy_save_button.setEnabled(bool(self.legacy_output_text.toPlainText())))

        # Add the credit label at the very bottom of the tab
        credit_label = QLabel("Legacy install command generation logic courtesy of Jeremy Ortega")
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit_label.setStyleSheet("font-style: italic; color: #AAAAAA; padding-top: 5px;")
        main_layout.addWidget(credit_label)

        # Connect scroll bar signals for the arrows
        scroll_bar = scroll_area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: self._update_scroll_arrows_visibility(scroll_area, self.legacy_scroll_arrow_up, self.legacy_scroll_arrow))
        scroll_bar.valueChanged.connect(lambda: self._update_scroll_arrows_visibility(scroll_area, self.legacy_scroll_arrow_up, self.legacy_scroll_arrow))
        return main_widget

    def _update_scroll_arrows_visibility(self, scroll_area: QScrollArea, up_arrow: QLabel, down_arrow: QLabel):
        """Shows or hides scroll indicator arrows based on the scrollbar position."""
        scroll_bar = scroll_area.verticalScrollBar()
        min_val, max_val = scroll_bar.minimum(), scroll_bar.maximum()
        current_val = scroll_bar.value()

        # Show up arrow if not at the very top
        up_arrow.setVisible(current_val > min_val)
        # Show down arrow if not at the very bottom
        down_arrow.setVisible(current_val < max_val)

    def _on_legacy_template_toggled(self, checked: bool):
        """Enables or disables the template-related fields on the Legacy tab."""
        # This now only controls the Template field.
        self.legacy_template.setEnabled(checked)

        if not checked:
            self.legacy_template.clear()

    def _on_legacy_vlan_toggled(self, checked: bool):
        """Enables or disables the VLAN ID field on the Legacy tab."""
        self.legacy_vlan_id.setEnabled(checked)
        if not checked:
            self.legacy_vlan_id.clear()

    def _on_legacy_docker_bip_toggled(self, checked: bool):
        """Enables or disables the Docker Bridge IP field on the Legacy tab."""
        self.legacy_docker_bip.setEnabled(checked)
        if not checked:
            self.legacy_docker_bip.clear()

    def _on_legacy_manual_isolcpu_toggled(self, checked: bool):
        """Enables or disables the ISOLCPU field on the Legacy tab."""
        self.legacy_isolcpu.setEnabled(checked)
        if not checked:
            self.legacy_isolcpu.clear()

    def _on_legacy_ib_mode_toggled(self, checked: bool):
        self.legacy_ib_mode.setEnabled(checked)
        if not checked:
            self.legacy_ib_mode.setCurrentText("datagram")

    def _on_legacy_ib_mode_toggled(self, checked: bool):
        self.legacy_ib_mode.setEnabled(checked)
        if not checked:
            self.legacy_ib_mode.setCurrentText("datagram")


    def _build_advanced_layout_ui(self):
        """Builds the Advanced Layout tab for cable path routing preferences (test/isolated mode)."""
        main_widget = QWidget()
        main_widget.setObjectName("DarkTab")
        main_layout = QVBoxLayout(main_widget)
        
        # Switch model display (read-only from Setup tab) - compact single line
        switch_info_layout = QHBoxLayout()
        switch_info_layout.setContentsMargins(0, 0, 0, 5)  # Minimal margins
        self.advanced_layout_switch_label = QLabel('Switch Model: Not loaded - configure on Setup tab')
        self.advanced_layout_switch_label.setStyleSheet("font-weight: bold; color: #4a90e2;")
        switch_info_layout.addWidget(self.advanced_layout_switch_label)
        switch_info_layout.addStretch()
        main_layout.addLayout(switch_info_layout)
        
        # DBox type selector
        dbox_group = QGroupBox('DBox Type')
        dbox_layout = QHBoxLayout(dbox_group)
        self.advanced_layout_dbox_mav = QRadioButton('Mav')
        self.advanced_layout_dbox_ceresv1 = QRadioButton('CeresV1')
        self.advanced_layout_dbox_ceresv2 = QRadioButton('CeresV2')
        # Connect signals BEFORE setting checked to avoid premature handler calls
        self.advanced_layout_dbox_mav.toggled.connect(self._on_advanced_layout_dbox_changed)
        self.advanced_layout_dbox_ceresv1.toggled.connect(self._on_advanced_layout_dbox_changed)
        self.advanced_layout_dbox_ceresv2.toggled.connect(self._on_advanced_layout_dbox_changed)
        # Set default AFTER connecting signals
        self.advanced_layout_dbox_ceresv1.setChecked(True)  # Default
        dbox_layout.addWidget(QLabel('Select DBox Type:'))
        dbox_layout.addWidget(self.advanced_layout_dbox_mav)
        dbox_layout.addWidget(self.advanced_layout_dbox_ceresv1)
        dbox_layout.addWidget(self.advanced_layout_dbox_ceresv2)
        dbox_layout.addStretch()
        main_layout.addWidget(dbox_group)
        
        # Combined configuration section: Node config and Uplink config side-by-side
        config_group = QGroupBox('Configuration')
        config_layout = QHBoxLayout(config_group)
        
        # Left side: Node counts and routing configuration
        node_counts_group = QWidget()
        node_counts_group.setMaximumWidth(450)  # Constrain width - narrow table
        node_counts_layout = QGridLayout(node_counts_group)
        node_counts_layout.setColumnStretch(0, 0)  # Type column: fixed width
        node_counts_layout.setColumnStretch(1, 0)  # Count column: fixed width
        node_counts_layout.setColumnStretch(2, 0)  # Split column: fixed width
        node_counts_layout.setColumnStretch(3, 0)  # Factor column: fixed width
        node_counts_layout.setColumnStretch(4, 0)  # Route column: fixed width
        
        # Headers
        node_counts_layout.addWidget(QLabel('<b>Type</b>'), 0, 0)
        node_counts_layout.addWidget(QLabel('<b>Count</b>'), 0, 1)
        node_counts_layout.addWidget(QLabel('<b>Split</b>'), 0, 2)
        node_counts_layout.addWidget(QLabel('<b>Factor</b>'), 0, 3)
        node_counts_layout.addWidget(QLabel('<b>Route</b>'), 0, 4)
        
        # DN row
        node_counts_layout.addWidget(QLabel('DN:'), 1, 0)
        self.advanced_layout_dn_count = QLineEdit('')
        self.advanced_layout_dn_count.setValidator(self.port_validator)
        self.advanced_layout_dn_count.setToolTip('Number of Data Nodes (must be even - 2 per DBox)')
        self.advanced_layout_dn_count.setFixedWidth(40)  # Compact: 4 chars max
        self.advanced_layout_dn_count.editingFinished.connect(self._validate_dn_count_even)
        self.advanced_layout_dn_count.returnPressed.connect(self._validate_dn_count_even)
        node_counts_layout.addWidget(self.advanced_layout_dn_count, 1, 1)
        
        # DN split options
        self.advanced_layout_dn_split_cb = QCheckBox()
        self.advanced_layout_dn_split_cb.setToolTip('Check if using breakout cables to split DN ports')
        self.advanced_layout_dn_split_cb.toggled.connect(self._on_advanced_layout_recalculate)
        node_counts_layout.addWidget(self.advanced_layout_dn_split_cb, 1, 2)
        
        self.advanced_layout_dn_factor = QComboBox()
        self.advanced_layout_dn_factor.addItems(['2', '4'])
        self.advanced_layout_dn_factor.setToolTip('Split factor: 2 for 1:2, 4 for 1:4')
        self.advanced_layout_dn_factor.setFixedWidth(50)
        self.advanced_layout_dn_factor.currentTextChanged.connect(self._on_advanced_layout_recalculate)
        node_counts_layout.addWidget(self.advanced_layout_dn_factor, 1, 3)
        
        # DN is fixed (Even=LEFT, Odd=RIGHT)
        dn_route_label = QLabel('(fixed)')
        dn_route_label.setStyleSheet("color: #888888; font-size: 9pt;")
        node_counts_layout.addWidget(dn_route_label, 1, 4)
        
        node_types_to_add = ['CN', 'EB', 'IE', 'GN']
        self.advanced_layout_node_counts = {}
        self.advanced_layout_node_splits = {}
        self.advanced_layout_routing_widgets = {}  # Store per-node-type routing widgets
        
        for i, nt in enumerate(node_types_to_add, 2):
            node_counts_layout.addWidget(QLabel(f'{nt}:'), i, 0)
            count_entry = QLineEdit('')
            count_entry.setValidator(self.port_validator)
            count_entry.setFixedWidth(40)  # Compact: 4 chars max
            self.advanced_layout_node_counts[nt] = count_entry
            node_counts_layout.addWidget(count_entry, i, 1)
            
            # Split checkbox
            split_cb = QCheckBox()
            split_cb.setToolTip('Check if using breakout cables to split ports')
            self.advanced_layout_node_splits[nt] = {'split_cb': split_cb, 'factor': None}
            node_counts_layout.addWidget(split_cb, i, 2)
            
            # Factor combo
            factor_combo = QComboBox()
            factor_combo.addItems(['2', '4'])
            factor_combo.setToolTip('Split factor: 2 for 1:2, 4 for 1:4')
            factor_combo.setFixedWidth(50)
            self.advanced_layout_node_splits[nt]['factor'] = factor_combo
            node_counts_layout.addWidget(factor_combo, i, 3)
            
            # L/R routing radio buttons (compact, inline)
            routing_container = QWidget()
            routing_hbox = QHBoxLayout(routing_container)
            routing_hbox.setContentsMargins(0, 0, 0, 0)
            routing_hbox.setSpacing(2)
            
            left_radio = QRadioButton('L')
            right_radio = QRadioButton('R')
            right_radio.setChecked(True)  # Default to RIGHT
            left_radio.setFixedWidth(22)
            right_radio.setFixedWidth(22)
            routing_hbox.addWidget(left_radio)
            routing_hbox.addWidget(right_radio)
            self.advanced_layout_routing_widgets[nt] = {'left': left_radio, 'right': right_radio}
            
            left_radio.toggled.connect(self._on_advanced_layout_recalculate)
            right_radio.toggled.connect(self._on_advanced_layout_recalculate)
            node_counts_layout.addWidget(routing_container, i, 4)
            
            # Connect signals
            count_entry.textChanged.connect(self._on_advanced_layout_counts_changed)
            split_cb.toggled.connect(self._on_advanced_layout_recalculate)
            factor_combo.currentTextChanged.connect(self._on_advanced_layout_recalculate)
        
        # Add node counts table to config layout (left side)
        config_layout.addWidget(node_counts_group)
        
        # Right side: Uplink configuration
        uplink_group = QGroupBox('Uplink Configuration')
        uplink_layout = QGridLayout(uplink_group)
        uplink_layout.setHorizontalSpacing(5)  # Very tight spacing between columns
        uplink_layout.setColumnStretch(0, 0)  # Column 0: fixed width (Type labels)
        uplink_layout.setColumnStretch(1, 0)  # Column 1: fixed width (Groups)
        uplink_layout.setColumnStretch(2, 0)  # Column 2: fixed width (Ports/Group)
        uplink_types = ['IPL', 'ISL', 'EXT']
        self.advanced_layout_uplink_widgets = {}
        
        uplink_layout.addWidget(QLabel('Uplink Type'), 0, 0)
        uplink_layout.addWidget(QLabel('Groups'), 0, 1)
        uplink_layout.addWidget(QLabel('Ports/Group'), 0, 2)
        
        for i, ut in enumerate(uplink_types, 1):
            ut_label = QLabel(ut)
            ut_label.setFixedWidth(30)  # Constrain width to just fit label
            uplink_layout.addWidget(ut_label, i, 0)
            groups_entry = QLineEdit(str(self.advanced_layout_config['uplinks'][ut]['groups']) if self.advanced_layout_config['uplinks'][ut]['groups'] > 0 else '')
            groups_entry.setValidator(self.port_validator)
            
            # IPL groups is fixed at 1 and should be disabled/greyed out
            if ut == 'IPL':
                groups_entry.setEnabled(False)
                groups_entry.setText('1')
                groups_entry.setStyleSheet("background-color: #555555; color: #AAAAAA;")
                groups_entry.setToolTip('IPL is always a single group (fixed)')
            else:
                groups_entry.textChanged.connect(self._on_advanced_layout_recalculate)
            
            ppg_val = self.advanced_layout_config['uplinks'][ut]['ports_per_group']
            ppg_entry = QLineEdit(str(ppg_val) if ppg_val > 0 else '')
            ppg_entry.setValidator(self.port_validator)
            ppg_entry.setFixedWidth(40)  # Compact: 4 chars max
            groups_entry.setFixedWidth(40)  # Compact: 4 chars max
            self.advanced_layout_uplink_widgets[ut] = {'groups': groups_entry, 'ppg': ppg_entry}
            uplink_layout.addWidget(groups_entry, i, 1)
            uplink_layout.addWidget(ppg_entry, i, 2)
            ppg_entry.textChanged.connect(self._on_advanced_layout_recalculate)
        
        config_layout.addWidget(uplink_group)
        main_layout.addWidget(config_group)
        
        # Live preview section
        preview_group = QGroupBox('Live Preview')
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(5, 5, 5, 5)  # Minimal margins
        preview_layout.setSpacing(5)  # Minimal spacing
        
        self.advanced_layout_canvas_a = ScalableLabel("Fabric A Preview")
        self.advanced_layout_canvas_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.advanced_layout_canvas_a.setFrameShape(QFrame.Shape.StyledPanel)
        self.advanced_layout_canvas_a.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.advanced_layout_canvas_b = ScalableLabel("Fabric B Preview")
        self.advanced_layout_canvas_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.advanced_layout_canvas_b.setFrameShape(QFrame.Shape.StyledPanel)
        self.advanced_layout_canvas_b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        previews_container = QWidget()
        previews_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        previews_hbox = QHBoxLayout(previews_container)
        previews_hbox.setContentsMargins(0, 0, 0, 0)
        previews_hbox.setSpacing(3)  # Very minimal spacing between previews
        previews_hbox.addWidget(self.advanced_layout_canvas_b, 1)
        previews_hbox.addWidget(self.advanced_layout_canvas_a, 1)
        
        preview_layout.addWidget(previews_container)
        main_layout.addWidget(preview_group)
        
        # Clone to Multi-Rack section
        clone_group = QGroupBox("Clone to Multi-Rack Design")
        clone_layout = QHBoxLayout(clone_group)
        
        clone_question_label = QLabel("Clone this cell and add to a Multi Rack Design? How many times:")
        clone_question_label.setToolTip("Number of racks to create in the multi-rack design.")
        clone_layout.addWidget(clone_question_label)
        
        self.advanced_layout_clone_count_entry = QLineEdit()
        self.advanced_layout_clone_count_entry.setValidator(self.numeric_validator)
        self.advanced_layout_clone_count_entry.setText("1")
        self.advanced_layout_clone_count_entry.setFixedWidth(40)
        self.advanced_layout_clone_count_entry.setToolTip("Number of racks to create in the multi-rack design.")
        clone_layout.addWidget(self.advanced_layout_clone_count_entry)
        
        name_label = QLabel("Rack Name:")
        name_label.setToolTip("Base name for racks (max 20 characters, will be suffixed with 1, 2, etc.)")
        clone_layout.addWidget(name_label)
        
        self.advanced_layout_clone_rack_name_entry = QLineEdit()
        self.advanced_layout_clone_rack_name_entry.setMaxLength(20)
        self.advanced_layout_clone_rack_name_entry.setText("Leaf Rack")
        self.advanced_layout_clone_rack_name_entry.setFixedWidth(120)
        self.advanced_layout_clone_rack_name_entry.setToolTip("Base name for racks (max 20 characters, will be suffixed with 1, 2, etc.)")
        clone_layout.addWidget(self.advanced_layout_clone_rack_name_entry)
        
        type_label = QLabel("Type:")
        type_label.setToolTip("Design type: Leaf or Spine")
        clone_layout.addWidget(type_label)
        
        self.advanced_layout_clone_rack_type_combo = QComboBox()
        self.advanced_layout_clone_rack_type_combo.addItems(['leaf', 'spine'])
        self.advanced_layout_clone_rack_type_combo.setToolTip("Design type: Leaf or Spine")
        clone_layout.addWidget(self.advanced_layout_clone_rack_type_combo)
        
        clone_go_button = QPushButton("Go")
        clone_go_button.setToolTip("Add racks to the multi-rack design.")
        clone_go_button.clicked.connect(self._on_advanced_layout_clone_to_multi_rack_go)
        clone_layout.addWidget(clone_go_button)
        
        clone_layout.addStretch()
        main_layout.addWidget(clone_group)
        
        # Initialize the clone rack type to match the current leaf/spine setting
        if hasattr(self, 'leaf_spine_combo'):
            self.advanced_layout_clone_rack_type_combo.setCurrentText(self.leaf_spine_combo.currentText())
        else:
            self.advanced_layout_clone_rack_type_combo.setCurrentText('leaf')
        
        main_layout.addStretch()
        
        return main_widget

    def _on_advanced_layout_dbox_changed(self):
        """Handle DBox type radio button changes."""
        # Only process when a button is actually checked (not when unchecked)
        if self.advanced_layout_dbox_mav.isChecked():
            self.advanced_layout_config['dbox_type'] = 'Mav'
        elif self.advanced_layout_dbox_ceresv1.isChecked():
            self.advanced_layout_config['dbox_type'] = 'CeresV1'
        elif self.advanced_layout_dbox_ceresv2.isChecked():
            self.advanced_layout_config['dbox_type'] = 'CeresV2'
        else:
            return  # No button checked, skip recalculation
        
        # Recalculate immediately with the new DBox type
        self._on_advanced_layout_recalculate()

    def _on_advanced_layout_clone_to_multi_rack_go(self):
        """Clone Advanced Layout tab configuration to multi-rack design."""
        # Read from Advanced Layout tab widgets and call clone function
        # Temporarily sync Advanced Layout data to cell_planning_advanced widgets for cloning
        # This allows reuse of the existing clone logic
        
        # Sync DN count
        if hasattr(self, 'cell_planning_advanced_dn_count'):
            self.cell_planning_advanced_dn_count.setText(self.advanced_layout_dn_count.text())
            self.cell_planning_advanced_dn_split_cb.setChecked(self.advanced_layout_dn_split_cb.isChecked())
            self.cell_planning_advanced_dn_factor.setCurrentText(self.advanced_layout_dn_factor.currentText())
        
        # Sync node counts
        for nt in ['CN', 'EB', 'IE', 'GN']:
            if nt in self.advanced_layout_node_counts and nt in self.cell_planning_advanced_node_counts:
                self.cell_planning_advanced_node_counts[nt].setText(self.advanced_layout_node_counts[nt].text())
                if nt in self.advanced_layout_node_splits and nt in self.cell_planning_advanced_node_splits:
                    self.cell_planning_advanced_node_splits[nt]['split_cb'].setChecked(
                        self.advanced_layout_node_splits[nt]['split_cb'].isChecked())
                    self.cell_planning_advanced_node_splits[nt]['factor'].setCurrentText(
                        self.advanced_layout_node_splits[nt]['factor'].currentText())
                if nt in self.advanced_layout_routing_widgets and nt in self.cell_planning_advanced_routing_widgets:
                    # Sync routing preference
                    adv_left = self.advanced_layout_routing_widgets[nt]['left'].isChecked()
                    self.cell_planning_advanced_routing_widgets[nt]['left'].setChecked(adv_left)
                    self.cell_planning_advanced_routing_widgets[nt]['right'].setChecked(not adv_left)
        
        # Sync uplinks
        for ut in ['IPL', 'ISL', 'EXT']:
            if ut in self.advanced_layout_uplink_widgets and ut in self.cell_planning_advanced_uplink_widgets:
                self.cell_planning_advanced_uplink_widgets[ut]['groups'].setText(
                    self.advanced_layout_uplink_widgets[ut]['groups'].text())
                self.cell_planning_advanced_uplink_widgets[ut]['ppg'].setText(
                    self.advanced_layout_uplink_widgets[ut]['ppg'].text())
        
        # Sync DBox type
        if self.advanced_layout_dbox_mav.isChecked():
            self.cell_planning_advanced_dbox_mav.setChecked(True)
        elif self.advanced_layout_dbox_ceresv1.isChecked():
            self.cell_planning_advanced_dbox_ceresv1.setChecked(True)
        elif self.advanced_layout_dbox_ceresv2.isChecked():
            self.cell_planning_advanced_dbox_ceresv2.setChecked(True)
        
        # Sync clone inputs
        if hasattr(self, 'cell_planning_advanced_clone_count_entry'):
            self.cell_planning_advanced_clone_count_entry.setText(self.advanced_layout_clone_count_entry.text())
            self.cell_planning_advanced_clone_rack_name_entry.setText(self.advanced_layout_clone_rack_name_entry.text())
            self.cell_planning_advanced_clone_rack_type_combo.setCurrentText(
                self.advanced_layout_clone_rack_type_combo.currentText())
        
        # Now call the clone function with advanced mode
        self._on_clone_to_multi_rack_go(mode='advanced')

    def _on_advanced_layout_counts_changed(self):
        """Handle node count changes - recalculate immediately."""
        self._on_advanced_layout_recalculate()

    def _validate_dn_count_even(self):
        """Ensure DN count is always even."""
        dn_count = safe_int(self.advanced_layout_dn_count.text(), 0)
        if dn_count > 0 and dn_count % 2 != 0:
            # Round down to nearest even number
            even_count = dn_count - 1
            self.advanced_layout_dn_count.setText(str(even_count))

    def _get_mellanox_port_order(self, port_count: int) -> list[int]:
        """
        Returns ports in unified column order for Advanced Layout tab (applies to all switch types).
        For 64-port: 16 columns, 4 ports per column (Column 1: 1-4, Column 16: 61-64)
        For 32-port: 16 columns, 2 ports per column (Column 1: 1-2, Column 16: 31-32)
        
        Order: Read down each column (sequential), then next column.
        Column 1: ports 1, 2, 3, 4 (top to bottom)
        Column 2: ports 5, 6, 7, 8
        ...
        Column 16: ports 61, 62, 63, 64 (for 64-port)
        """
        if port_count == 64:
            # 16 columns, 4 ports per column
            # Column 1: 1, 2, 3, 4
            # Column 2: 5, 6, 7, 8
            # ...
            # Column 16: 61, 62, 63, 64
            ports = []
            for col in range(16):  # Columns 1-16
                for row in range(4):  # 4 ports per column
                    port = col * 4 + row + 1
                    ports.append(port)
            return ports
        elif port_count == 32:
            # 16 columns, 2 ports per column
            # Column 1: 1, 2
            # Column 2: 3, 4
            # ...
            # Column 16: 31, 32
            ports = []
            for col in range(16):  # Columns 1-16
                for row in range(2):  # 2 ports per column
                    port = col * 2 + row + 1
                    ports.append(port)
            return ports
        else:
            # Fallback to sequential
            return list(range(1, port_count + 1))

    def _get_left_right_ports_mellanox(self, port_count: int) -> tuple[list[int], list[int]]:
        """
        Returns LEFT and RIGHT port lists for Advanced Layout tab.
        Uses unified column ordering: 16 columns total
        LEFT ports: Columns 1-8 (first half)
        RIGHT ports: Columns 9-16 (second half), reversed so highest ports come first
        """
        all_ports = self._get_mellanox_port_order(port_count)
        if port_count == 64:
            # 16 columns, 4 ports per column = 64 ports total
            # LEFT: Columns 1-8 (ports 1-32 in column order)
            # RIGHT: Columns 9-16 (ports 33-64 in column order), reversed for high-to-low
            left = all_ports[:32]
            right_columns = all_ports[32:]
            right = list(reversed(right_columns))  # Reverse so highest ports come first
            return left, right
        elif port_count == 32:
            # 16 columns, 2 ports per column = 32 ports total
            # LEFT: Columns 1-8 (ports 1-16 in column order)
            # RIGHT: Columns 9-16 (ports 17-32 in column order), reversed for high-to-low
            left = all_ports[:16]
            right_columns = all_ports[16:]
            right = list(reversed(right_columns))  # Reverse so highest ports come first
            return left, right
        else:
            # Fallback: split in half
            mid = len(all_ports) // 2
            left = all_ports[:mid]
            right = list(reversed(all_ports[mid:]))  # Reverse so highest ports come first
            return left, right

    def _on_advanced_layout_recalculate(self):
        """Recalculate port assignments and update live preview."""
        if not self.config_started or not self.base_image:
            if hasattr(self, 'advanced_layout_canvas_a'):
                self.advanced_layout_canvas_a.setText('⬅ Load switch on Setup tab first')
                self.advanced_layout_canvas_b.setText('⬅ Load switch on Setup tab first')
            return
        
        port_map = self._calculate_advanced_layout_ports()
        self.advanced_layout_port_map = port_map
        self._draw_advanced_layout_preview()

    def _calculate_advanced_layout_ports(self) -> list[tuple[int, str]]:
        """
        Calculate port assignments for Advanced Layout tab.
        Rules:
        1. DN odd numbers (DN1, DN3...) -> LEFT side first
        2. DN even numbers (DN2, DN4...) -> RIGHT side first
        3. CN ports next (based on per-DBox routing preferences)
        4. Center remaining ports from RIGHT, using full columns
        5. Uplinks (IPL, ISL, EXT) in center, skipping columns to center them
        """
        port_map = []
        port_count = self.layout_config['PORT_COUNT']
        left_ports, right_ports = self._get_left_right_ports_mellanox(port_count)
        
        # Track assigned ports
        assigned = set()
        
        # Get node counts
        dn_count = safe_int(self.advanced_layout_dn_count.text(), 0)
        node_counts = {nt: safe_int(widget.text(), 0) for nt, widget in self.advanced_layout_node_counts.items()}
        
        # Track current indices for left and right sides
        left_current_index = 0
        right_current_index = 0
        
        # 1. Assign DN ports: Based on DBox type
        dbox_type = self.advanced_layout_config['dbox_type']
        dn_split = self.advanced_layout_dn_split_cb.isChecked()
        dn_factor = safe_int(self.advanced_layout_dn_factor.currentText(), 2) if dn_split else 1
        
        if dn_count > 0:
            # Get DNode groups based on DBox type
            left_dns, right_dns = self._get_dnode_groups_by_dbox_type(dn_count, dbox_type)
            
            # Assign DNs to LEFT side
            if dn_split and dn_factor > 1:
                # Port splitting: take first N DNs from left_dns list for each port
                left_idx = 0
                while left_idx < len(left_dns) and left_current_index < len(left_ports):
                    # Take next dn_factor DNs from the left_dns list
                    dns_for_port = left_dns[left_idx:left_idx + dn_factor]
                    if len(dns_for_port) == 1:
                        label = f'DN-{dns_for_port[0]}'
                    else:
                        label = f'DN-{dns_for_port[0]}/{dns_for_port[-1]}'
                    
                    port = left_ports[left_current_index]
                    port_map.append((port, label))
                    assigned.add(port)
                    left_current_index += 1
                    left_idx += len(dns_for_port)
            else:
                # No splitting: one DN per port
                for dn_num in left_dns:
                    if left_current_index < len(left_ports):
                        port = left_ports[left_current_index]
                        port_map.append((port, f'DN-{dn_num}'))
                        assigned.add(port)
                        left_current_index += 1
            
            # Assign DNs to RIGHT side
            if dn_split and dn_factor > 1:
                # Port splitting: take first N DNs from right_dns list for each port
                right_idx = 0
                while right_idx < len(right_dns) and right_current_index < len(right_ports):
                    # Take next dn_factor DNs from the right_dns list
                    dns_for_port = right_dns[right_idx:right_idx + dn_factor]
                    if len(dns_for_port) == 1:
                        label = f'DN-{dns_for_port[0]}'
                    else:
                        label = f'DN-{dns_for_port[0]}/{dns_for_port[-1]}'
                    
                    port = right_ports[right_current_index]
                    port_map.append((port, label))
                    assigned.add(port)
                    right_current_index += 1
                    right_idx += len(dns_for_port)
            else:
                # No splitting: one DN per port
                for dn_num in right_dns:
                    if right_current_index < len(right_ports):
                        port = right_ports[right_current_index]
                        port_map.append((port, f'DN-{dn_num}'))
                        assigned.add(port)
                        right_current_index += 1
        
        # 2. Assign other node types (CN, EB, IE, GN) based on routing preferences
        # Track current indices for LEFT and RIGHT sides separately
        # left_current_index and right_current_index already updated above
        
        node_types_to_assign = ['CN', 'EB', 'IE', 'GN']
        for nt in node_types_to_assign:
            count = node_counts.get(nt, 0)
            if count == 0:
                continue
            
            # Get split settings
            split = False
            factor = 1
            if nt in self.advanced_layout_node_splits:
                split = self.advanced_layout_node_splits[nt]['split_cb'].isChecked()
                if split and self.advanced_layout_node_splits[nt]['factor']:
                    factor = safe_int(self.advanced_layout_node_splits[nt]['factor'].currentText(), 2)
            
            # Calculate physical ports needed
            phys_ports_needed = math.ceil(count / factor) if split and factor > 1 else count
            
            # Get routing preference for this node type
            routing_pref = 'RIGHT'  # Default
            if nt in self.advanced_layout_routing_widgets:
                nt_widgets = self.advanced_layout_routing_widgets[nt]
                if nt_widgets.get('left', QRadioButton()).isChecked():
                    routing_pref = 'LEFT'
            
            # Assign ports based on preference
            if routing_pref == 'LEFT':
                port_list = left_ports
                port_index = left_current_index
            else:
                port_list = right_ports
                port_index = right_current_index
            
            # Assign physical ports
            node_num = 1
            for phys_port_idx in range(phys_ports_needed):
                # Find next available port that's not assigned
                while port_index < len(port_list) and port_list[port_index] in assigned:
                    port_index += 1
                if port_index >= len(port_list):
                    break  # No more ports available
                
                port = port_list[port_index]
                assigned.add(port)
                
                # Create label(s) for this physical port
                if split and factor > 1:
                    # Multiple nodes per physical port
                    nodes_this_port = min(factor, count - node_num + 1)
                    if nodes_this_port == 1:
                        label = f'{nt}-{node_num}'
                        port_map.append((port, label))
                    else:
                        last_node = node_num + nodes_this_port - 1
                        label = f'{nt}-{node_num}/{last_node}'
                        port_map.append((port, label))
                    node_num += nodes_this_port
                else:
                    # One node per physical port
                    port_map.append((port, f'{nt}-{node_num}'))
                    node_num += 1
                
                port_index += 1
            
            # Update the current index for this side
            if routing_pref == 'LEFT':
                left_current_index = port_index
            else:
                right_current_index = port_index
        
        # 3. Calculate uplink ports needed
        uplink_ports_needed = 0
        for ut in ['IPL', 'ISL', 'EXT']:
            if ut in self.advanced_layout_uplink_widgets:
                # IPL is always 1 group (fixed)
                if ut == 'IPL':
                    groups = 1
                else:
                    groups = safe_int(self.advanced_layout_uplink_widgets[ut]['groups'].text(), 0)
                ppg = safe_int(self.advanced_layout_uplink_widgets[ut]['ppg'].text(), 0)
                uplink_ports_needed += groups * ppg
        
        # 3. Center uplinks from RIGHT, using full columns
        # Use full columns, skip columns to center uplinks
        all_mellanox_order = self._get_mellanox_port_order(port_count)
        available_ports = [p for p in all_mellanox_order if p not in assigned]
        
        # Reverse to start from RIGHT
        available_ports.reverse()
        
        # Assign uplinks in center (from right, skipping columns as needed)
        uplink_labels = []
        for ut in ['IPL', 'ISL', 'EXT']:
            if ut in self.advanced_layout_uplink_widgets:
                # IPL is always 1 group (fixed)
                if ut == 'IPL':
                    groups = 1
                else:
                    groups = safe_int(self.advanced_layout_uplink_widgets[ut]['groups'].text(), 0)
                ppg = safe_int(self.advanced_layout_uplink_widgets[ut]['ppg'].text(), 0)
                for group_num in range(1, groups + 1):
                    for port_num in range(1, ppg + 1):
                        if available_ports:
                            port = available_ports.pop(0)
                            label = f'{ut}{group_num}-{port_num}'
                            uplink_labels.append((port, label))
                            assigned.add(port)
        
        port_map.extend(uplink_labels)
        
        return sorted(port_map, key=lambda x: x[0])

    def _draw_advanced_layout_preview(self):
        """Draw live preview for Advanced Layout tab."""
        if not self.advanced_layout_port_map:
            self.advanced_layout_canvas_a.setText('No ports assigned')
            self.advanced_layout_canvas_b.setText('No ports assigned')
            return
        
        try:
            df_raw = pd.DataFrame(self.advanced_layout_port_map, columns=['Port ID', 'Port Name'])
            df_agg = df_raw.groupby('Port ID')['Port Name'].apply(lambda s: s.iloc[0]).reset_index()
            
            scale_a = self.advanced_layout_canvas_a.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.advanced_layout_canvas_a.width() > 0 else 1.0
            dfA = df_agg.copy()
            dfA['Fabric ID'] = 'A'
            dfA['Hostname'] = 'SwitchA'
            imgA = self._draw_overlay(dfA, self.base_image, self.layout_config, display_scale=scale_a)
            self.advanced_layout_canvas_a.setPixmap(pil_to_qpixmap(imgA))
            
            scale_b = self.advanced_layout_canvas_b.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.advanced_layout_canvas_b.width() > 0 else 1.0
            dfB = df_agg.copy()
            dfB['Fabric ID'] = 'B'
            dfB['Hostname'] = 'SwitchB'
            imgB = self._draw_overlay(dfB, self.base_image, self.layout_config, display_scale=scale_b)
            self.advanced_layout_canvas_b.setPixmap(pil_to_qpixmap(imgB))
        except Exception as e:
            self.advanced_layout_canvas_a.setText(f'Preview error: {e}')
            self.advanced_layout_canvas_b.setText(f'Preview error: {e}')

    def _build_output_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("DarkTab")
        main_layout = QVBoxLayout(main_widget)

        # --- Top Button Layout ---
        top_button_layout = QHBoxLayout()
        self.gen_overlay_button = QPushButton('Generate overlays & export')
        self.gen_overlay_button.setToolTip("Generate and save the final PNG diagrams for both switches to the selected output folder.")
        self.gen_overlay_button.clicked.connect(lambda: self.generate_overlays_and_export(export_files=True))
        self.export_json_button = QPushButton('Export JSON Config')
        self.export_json_button.setToolTip("Save all current UI settings to a JSON file, which can be imported later.")
        self.export_json_button.clicked.connect(self._export_config_to_json)
        self.create_config_button = QPushButton('Create Switch Configs')
        self.create_config_button.setToolTip("Generate a configuration script and execute it to produce the final switch configuration files.")
        self.create_config_button.clicked.connect(self._generate_switch_config)
        top_button_layout.addWidget(self.gen_overlay_button)
        top_button_layout.addWidget(self.export_json_button)
        top_button_layout.addWidget(self.create_config_button)
        main_layout.addLayout(top_button_layout)

        # --- Multi-Rack Selector ---
        self.output_rack_selector_widget = QWidget()
        output_rack_selector_layout = QHBoxLayout(self.output_rack_selector_widget)
        output_rack_selector_layout.setContentsMargins(0, 5, 0, 5)
        output_rack_selector_layout.addWidget(QLabel("View Summary for Rack:"))
        self.output_rack_selector_combo = QComboBox()
        self.output_rack_selector_combo.currentTextChanged.connect(self._on_output_rack_selected)
        output_rack_selector_layout.addWidget(self.output_rack_selector_combo, 1)
        output_rack_selector_layout.addStretch()
        main_layout.addWidget(self.output_rack_selector_widget)

        # --- Main Content Area (Previews + Bandwidth) ---
        content_hbox = QHBoxLayout()

        # Previews (take up the majority of space)
        previews_container = QWidget()
        previews_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        previews_vbox = QVBoxLayout(previews_container)
        previews_vbox.setContentsMargins(0, 10, 0, 0)
        self.canvas_a = ScalableLabel("Final Fabric A Layout")
        self.canvas_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.canvas_a.setFrameShape(QFrame.Shape.StyledPanel)
        self.canvas_a.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.canvas_b = ScalableLabel("Final Fabric B Layout")
        self.canvas_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.canvas_b.setFrameShape(QFrame.Shape.StyledPanel)
        self.canvas_b.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        previews_vbox.addWidget(self.canvas_b)
        previews_vbox.addWidget(self.canvas_a)
        content_hbox.addWidget(previews_container, 80) # 80% of horizontal space

        # Bandwidth Summary (takes up a smaller portion on the right)
        bw_group = QGroupBox("BW Summary Per Switch Pair")
        bw_group.setToolTip("This panel audits your current port design against the 'Max BW Required Per Rack/Cell' goal set on the Setup tab.\n\n"
                            "- Per SW: Shows the total bandwidth for a single switch.\n"
                            "- Aggr: Shows the total aggregate bandwidth for the switch pair. The audit check (✓/X) is based on this value.\n"
                            "- HA (High Availability): Simulates a single switch failure, showing if the goal is still met with 50% of the aggregate bandwidth.\n\n"
                            "All values are displayed in the units (GB/s or GiB/s) selected on the Setup tab.")
        bw_group.setFixedWidth(250) # Fixed width for the summary panel
        bw_layout = QGridLayout(bw_group)
        bw_layout.setColumnStretch(4, 1)

        # Use a smaller font for the bandwidth values to prevent text overlap.
        small_font = QFont()
        small_font.setPointSize(10)
        # Create a list of labels that will get the smaller font.
        bw_value_labels = []

        self.bw_target_label = QLabel("0 GB/s")
        self.bw_target_audit = QLabel("")
        self.bw_nb_a_label = QLabel("0 GB/s")
        self.bw_nb_a_audit = QLabel("")
        self.bw_nb_b_label = QLabel("0 GB/s")
        self.bw_nb_b_audit = QLabel("")
        self.bw_isl_a_label = QLabel("0 Tb/s")
        self.bw_isl_per_switch_audit = QLabel("")
        self.bw_isl_a_ha_audit = QLabel("")
        self.bw_isl_b_label = QLabel("0 Tb/s")
        self.bw_isl_aggregate_audit = QLabel("")
        self.bw_isl_b_ha_audit = QLabel("")
        self.bw_ext_a_label = QLabel("0 Tb/s")
        self.bw_ext_a_audit = QLabel("")
        self.bw_ext_a_ha_audit = QLabel("")
        self.bw_ext_b_label = QLabel("0 Tb/s")
        self.bw_ext_b_audit = QLabel("")
        self.bw_ext_b_ha_audit = QLabel("")

        # Add all the value labels to the list for font change
        bw_value_labels.extend([self.bw_target_label, self.bw_nb_a_label, self.bw_nb_b_label,
                                self.bw_isl_a_label, self.bw_isl_b_label, self.bw_ext_a_label, self.bw_ext_b_label])

        # HA Header with a smaller, superscript help icon using rich text
        ha_header_label = QLabel('HA<sup style="font-size: 8pt; vertical-align: super;">❔</sup>')
        ha_header_label.setToolTip("This column checks if your target BW is available, even if a switch fails")
        ha_header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bw_layout.addWidget(ha_header_label, 0, 3)

        bw_layout.addWidget(QLabel("BW Goal:"), 0, 0)
        bw_layout.addWidget(self.bw_target_label, 0, 1)
        bw_layout.addWidget(self.bw_target_audit, 0, 2)
        bw_layout.addWidget(QLabel("NB (Per SW):"), 1, 0)
        bw_layout.addWidget(self.bw_nb_a_label, 1, 1)
        bw_layout.addWidget(self.bw_nb_a_audit, 1, 2)
        bw_layout.addWidget(QLabel("NB (Aggr):"), 2, 0)
        bw_layout.addWidget(self.bw_nb_b_label, 2, 1)
        bw_layout.addWidget(self.bw_nb_b_audit, 2, 2)
        bw_layout.addWidget(QLabel("ISL (Per SW):"), 3, 0)
        bw_layout.addWidget(self.bw_isl_a_label, 3, 1)
        bw_layout.addWidget(self.bw_isl_per_switch_audit, 3, 2)
        bw_layout.addWidget(self.bw_isl_a_ha_audit, 3, 3)
        bw_layout.addWidget(QLabel("ISL (Aggr):"), 4, 0)
        bw_layout.addWidget(self.bw_isl_b_label, 4, 1)
        bw_layout.addWidget(self.bw_isl_aggregate_audit, 4, 2)
        bw_layout.addWidget(self.bw_isl_b_ha_audit, 4, 3)
        bw_layout.addWidget(QLabel("Ext (Per SW):"), 5, 0)
        bw_layout.addWidget(self.bw_ext_a_label, 5, 1)
        bw_layout.addWidget(self.bw_ext_a_audit, 5, 2)
        bw_layout.addWidget(self.bw_ext_a_ha_audit, 5, 3)
        bw_layout.addWidget(QLabel("Ext (Aggr):"), 6, 0)
        bw_layout.addWidget(self.bw_ext_b_label, 6, 1)
        bw_layout.addWidget(self.bw_ext_b_audit, 6, 2)
        bw_layout.addWidget(self.bw_ext_b_ha_audit, 6, 3)
        bw_layout.setRowStretch(7, 1)

        # Apply the smaller font to all the bandwidth value labels
        for label in bw_value_labels:
            label.setFont(small_font)

        content_hbox.addWidget(bw_group, 20) # 20% of horizontal space
        main_layout.addLayout(content_hbox)

        # --- Bottom Directory Layout ---
        dir_layout = QHBoxLayout()
        select_dir_button = QPushButton('Select output folder')
        select_dir_button.setToolTip("Choose the destination directory for all generated files.")
        select_dir_button.clicked.connect(self.select_output_directory)
        self.out_dir_label = QLabel(self.out_dir)
        dir_layout.addWidget(select_dir_button)
        dir_layout.addWidget(self.out_dir_label)
        main_layout.addLayout(dir_layout)

        return main_widget

    def export_csv_xlsx(self):
        is_multi_rack = self.multi_rack_checkbox.isChecked()
        if is_multi_rack:
            rack_name = self.output_rack_selector_combo.currentText()
            if not rack_name or rack_name not in self.multi_rack_config:
                QMessageBox.critical(self, 'Error', 'No rack selected or data available to export.')
                return
            port_map_to_export = self.multi_rack_config[rack_name].get('port_map', [])
            hostname_a = self.multi_rack_config[rack_name].get('hostname_a', 'FabricA')
            hostname_b = self.multi_rack_config[rack_name].get('hostname_b', 'FabricB')
        else:
            port_map_to_export = self.port_map
            hostname_a = self.ha_entry.text().strip() or 'FabricA'
            hostname_b = self.hb_entry.text().strip() or 'FabricB'

        if not port_map_to_export:
            QMessageBox.critical(self, 'Error', 'No port data to export')
            return
        try:
            df_raw = pd.DataFrame(port_map_to_export, columns=['Port ID', 'Port Name'])
            df_export_a = df_raw.copy()
            df_export_a['Hostname'] = hostname_a
            df_export_a['Fabric ID'] = 'A'
            df_export_a = df_export_a.rename(columns={'Port ID': 'Port ID (A)', 'Port Name': 'Port Name (A)', 'Fabric ID': 'Fabric ID (A)', 'Hostname': 'Hostname (A)'})

            df_export_b = df_raw.copy()
            df_export_b['Hostname'] = hostname_b
            df_export_b['Fabric ID'] = 'B'
            df_export_b = df_export_b.rename(columns={'Port ID': 'Port ID (B)', 'Port Name': 'Port Name (B)', 'Fabric ID': 'Fabric ID (B)', 'Hostname': 'Hostname (B)'})

            df_combined = pd.concat([df_export_a.reset_index(drop=True), df_export_b.reset_index(drop=True)], axis=1)
            df_combined.insert(0, 'Switch Model', self.layout_config['NAME'])
            ls_type = self.leaf_spine_combo.currentText()
            cluster_name = self.cluster_name_entry.text().strip() or 'UnnamedCluster'
            host_part = f'{hostname_a}-{hostname_b}' if hostname_b and hostname_b != 'FabricB' else hostname_a
            
            # Create descriptive filename with cluster, switch, leaf/spine names
            base_filename = f'{cluster_name}_{host_part}_{ls_type}'

            # Use the new cluster-specific output directory
            os.makedirs(self._cluster_output_dir, exist_ok=True)
            csv_filename = get_unique_filename(os.path.join(self._cluster_output_dir, f'{base_filename}.csv'))
            xlsx_filename = get_unique_filename(os.path.join(self._cluster_output_dir, f'{base_filename}.xlsx'))
            df_combined.to_csv(csv_filename, index=False)
            df_combined.to_excel(xlsx_filename, index=False)

            self._show_timed_messagebox('Success', f'Data exported to:\n{os.path.relpath(csv_filename)}\n{os.path.relpath(xlsx_filename)}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to export data: {e}')

    def _export_config_to_json(self, filepath: Union[str, bool] = False):
        """Gathers the current UI state and exports it to a JSON file."""
        if not isinstance(filepath, str):
            # Generate a filename automatically instead of showing a dialog.
            # Use cluster name, hostname, or a default, and ensure it's a valid filename.
            ls_type = self.leaf_spine_combo.currentText()
            cluster_name = self.cluster_name_entry.text().strip() or 'UnnamedCluster'
            hostname_a = self.ha_entry.text().strip() or 'FabricA'
            hostname_b = self.hb_entry.text().strip() or 'FabricB'
            
            # Create descriptive filename with cluster, switch, leaf/spine names
            base_name = f"{cluster_name}_{hostname_a}_{hostname_b}_{ls_type}".replace(' ', '_').strip('_')
            # Add a suffix for multi-rack configurations
            if self.multi_rack_checkbox.isChecked():
                base_name += '_MR'
            # Construct the full path within the designated output directory.
            json_filename = f"{base_name}_config.json"
            # Use the new cluster-specific output directory
            os.makedirs(self._cluster_output_dir, exist_ok=True)
            filepath = get_unique_filename(os.path.join(self._cluster_output_dir, json_filename))

        try:
            config = {
                'metadata': {
                    'version': '1.1',
                    'created_timestamp': datetime.now().isoformat(),
                    'app_version': SCRIPT_VERSION,
                    'switch_model': self.layout_config['NAME'],
                    'switch_id': self.switch_id,
                    'total_ports': self.layout_config['PORT_COUNT'],
                    'config_name': os.path.basename(filepath).replace('.json', ''),
                    'description': f'Exported configuration from Port-Mapper v{SCRIPT_VERSION}'
                },
                'setup_values': {
                    'customer_name': self.customer_name_entry.text(),
                    'site_name': self.site_name_entry.text(),
                    'hostname_a': self.ha_entry.text(),
                    'hostname_b': self.hb_entry.text(),
                    'switch_os': self.vendor_combo.currentText(),
                    'mgmt_default_route': self.net_def_route_entry.text(),
                    'network_cidr': self.net_cidr_combo.currentText(),
                    'fabric_a_mgmt_ip': self.switch_a_mgmt_ip_entry.text(),
                    'fabric_b_mgmt_ip': self.switch_b_mgmt_ip_entry.text(),
                    'cluster_name': self.cluster_name_entry.text(),
                    'ntp_server_ip': self.ntp_server_entry.text(),
                    'leafs_or_spines': self.leaf_spine_combo.currentText(),
                    'uplink_speed': self.uplink_speed_combo.currentText(),
                    'customer_vlans': self.customer_vlans_entry.text(),
                    'bgp_asn': self.bgp_asn_entry.text(),
                    'data_vlan': self.data_vlan_entry.text(),
                    'vxlan': self.vxlan_checkbox.isChecked(), 'pfc': self.pfc_checkbox.isChecked(),
                    'use_2nd_nic': 'Yes' if self.use_2nd_nic_checkbox.isChecked() else 'No',
                    'use_converged_networking': self.use_converged_networking_checkbox.isChecked(),
                    'fabric_topology': self.fabric_topology,
                    'use_vxlan_overlay': self.use_vxlan_overlay,
                    'peak_bw_goal': self.peak_bw_goal_entry.text(),
                    'peak_bw_units': self.peak_bw_units_combo.currentText(),
                    'multi_rack_enabled': self.multi_rack_checkbox.isChecked(),
                    'legacy_mode_enabled': self.legacy_mode_checkbox.isChecked(),
                    'mapping_mode': self.cell_planning_mode,  # NEW: Export current mode
                },
                'node_types': {},
                'uplink_types': {}
            }

            for nt, ent in self.node_entries.items():
                config['node_types'][nt] = {
                    'count': safe_int(ent['cnt'].text()),
                    'split': ent['split_cb'].isChecked(),
                    'factor': safe_int(ent['fac'].currentText(), 1),
                    'reserved': safe_int(ent['rsv'].text()),
                    'manual_ports': ent['st'].text().strip(),
                    'locked': ent['lock_cb'].isChecked()
                }

            for ut, ent in self.uplink_entries.items():
                config['uplink_types'][ut] = {
                    'groups': safe_int(ent['gcnt'].text()) if ut not in ['IPL', 'NB'] else 1,
                    'ports_per_group': safe_int(ent['ppg'].text()),
                    'split': ent['split_cb'].isChecked(),
                    'factor': safe_int(ent['fac'].currentText(), 1),
                    'reserved': safe_int(ent['rsv'].text()),
                    'manual_ports': ent['st'].text().strip(),
                    'locked': ent['lock_cb'].isChecked()
                }

            # If multi-rack is enabled, save the entire multi-rack configuration.
            # We remove the 'port_map' from each rack as it's calculated on the fly.
            if self.multi_rack_checkbox.isChecked():
                config['multi_rack_config'] = {}
                for rack_name, rack_data in self.multi_rack_config.items():
                    # Create a copy and remove the calculated port_map before saving
                    config['multi_rack_config'][rack_name] = {k: v for k, v in rack_data.items() if k != 'port_map'}
            
            # Export advanced config if in advanced mode
            if self.cell_planning_mode == 'advanced':
                config['advanced_config'] = {
                    'dbox_type': self.cell_planning_advanced_config['dbox_type'],
                    'node_routing': {},
                    'uplinks': self.cell_planning_advanced_config['uplinks'].copy()
                }
                # Collect routing preferences
                for nt in ['CN', 'EB', 'IE', 'GN']:
                    if nt in self.cell_planning_advanced_routing_widgets:
                        nt_widgets = self.cell_planning_advanced_routing_widgets[nt]
                        if nt_widgets.get('left', QRadioButton()).isChecked():
                            config['advanced_config']['node_routing'][nt] = 'LEFT'
                        else:
                            config['advanced_config']['node_routing'][nt] = 'RIGHT'
            
            # --- Add Legacy Install Values ---
            config['legacy_install_values'] = {
                'customer': self.legacy_customer.text(),
                'cluster_name': self.legacy_cluster_name.text(),
                'cluster_label': self.legacy_cluster_label.text(),
                'release': self.legacy_release.text(),
                'buildfile': self.legacy_buildfile.text(),
                'cnode_count': self.legacy_cnode_count.text(),
                'dbox_type': self.legacy_dbox_type.currentText(),
                'ceres_version': self.legacy_ceres_version.currentText(),
                'dbox_count': self.legacy_dbox_count.text(),
                'hostname_template': self.legacy_hostname_template.text(),
                'mgmt_ip_cnode': self.legacy_mgmt_ip_cnode.text(),
                'mgmt_ip_dnode': self.legacy_mgmt_ip_dnode.text(),
                'mgmt_netmask': self.legacy_mgmt_netmask.text(),
                'dns': self.legacy_dns.text(),
                'ntp': self.legacy_ntp.text(),
                'ext_gateway': self.legacy_ext_gateway.text(),
                'b2b_ipmi': self.legacy_b2b_ipmi.isChecked(),
                'vm_vip': self.legacy_vm_vip.text(),
                'switch1': self.legacy_switch1.text(),
                'switch2': self.legacy_switch2.text(),
                'mellanox_switches': self.legacy_mellanox_switches.isChecked(),
                'switch_os': self.legacy_switch_os.currentText(),
                'skip_nic': self.legacy_skip_nic.isChecked(),
                'rdma_pfc': self.legacy_rdma_pfc.isChecked(),
                'auto_ports': self.legacy_auto_ports.currentText(),
                'ib_mode': self.legacy_ib_mode.currentText(),
                'ib_mtu': self.legacy_ib_mtu.text(),
                'eth_mtu': self.legacy_eth_mtu.text(),
                'vxlan': self.legacy_vxlan.isChecked(),
                'change_template': self.legacy_change_template.isChecked(),
                'template': self.legacy_template.text(),
                'mgmt_inner_vip': self.legacy_mgmt_inner_vip.text(),
                'docker_bip': self.legacy_docker_bip.text(),
                'change_vlan': self.legacy_change_vlan.isChecked(),
                'vlan_id': self.legacy_vlan_id.text(),
                'isolcpu': self.legacy_isolcpu.text(),
            }

            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)

            self._show_timed_messagebox('Export Successful', f'Configuration successfully exported to:\n{os.path.relpath(filepath)}')

        except Exception as e:
            QMessageBox.critical(self, 'Export Error', f'Failed to export configuration:\n{e}')

    def _import_config_from_json(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Import Port Configuration', self.out_dir, "JSON Files (*.json);;All Files (*)")
        if not filepath:
            return

        try:
            with open(filepath, 'r') as f:
                config = json.load(f)

            # --- Validation ---
            config_switch_name = config.get('metadata', {}).get('switch_model')
            if not config_switch_name:
                QMessageBox.critical(self, 'Import Error', "The JSON file is missing the 'switch_model' in its metadata.")
                return

            if config_switch_name != self.layout_config['NAME']:
                # If the model in the JSON is different, automatically switch to it.
                # The JSON is considered the source of truth.
                if not any(v['NAME'] == config_switch_name for v in SWITCH_LAYOUTS.values()):
                    QMessageBox.critical(self, 'Import Error', f"The switch model '{config_switch_name}' from the JSON file is not supported by this tool.")
                    return
                self.switch_var_combo.setCurrentText(config_switch_name)

            # --- Preview ---
            preview_text, warnings = self._get_import_preview_text(config)
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Import Preview')
            msg_box.setText('Apply the following configuration?')
            msg_box.setInformativeText(preview_text)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel)
            # If there are warnings, make Cancel the default button
            msg_box.setDefaultButton(QMessageBox.StandardButton.Cancel if warnings else QMessageBox.StandardButton.Apply)
            reply = msg_box.exec()

            if reply == QMessageBox.StandardButton.Cancel:
                return

            # --- Apply ---
            self._apply_import_config(config)
            self.notebook.setCurrentIndex(self.notebook.indexOf(self.output_tab))

        except json.JSONDecodeError as e:
            QMessageBox.critical(self, 'Invalid JSON', f'Failed to parse JSON file:\n{e}')
        except Exception as e:
            QMessageBox.critical(self, 'Import Error', f'Failed to import configuration:\n{e}')

    def _format_import_preview_details(self, port_types: dict, is_node: bool) -> list[str]:
        """Helper to format the details for node or uplink types in the import preview."""
        lines = []
        for type_name, data in port_types.items():
            # Determine the primary count value based on type
            count = data.get('count', 0) if is_node else data.get('ports_per_group', 0)
            reserved = data.get('reserved', 0)
            if count <= 0 and reserved <= 0:
                continue

            details = []
            if not is_node:
                groups = data.get('groups', 1)
                if groups > 1:
                    details.append(f"{groups} groups")

            if data.get('split'):
                details.append(f"Split 1:{data.get('factor', 1)}")
            if reserved > 0:
                details.append(f"Reserved: {reserved}")
            if data.get('locked'):
                details.append(f"🔒 Locked: {data.get('manual_ports', 'N/A')}")

            details_str = f" ({', '.join(details)})" if details else ""
            unit = "nodes" if is_node else "ports per group"
            lines.append(f"&nbsp;&nbsp;<b>{type_name}:</b> {count} {unit}{details_str}<br>")
        return lines

    def _get_import_preview_text(self, config: dict) -> tuple[str, list[str]]:
        """Generates a summary string for the import preview dialog."""
        metadata = config.get('metadata', {})
        info_lines = [
            f"<b>Configuration:</b> {metadata.get('config_name', 'Unknown')}<br>",
            f"<b>Switch Model:</b> {metadata.get('switch_model', 'Unknown')}<br>",
            f"<b>Description:</b> {metadata.get('description', 'No description')}<br><br>"
        ]

        if 'setup_values' in config:
            sv = config['setup_values']
            info_lines.append('<b>Setup Values:</b><br>')
            info_lines.append(f"&nbsp;&nbsp;Hostnames: {sv.get('hostname_a', 'N/A')}, {sv.get('hostname_b', 'N/A')}<br>")
            info_lines.append(f"&nbsp;&nbsp;Switch OS: {sv.get('switch_os', 'N/A')}<br>")
            info_lines.append(f"&nbsp;&nbsp;Cluster: {sv.get('cluster_name', 'N/A')}<br>")

        info_lines.append('<br><b>Node Types:</b><br>')
        info_lines.extend(self._format_import_preview_details(config.get('node_types', {}), is_node=True))

        info_lines.append('<br><b>Uplinks:</b><br>')
        info_lines.extend(self._format_import_preview_details(config.get('uplink_types', {}), is_node=False))

        # --- Perform Validation ---
        warnings = self._validate_import_config(config)
        if warnings:
            info_lines.append("<br><hr><b><font color='orange'>Warnings Found:</font></b><br>")
            for warning in warnings:
                info_lines.append(f"&nbsp;&nbsp;• {warning}<br>")

        return "".join(info_lines), warnings

    def _validate_import_config(self, config: dict) -> list[str]:
        """
        Validates a loaded configuration dictionary for common errors before import.
        Returns a list of warning strings.
        """
        warnings = []
        assigned_ports = {} # port -> type_name

        all_types = {**config.get('node_types', {}), **config.get('uplink_types', {})}

        for type_name, data in all_types.items():
            if not data.get('locked'):
                continue

            is_node = type_name in config.get('node_types', {})
            count = data.get('count', 0) if is_node else data.get('ports_per_group', 0)
            groups = data.get('groups', 1) if not is_node else 1
            reserved = data.get('reserved', 0)
            split = data.get('split', False)
            factor = data.get('factor', 1) if split else 1

            phys_per_group = math.ceil(count / factor) if (is_node and split) else count
            total_phys_needed = (phys_per_group + reserved) * groups

            manual_ports_str = data.get('manual_ports', '')
            parsed_ports = _parse_port_string(manual_ports_str)

            # Check if this is Mode 1 (single starting port) or Mode 2 (full port list)
            is_single_number = len(parsed_ports) == 1 and not ('-' in manual_ports_str or ',' in manual_ports_str)
            
            if is_single_number:
                # Mode 1: Single starting port - no validation needed as it's auto-assignment
                # The single port is just the starting point, not the complete assignment
                pass
            else:
                # Mode 2: Full port list - validate that the count matches
                if len(parsed_ports) != total_phys_needed:
                    warnings.append(f"<b>{type_name}:</b> Count mismatch. Requires {total_phys_needed} ports, but {len(parsed_ports)} are assigned.")

            for port in parsed_ports:
                if port in assigned_ports:
                    warnings.append(f"<b>Port {port}:</b> Overlap between '{type_name}' and '{assigned_ports[port]}'.")
                else:
                    assigned_ports[port] = type_name
        return warnings

    def _apply_import_config(self, config: dict):
        """Sets the UI state from a loaded configuration dictionary."""
        # Load switch and reset everything first
        self.load_switch_and_prepare()

        # Apply setup values
        imported_mode = 'default'  # Initialize mode
        if 'setup_values' in config:
            sv = config['setup_values']
            self.customer_name_entry.setText(sv.get('customer_name', ''))
            self.site_name_entry.setText(sv.get('site_name', ''))
            self.ha_entry.setText(sv.get('hostname_a', ''))
            self.hb_entry.setText(sv.get('hostname_b', ''))

            # Set switch_os from JSON. If the OS from the file is not valid for the
            # selected switch model, setCurrentText will do nothing, and the
            # default OS for the model will be used instead. This is the desired behavior.
            switch_os_from_json = sv.get('switch_os', '')
            if switch_os_from_json:
                self.vendor_combo.setCurrentText(switch_os_from_json)

            self.net_def_route_entry.setText(sv.get('mgmt_default_route', ''))
            self.net_cidr_combo.setCurrentText(sv.get('network_cidr', '24'))
            self.switch_a_mgmt_ip_entry.setText(sv.get('fabric_a_mgmt_ip', ''))
            self.switch_b_mgmt_ip_entry.setText(sv.get('fabric_b_mgmt_ip', ''))
            self.cluster_name_entry.setText(sv.get('cluster_name', ''))
            self.ntp_server_entry.setText(sv.get('ntp_server_ip', ''))
            self.leaf_spine_combo.setCurrentText(sv.get('leafs_or_spines', 'leaf'))
            self.uplink_speed_combo.setCurrentText(sv.get('uplink_speed', ''))
            self.customer_vlans_entry.setText(sv.get('customer_vlans', ''))
            self.bgp_asn_entry.setText(sv.get('bgp_asn', ''))
            self.data_vlan_entry.setText(sv.get('data_vlan', '69'))
            self.vxlan_checkbox.setChecked(sv.get('vxlan', False))
            self.pfc_checkbox.setChecked(sv.get('pfc', False))
            self.use_2nd_nic_checkbox.setChecked(sv.get('use_2nd_nic', 'No') == 'Yes')
            self.use_converged_networking_checkbox.setChecked(sv.get('use_converged_networking', False))
            fabric_topology = sv.get('fabric_topology', 'single_pair')
            if fabric_topology == 'leaf_spine':
                self.fabric_spine_radio.setChecked(True)
            else:
                self.fabric_single_radio.setChecked(True)
            overlay_flag = sv.get('use_vxlan_overlay', False)
            if self.fabric_overlay_checkbox.isEnabled():
                self.fabric_overlay_checkbox.setChecked(overlay_flag)
            else:
                self.fabric_overlay_checkbox.blockSignals(True)
                self.fabric_overlay_checkbox.setChecked(False)
                self.fabric_overlay_checkbox.blockSignals(False)
                self.use_vxlan_overlay = False
            self.peak_bw_goal_entry.setText(sv.get('peak_bw_goal', ''))
            self.peak_bw_units_combo.setCurrentText(sv.get('peak_bw_units', 'GB/s'))
            self.multi_rack_checkbox.setChecked(sv.get('multi_rack_enabled', False))
            self.legacy_mode_checkbox.setChecked(sv.get('legacy_mode_enabled', False))
            # Apply mapping mode and advanced config
            imported_mode = sv.get('mapping_mode', 'default')
            self.cell_planning_mode = imported_mode
            if hasattr(self, 'cell_planning_mode_default_radio') and hasattr(self, 'cell_planning_mode_advanced_radio'):
                if imported_mode == 'advanced':
                    self.cell_planning_mode_advanced_radio.setChecked(True)
                    self.cell_planning_stacked.setCurrentIndex(1)
                else:
                    self.cell_planning_mode_default_radio.setChecked(True)
                    self.cell_planning_stacked.setCurrentIndex(0)
            self._update_vxlan_checkbox_state()
            
            # Apply advanced config if present
            if 'advanced_config' in config and imported_mode == 'advanced':
                adv_config = config['advanced_config']
                # Set DBox type
                dbox_type = adv_config.get('dbox_type', 'CeresV1')
                if hasattr(self, 'cell_planning_advanced_dbox_mav'):
                    if dbox_type == 'Mav':
                        self.cell_planning_advanced_dbox_mav.setChecked(True)
                    elif dbox_type == 'CeresV1':
                        self.cell_planning_advanced_dbox_ceresv1.setChecked(True)
                    elif dbox_type == 'CeresV2':
                        self.cell_planning_advanced_dbox_ceresv2.setChecked(True)
                    self.cell_planning_advanced_config['dbox_type'] = dbox_type
                
                # Apply routing preferences
                node_routing = adv_config.get('node_routing', {})
                for nt, direction in node_routing.items():
                    if nt in self.cell_planning_advanced_routing_widgets:
                        nt_widgets = self.cell_planning_advanced_routing_widgets[nt]
                        if direction == 'LEFT':
                            nt_widgets['left'].setChecked(True)
                        else:
                            nt_widgets['right'].setChecked(True)
                    self.cell_planning_advanced_config['node_routing'][nt] = direction

        # Apply node types
        for nt, data in config.get('node_types', {}).items():
            if nt in self.node_entries:
                ent = self.node_entries[nt]
                ent['cnt'].setText(str(data.get('count', 0)))
                ent['split_cb'].setChecked(data.get('split', False))
                ent['fac'].setCurrentText(str(data.get('factor', 2)))
                ent['rsv'].setText(str(data.get('reserved', 0)))
                ent['lock_cb'].setChecked(data.get('locked', False))
                if ent['lock_cb'].isChecked():
                    ent['st'].setText(data.get('manual_ports', ''))
            
            # Always populate advanced mode UI as well (for mode carry-over)
            if nt == 'DN' and hasattr(self, 'cell_planning_advanced_dn_count'):
                self.cell_planning_advanced_dn_count.setText(str(data.get('count', 0)))
                if hasattr(self, 'cell_planning_advanced_dn_split_cb'):
                    self.cell_planning_advanced_dn_split_cb.setChecked(data.get('split', False))
                if hasattr(self, 'cell_planning_advanced_dn_factor'):
                    self.cell_planning_advanced_dn_factor.setCurrentText(str(data.get('factor', 2)))
            elif nt in ['CN', 'EB', 'IE', 'GN'] and nt in self.cell_planning_advanced_node_counts:
                self.cell_planning_advanced_node_counts[nt].setText(str(data.get('count', 0)))
                if nt in self.cell_planning_advanced_node_splits:
                    self.cell_planning_advanced_node_splits[nt]['split_cb'].setChecked(data.get('split', False))
                    self.cell_planning_advanced_node_splits[nt]['factor'].setCurrentText(str(data.get('factor', 2)))

        # Apply uplink types
        for ut, data in config.get('uplink_types', {}).items():
            if ut in self.uplink_entries:
                ent = self.uplink_entries[ut]
                if 'gcnt' in ent: ent['gcnt'].setText(str(data.get('groups', 1)))
                ent['ppg'].setText(str(data.get('ports_per_group', 0)))
                if 'split_cb' in ent: ent['split_cb'].setChecked(data.get('split', False))
                if 'fac' in ent: ent['fac'].setCurrentText(str(data.get('factor', 2)))
                ent['rsv'].setText(str(data.get('reserved', 0)))
                ent['lock_cb'].setChecked(data.get('locked', False))
                if ent['lock_cb'].isChecked():
                    ent['st'].setText(data.get('manual_ports', ''))
            
            # Always populate advanced mode UI as well (for mode carry-over)
            # Map MLAG/BGP to EXT for advanced UI
            lookup_key = 'EXT' if ut == 'MLAG/BGP' else ut
            if lookup_key in self.cell_planning_advanced_uplink_widgets:
                groups_widget = self.cell_planning_advanced_uplink_widgets[lookup_key]['groups']
                ppg_widget = self.cell_planning_advanced_uplink_widgets[lookup_key]['ppg']
                groups_val = data.get('groups', 1 if ut == 'IPL' else 0)
                groups_widget.setText(str(groups_val))
                ppg_widget.setText(str(data.get('ports_per_group', 0)))
                # Update config
                self.cell_planning_advanced_config['uplinks'][lookup_key] = {
                    'groups': safe_int(str(groups_val), 1 if ut == 'IPL' else 0),
                    'ports_per_group': safe_int(str(data.get('ports_per_group', 0)), 0)
                }

        # Apply multi-rack configuration if it exists in the file
        if 'multi_rack_config' in config and self.multi_rack_checkbox.isChecked():
            # Clear any existing multi-rack state before importing
            self.rack_list_widget.clear()
            for rack_name, rack_widgets in self.rack_widgets.items():
                rack_widgets['widget'].deleteLater()
            self.rack_widgets.clear()
            self.multi_rack_config.clear()

            self.multi_rack_config = config['multi_rack_config']
            for rack_name in self.multi_rack_config.keys():
                self.rack_list_widget.addItem(rack_name)
                self._create_rack_detail_widget(rack_name)
                self._calculate_and_store_rack_port_map(rack_name)

        # Apply legacy install values
        if 'legacy_install_values' in config:
            lv = config['legacy_install_values']
            self.legacy_customer.setText(lv.get('customer', ''))
            self.legacy_cluster_name.setText(lv.get('cluster_name', ''))
            self.legacy_cluster_label.setText(lv.get('cluster_label', ''))
            self.legacy_release.setText(lv.get('release', ''))
            self.legacy_buildfile.setText(lv.get('buildfile', ''))
            self.legacy_cnode_count.setText(lv.get('cnode_count', ''))
            self.legacy_dbox_type.setCurrentText(lv.get('dbox_type', 'Ceres'))
            self.legacy_ceres_version.setCurrentText(lv.get('ceres_version', 'v1'))
            self.legacy_dbox_count.setText(lv.get('dbox_count', ''))
            self.legacy_hostname_template.setText(lv.get('hostname_template', ''))
            self.legacy_mgmt_ip_cnode.setText(lv.get('mgmt_ip_cnode', ''))
            self.legacy_mgmt_ip_dnode.setText(lv.get('mgmt_ip_dnode', ''))
            self.legacy_mgmt_netmask.setText(lv.get('mgmt_netmask', ''))
            self.legacy_dns.setText(lv.get('dns', ''))
            self.legacy_ntp.setText(lv.get('ntp', ''))
            self.legacy_ext_gateway.setText(lv.get('ext_gateway', ''))
            self.legacy_b2b_ipmi.setChecked(lv.get('b2b_ipmi', True))
            self.legacy_vm_vip.setText(lv.get('vm_vip', ''))
            self.legacy_switch1.setText(lv.get('switch1', ''))
            self.legacy_switch2.setText(lv.get('switch2', ''))
            self.legacy_mellanox_switches.setChecked(lv.get('mellanox_switches', False))
            self.legacy_switch_os.setCurrentText(lv.get('switch_os', 'Onyx'))
            self.legacy_skip_nic.setChecked(lv.get('skip_nic', False))
            self.legacy_rdma_pfc.setChecked(lv.get('rdma_pfc', False))
            self.legacy_auto_ports.setCurrentText(lv.get('auto_ports', 'eth'))
            self.legacy_ib_mode.setCurrentText(lv.get('ib_mode', 'datagram'))
            self.legacy_ib_mtu.setText(lv.get('ib_mtu', '4096'))
            self.legacy_eth_mtu.setText(lv.get('eth_mtu', '9000'))
            self.legacy_vxlan.setChecked(lv.get('vxlan', False))
            self.legacy_change_template.setChecked(lv.get('change_template', False))
            self.legacy_template.setText(lv.get('template', ''))
            self.legacy_mgmt_inner_vip.setText(lv.get('mgmt_inner_vip', ''))
            self.legacy_docker_bip.setText(lv.get('docker_bip', ''))
            self.legacy_change_vlan.setChecked(lv.get('change_vlan', False))
            self.legacy_vlan_id.setText(lv.get('vlan_id', ''))
            self.legacy_isolcpu.setText(lv.get('isolcpu', ''))

        # Recalculate and redraw everything (silent=True to skip port assignment count dialogs)
        self.generate_node_ports(silent=True)
        self.generate_uplink_ports(silent=True)
        
        # Update uplink suggestions for both tabs after import
        QTimer.singleShot(100, self._update_uplink_suggestions)

    def _update_start_ports_realtime(self):
        """
        Calculates and displays prospective port assignments in the UI without
        committing them. This provides real-time feedback to the user.
        This function is stateless within its loops to ensure previews are accurate.
        """
        if self.layout_config.get('BALANCED_NODE_ASSIGNMENT'):
            return

        # --- 1. Calculate Node Port Previews ---
        # Start with committed uplink ports as the baseline.
        node_base_assigned = {p for p, lbl in self.port_map if get_port_base_type(lbl) in self.uplink_types}
        # Add any locked node ports.
        for nt_check in self.node_types:
            ent_check = self.node_entries[nt_check]
            if ent_check['lock_cb'].isChecked():
                parsed = _parse_port_string(ent_check['st'].text())
                if parsed: node_base_assigned.update(parsed)

        temp_assigned_for_nodes = node_base_assigned.copy()
        cur_low = 1
        for nt in self.node_types:
            ent = self.node_entries[nt]
            if not ent['lock_cb'].isChecked():
                count = safe_int(ent['cnt'].text())
                split = ent['split_cb'].isChecked()
                factor = safe_int(ent['fac'].currentText(), 1) if split else 1
                reserved = safe_int(ent['rsv'].text())
                phys_needed = (math.ceil(count / factor) if split else count) + reserved
                if phys_needed > 0:
                    start_pos = cur_low
                    while any(p in temp_assigned_for_nodes for p in range(start_pos, start_pos + phys_needed)):
                        start_pos += 1
                    # Do not pre-populate the text box. The placeholder text will guide the user.
                    # ent['st'].setText(str(start_pos))
                    ent['st'].setPlaceholderText(str(start_pos))
                    temp_assigned_for_nodes.update(range(start_pos, start_pos + phys_needed))
                    cur_low = start_pos + phys_needed
                else:
                    ent['st'].clear()

        # --- 2. Calculate Uplink Port Previews ---
        # Start with committed node ports as the baseline.
        uplink_base_assigned = {p for p, lbl in self.port_map if get_port_base_type(lbl) in self.node_types}
        # Add any locked uplink ports.
        for ut_check in self.uplink_types:
            ent_check = self.uplink_entries[ut_check]
            if ent_check['lock_cb'].isChecked():
                is_list = '-' in ent_check['st'].text() or ',' in ent_check['st'].text()
                if is_list:
                    parsed = _parse_port_string(ent_check['st'].text())
                    if parsed: uplink_base_assigned.update(parsed)

        temp_assigned_for_uplinks = uplink_base_assigned.copy()
        for ut in self.uplink_types:  # Assign from high ports down, IPL first
            ent = self.uplink_entries[ut]
            if not ent['lock_cb'].isChecked():
                groups = safe_int(ent['gcnt'].text()) if ut not in ['IPL', 'NB'] else 1
                ppg = safe_int(ent['ppg'].text())
                split = ent['split_cb'].isChecked()
                fac = safe_int(ent['fac'].currentText(), 1) if split else 1
                rsv = safe_int(ent['rsv'].text())

                phys_per_group = math.ceil(ppg / fac) if split and fac > 1 else ppg
                total_span = (phys_per_group + rsv) * groups

                if total_span > 0:
                    # Always search from the absolute top for each uplink type
                    start_pos = self.layout_config['PORT_COUNT']
                    while start_pos >= total_span:
                        port_range = range(start_pos - total_span + 1, start_pos + 1)
                        if not any(p in temp_assigned_for_uplinks for p in port_range):
                            break
                        start_pos -= 1
                    else: # Loop finished without break
                        start_pos = -1 # Indicate no space found

                    if start_pos != -1:
                        # Do not pre-populate the text box. The placeholder text will guide the user.
                        # ent['st'].setText(str(start_pos))
                        ent['st'].setPlaceholderText(str(start_pos))
                        # Add the found ports to the temporary set for the next iteration
                        temp_assigned_for_uplinks.update(range(start_pos - total_span + 1, start_pos + 1))
                    else:
                        ent['st'].setText("N/A")
                else:
                    ent['st'].clear()

    def _generate_cisco9364_node_ports(self, nt, cnt, split, fac, rsv, node_start, existing_ports, start_slice=0):
        """
        Calculates a slice-balanced, round-robin port assignment for Cisco C9364.
        Returns (list_of_tuples, error_string, next_slice_to_use)
        """
        phys_for_nodes = math.ceil(cnt / fac) if split and fac > 1 else cnt
        total_phys = phys_for_nodes + rsv

        if total_phys == 0:
            return ([], None, start_slice)

        num_slices = self.layout_config['PORT_COUNT'] // 8
        base_ports_per_slice = total_phys // num_slices
        extra_ports = total_phys % num_slices
        slice_counts = [base_ports_per_slice] * num_slices
        for i in range(extra_ports):
            slice_to_get_extra = (start_slice + i) % num_slices
            slice_counts[slice_to_get_extra] += 1

        available_by_slice = [[] for _ in range(num_slices)]
        for p in range(1, self.layout_config['PORT_COUNT'] + 1):
            if p not in existing_ports:
                slice_idx = (p - 1) // 8
                if 0 <= slice_idx < num_slices:
                    available_by_slice[slice_idx].append(p)

        for i in range(num_slices):
            if len(available_by_slice[i]) < slice_counts[i]:
                err_msg = (f"Cannot assign ports for {nt}.\n"
                           f"Slice {i+1} (Ports {i*8+1}-{i*8+8}) needs {slice_counts[i]} ports, "
                           f"but only {len(available_by_slice[i])} are available.")
                return (None, err_msg, start_slice)

        ports_to_use = []
        slice_pointers = [0] * num_slices
        last_slice_assigned = -1

        while len(ports_to_use) < total_phys:
            ports_at_start_of_pass = len(ports_to_use)
            for i in range(num_slices):
                slice_idx = (start_slice + i) % num_slices
                if slice_pointers[slice_idx] < slice_counts[slice_idx]:
                    port_to_add = available_by_slice[slice_idx][slice_pointers[slice_idx]]
                    ports_to_use.append(port_to_add)
                    slice_pointers[slice_idx] += 1
                    last_slice_assigned = slice_idx

            if len(ports_to_use) == ports_at_start_of_pass:
                break

        port_labels = []
        for i in range(phys_for_nodes):
            port_num = ports_to_use[i]
            if split and fac > 1:
                first_node = node_start + i * fac
                last_node = min(first_node + fac - 1, node_start + cnt - 1)
                label = f'{nt}-{first_node}' if first_node == last_node else f'{nt}-{first_node}/{last_node}'
            else:
                label = f'{nt}-{node_start + i}'
            port_labels.append((port_num, label))

        for i in range(rsv):
            port_num = ports_to_use[phys_for_nodes + i]
            label = f'RSVD-{nt}'
            port_labels.append((port_num, label))

        next_slice = (last_slice_assigned + 1) % num_slices if last_slice_assigned != -1 else start_slice
        return (port_labels, None, next_slice)

    def _generate_cisco_balanced_uplink_ports(self, ut, groups, ppg, split, fac, rsv, existing_ports, start_slice):
        """
        Calculates a slice-balanced, round-robin port assignment for Cisco uplinks,
        assigning from high ports to low ports.
        Returns (list_of_tuples, error_string, next_slice_to_use)
        """
        if ut == 'NB':
            phys_for_data = math.ceil(ppg / fac) if split and fac > 1 else ppg
            total_phys = phys_for_data + rsv
        else:
            total_phys = (ppg + rsv) * groups

        if total_phys == 0:
            return ([], None, start_slice)

        num_slices = self.layout_config['PORT_COUNT'] // 8
        base_ports_per_slice = total_phys // num_slices
        extra_ports = total_phys % num_slices
        slice_counts = [base_ports_per_slice] * num_slices
        for i in range(extra_ports):
            slice_to_get_extra = (start_slice - i + num_slices) % num_slices
            slice_counts[slice_to_get_extra] += 1

        available_by_slice = [[] for _ in range(num_slices)]
        for p in range(self.layout_config['PORT_COUNT'], 0, -1):
            if p not in existing_ports:
                slice_idx = (p - 1) // 8
                if 0 <= slice_idx < num_slices:
                    available_by_slice[slice_idx].append(p)

        for i in range(num_slices):
            if len(available_by_slice[i]) < slice_counts[i]:
                err_msg = (f"Cannot assign uplink ports for {ut}.\n"
                           f"Slice {i+1} (Ports {i*8+1}-{i*8+8}) needs {slice_counts[i]} ports, "
                           f"but only {len(available_by_slice[i])} are available from the top down.")
                return (None, err_msg, start_slice)

        ports_to_use = []
        slice_pointers = [0] * num_slices
        last_slice_assigned = -1
        while len(ports_to_use) < total_phys:
            ports_at_start_of_pass = len(ports_to_use)
            for i in range(num_slices):
                slice_idx = (start_slice - i + num_slices) % num_slices
                if slice_pointers[slice_idx] < slice_counts[slice_idx]:
                    port_to_add = available_by_slice[slice_idx][slice_pointers[slice_idx]]
                    ports_to_use.append(port_to_add)
                    slice_pointers[slice_idx] += 1
                    last_slice_assigned = slice_idx
                    if len(ports_to_use) == total_phys:
                        break
            if len(ports_to_use) == ports_at_start_of_pass:
                break

        ports_to_use.sort(reverse=True)
        port_iterator = iter(ports_to_use)
        port_labels = []

        try:
            if ut == 'NB':
                # Get CN and EB counts for proper labeling
                cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if hasattr(self, 'node_entries') else 0
                eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if hasattr(self, 'node_entries') else 0
                
                cn_nb_count = 0
                eb_nb_count = 0
                
                for i in range(phys_for_data):
                    port_num = next(port_iterator)
                    if split and fac > 1:
                        first = i * fac + 1
                        last = min(first + fac - 1, ppg)
                        # Determine if this port corresponds to CN or EB
                        if i < cn_count:
                            cn_nb_count += 1
                            label = f'CN-NB-{cn_nb_count}' if first == last else f'CN-NB-{cn_nb_count}/{last}'
                        else:
                            eb_nb_count += 1
                            label = f'EB-NB-{eb_nb_count}' if first == last else f'EB-NB-{eb_nb_count}/{last}'
                    else:
                        # Determine if this port corresponds to CN or EB
                        if i < cn_count:
                            cn_nb_count += 1
                            label = f'CN-NB-{cn_nb_count}'
                        else:
                            eb_nb_count += 1
                            label = f'EB-NB-{eb_nb_count}'
                    port_labels.append((port_num, label))
                for _ in range(rsv):
                    port_num = next(port_iterator)
                    label = f'RSVD-NB'
                    port_labels.append((port_num, label))
            else:
                # *** CRITICAL: DO NOT CHANGE THIS LABEL MAPPING ***
                # Display 'EXT' instead of 'MLAG/BGP' for port labels
                display_ut = 'EXT' if ut == 'MLAG/BGP' else ut
                for group_num in range(groups):
                    for port_index in range(ppg):
                        port_num = next(port_iterator)
                        if display_ut == 'IPL':
                            label = f'IPL-{port_index + 1}'
                        elif groups > 1:
                            label = f'{display_ut}{group_num + 1}-{port_index + 1}'
                        else:
                            label = f'{display_ut}-{port_index + 1}'
                        if split and fac > 1 and (display_ut != 'IPL'):
                            label += f'/{fac}'
                        port_labels.append((port_num, label))

                    for _ in range(rsv):
                        port_num = next(port_iterator)
                        label = 'RSVD-EXT' if display_ut == 'EXT' else f'RSVD-{display_ut}'
                        port_labels.append((port_num, label))
        except StopIteration:
            return (None, f"Internal error during labeling for {ut}: not enough ports collected.", start_slice)

        next_slice = (last_slice_assigned - 1 + num_slices) % num_slices if last_slice_assigned != -1 else start_slice
        return (port_labels, None, next_slice)

    def generate_node_ports(self, silent=False):
        # Validation loop for manual entries
        for nt in self.node_types:
            ent = self.node_entries[nt]
            if ent['lock_cb'].isChecked():
                cnt = safe_int(ent['cnt'].text())
                rsv = safe_int(ent['rsv'].text())
                split = ent['split_cb'].isChecked()
                fac = safe_int(ent['fac'].currentText(), 1) if split else 1
                phys_needed = (math.ceil(cnt / fac) if split else cnt) + rsv
                start_str = ent['st'].text().strip()

                if not start_str and phys_needed > 0:
                    if not silent:
                        QMessageBox.critical(self, 'Input Error', f"Node Type '{nt}': Manual input is selected, but no ports were assigned.")
                    return

                # Only validate count mismatch if it's a full list/range, not a single start port.
                is_start_port_mode = '-' not in start_str and ',' not in start_str and start_str.isdigit()
                if not is_start_port_mode:
                    parsed_ports = _parse_port_string(start_str)
                    if parsed_ports is None or len(parsed_ports) != phys_needed:
                        if not silent:
                            count_str = len(parsed_ports) if parsed_ports else 0
                            QMessageBox.critical(self, 'Count Mismatch', f"For Node Type '{nt}', the number of assigned ports ({count_str}) does not match the required number of physical ports ({phys_needed}).")
                        return

        # Main assignment logic
        self.port_map = [p for p in self.port_map if get_port_base_type(p[1]) not in self.node_types]
        total_nodes = sum(safe_int(self.node_entries[nt]['cnt'].text()) for nt in self.node_types)
        total_reserved = sum(safe_int(self.node_entries[nt]['rsv'].text()) for nt in self.node_types)
        if total_nodes == 0 and total_reserved == 0 and not any(e['lock_cb'].isChecked() for e in self.node_entries.values()):
            if not silent:
                QMessageBox.information(self, 'Node Ports Cleared', 'All node port assignments have been cleared.')
            for nt in self.node_types:
                self.node_entries[nt]['st'].clear()
            self._do_live_preview()
            return

        existing_ports = {p for p, _ in self.port_map}
        starts = {nt: 1 for nt in self.node_types}
        next_balanced_slice = 0

        ports_generated_this_run = 0

        for nt in self.node_types:
            ent = self.node_entries[nt]
            cnt = safe_int(ent['cnt'].text())
            split = ent['split_cb'].isChecked()
            fac = safe_int(ent['fac'].currentText(), 1) if split else 1
            rsv = safe_int(ent['rsv'].text())
            locked = ent['lock_cb'].isChecked()

            if cnt == 0 and rsv == 0:
                continue

            port_labels = []
            if self.layout_config.get('BALANCED_NODE_ASSIGNMENT') and not locked:
                port_labels, err_msg, next_balanced_slice = self._generate_cisco9364_node_ports(
                    nt, cnt, split, fac, rsv, starts[nt], existing_ports, start_slice=next_balanced_slice)
                if err_msg:
                    if not silent:
                        QMessageBox.critical(self, 'Assignment Error', err_msg)
                    return
            elif locked:
                parsed_ports = _parse_port_string(ent['st'].text().strip())
                start_str = ent['st'].text().strip()
                is_start_port_mode = '-' not in start_str and ',' not in start_str and start_str.isdigit()

                if is_start_port_mode:
                    # User entered a single number, treat it as the starting port.
                    start_port = int(start_str)
                    port_labels, _ = self.planner.generate_node_ports(nt, cnt, split, fac, start_port, rsv, starts[nt])
                else:
                    # User entered a full list/range.
                    if not parsed_ports: continue
                    phys_needed_for_nodes = math.ceil(cnt / fac) if split else cnt
                    for i in range(phys_needed_for_nodes):
                        if i >= len(parsed_ports): break
                        port_num = parsed_ports[i]
                        if split:
                            first_node = starts[nt] + i * fac
                            last_node = min(first_node + fac - 1, starts[nt] + cnt - 1)
                            label = f'{nt}-{first_node}' if first_node == last_node else f'{nt}-{first_node}/{last_node}'
                        else:
                            label = f'{nt}-{starts[nt] + i}'
                        port_labels.append((port_num, label))
                    reserved_start_index = phys_needed_for_nodes
                    for i in range(rsv):
                        if reserved_start_index + i >= len(parsed_ports): break
                        port_labels.append((parsed_ports[reserved_start_index + i], f'RSVD-{nt}'))
            else: # Automatic assignment
                phys_needed = (math.ceil(cnt / fac) if split else cnt) + rsv
                spt = 1
                while any(p in existing_ports for p in range(spt, spt + phys_needed)):
                    spt += 1
                port_labels, _ = self.planner.generate_node_ports(nt, cnt, split, fac, spt, rsv, starts[nt])

            self.port_map.extend(port_labels)
            ports_generated_this_run += len(port_labels)
            existing_ports.update(p for p, _ in port_labels)
            starts[nt] += cnt

        # Clear dirty state and update indicators
        self.node_ports_dirty = False
        node_tab_index = self.notebook.indexOf(self.node_tab)
        if node_tab_index != -1:
            self._update_tab_badge(node_tab_index, False, 'Cell Planning')
        
        if not silent:
            # Only show message and navigate when explicitly called (not during auto-assignment)
            self._show_timed_messagebox('Success', f'✓ {ports_generated_this_run} node ports assigned successfully', timeout=1000)
            self.notebook.setCurrentIndex(self.notebook.indexOf(self.output_tab))
        
        self._update_start_ports_realtime()
        self._do_live_preview()

    def generate_uplink_ports(self, silent=False):
        # Validation loop for manual entries
        for ut in self.uplink_types:
            ent = self.uplink_entries[ut]
            if ent['lock_cb'].isChecked():
                groups = safe_int(ent['gcnt'].text()) if ut not in ['IPL', 'NB'] else 1
                ppg = safe_int(ent['ppg'].text())
                rsv = safe_int(ent['rsv'].text())
                split = ent['split_cb'].isChecked()
                fac = safe_int(ent['fac'].currentText(), 1) if split else 1
                phys_per_group = math.ceil(ppg / fac) if split and fac > 1 else ppg
                total_phys_needed = (phys_per_group + rsv) * groups
                start_str = ent['st'].text().strip()

                if not start_str and total_phys_needed > 0:
                    if not silent:
                        QMessageBox.critical(self, 'Input Error', f"Uplink Type '{ut}': Manual input is selected, but no ports were assigned.")
                    return

                is_start_port_mode = '-' not in start_str and ',' not in start_str and start_str.isdigit()
                if not is_start_port_mode:
                    parsed_ports = _parse_port_string(start_str)
                    if parsed_ports is None or len(parsed_ports) != total_phys_needed:
                        if not silent:
                            QMessageBox.critical(self, 'Count Mismatch', f"For Uplink Type '{ut}', the number of assigned ports ({len(parsed_ports)}) does not match the required number of physical ports ({total_phys_needed}).")
                        return

        # Main assignment logic
        bases = {'ISL', 'EXT', 'IPL', 'NB'}
        self.port_map = [p for p in self.port_map if get_port_base_type(p[1]) not in bases]

        # Start with ports assigned to nodes.
        existing_ports = {p for p, _ in self.port_map}
        # Pre-populate existing_ports with any manually locked uplink ports to avoid conflicts.
        for ut_check in self.uplink_types:
            ent_check = self.uplink_entries[ut_check]
            if ent_check['lock_cb'].isChecked():
                start_str = ent_check['st'].text().strip()
                # Only add full lists, not single start-port numbers, as those are calculated.
                is_start_port_mode = '-' not in start_str and ',' not in start_str and start_str.isdigit()
                if not is_start_port_mode:
                    parsed = _parse_port_string(start_str)
                    if parsed:
                        existing_ports.update(parsed)

        ports_generated_this_run = 0
        next_balanced_uplink_slice = self.layout_config['PORT_COUNT'] // 8 - 1

        for ut in self.uplink_types:
            ent = self.uplink_entries[ut]
            ppg = safe_int(ent['ppg'].text())
            split = ent['split_cb'].isChecked()
            fac = safe_int(ent['fac'].currentText(), 1) if split else 1
            rsv = safe_int(ent['rsv'].text())
            locked = ent['lock_cb'].isChecked()
            
            # Get groups value - handle cases where gcnt widget might not exist
            if ut not in ['IPL', 'NB']:
                gcnt_widget = ent.get('gcnt')
                if gcnt_widget and hasattr(gcnt_widget, 'text'):
                    groups = safe_int(gcnt_widget.text())
                else:
                    groups = 1  # Default if gcnt widget doesn't exist
            else:
                groups = 1
                


            # Calculate the total number of physical ports needed for this uplink type
            phys_per_group = math.ceil(ppg / fac) if split else ppg
            total_span = (phys_per_group + rsv) * groups

            port_labels = []
            if locked:
                start_str = ent['st'].text().strip()
                if not start_str: continue
                is_start_port_mode = '-' not in start_str and ',' not in start_str and start_str.isdigit()
                if is_start_port_mode:
                    # User entered a single number, which is the HIGHEST port of the range.
                    spt_high = int(start_str)
                    # Get CN and EB counts for NB port labeling
                    cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                    eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                    port_labels = self.planner.generate_grouped_ports(ut, groups, ppg, split, fac, spt_high, rsv, locked=False, cn_count=cn_count, eb_count=eb_count)
                else:
                    parsed_ports = _parse_port_string(start_str)
                    if not parsed_ports: continue
                    phys_per_group_data = math.ceil(ppg / fac) if split and fac > 1 else ppg
                    port_iterator = iter(parsed_ports)
                    try:
                        if ut == 'NB':
                            # Get CN and EB counts for proper labeling
                            cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if hasattr(self, 'node_entries') else 0
                            eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if hasattr(self, 'node_entries') else 0
                            
                            cn_nb_count = 0
                            eb_nb_count = 0
                            
                            for i in range(phys_per_group_data):
                                port_num = next(port_iterator)
                                if split and fac > 1:
                                    first, last = i * fac + 1, min((i + 1) * fac, ppg)
                                    # Determine if this port corresponds to CN or EB
                                    if i < cn_count:
                                        cn_nb_count += 1
                                        label = f'CN-NB-{cn_nb_count}/{last}' if first != last else f'CN-NB-{cn_nb_count}'
                                    else:
                                        eb_nb_count += 1
                                        label = f'EB-NB-{eb_nb_count}/{last}' if first != last else f'EB-NB-{eb_nb_count}'
                                else:
                                    # Determine if this port corresponds to CN or EB
                                    if i < cn_count:
                                        cn_nb_count += 1
                                        label = f'CN-NB-{cn_nb_count}'
                                    else:
                                        eb_nb_count += 1
                                        label = f'EB-NB-{eb_nb_count}'
                                port_labels.append((port_num, label))
                            for _ in range(rsv):
                                port_labels.append((next(port_iterator), f'RSVD-NB'))
                        else:
                            # *** CRITICAL: DO NOT CHANGE THIS LABEL MAPPING ***
                            # Display 'EXT' instead of 'MLAG/BGP' for port labels
                            display_ut = 'EXT' if ut == 'MLAG/BGP' else ut
                            for group_num in range(groups):
                                for port_index in range(ppg):
                                    port_num = next(port_iterator)
                                    label = f'IPL-{port_index + 1}' if display_ut == 'IPL' else f'{display_ut}{group_num + 1}-{port_index + 1}' if groups > 1 else f'{display_ut}-{port_index + 1}'
                                    if split and fac > 1 and display_ut != 'IPL': label += f'/{fac}'
                                    port_labels.append((port_num, label))
                                for _ in range(rsv):
                                    port_num = next(port_iterator)
                                    label = 'RSVD-EXT' if display_ut == 'EXT' else f'RSVD-{display_ut}'
                                    port_labels.append((port_num, label))
                    except StopIteration:
                        pass
            elif self.layout_config.get('BALANCED_UPLINK_ASSIGNMENT'):
                port_labels, err_msg, next_balanced_uplink_slice = self._generate_cisco_balanced_uplink_ports(
                    ut, groups, ppg, split, fac, rsv, existing_ports, start_slice=next_balanced_uplink_slice)
                if err_msg:
                    if not silent:
                        QMessageBox.critical(self, 'Uplink Assignment Error', err_msg)
                    return
                if port_labels:
                    # DO NOT populate the manual port entry field - this breaks things!
                    # Auto-assigned ports should NOT have entries in the 'st' field
                    # ent['st'].setText(str(min(assigned_port_nums)))
                    pass
            else:
                # Automatic, non-balanced assignment. Search from the top every time.
                if total_span > 0:
                    spt_high = self.layout_config['PORT_COUNT']
                    # Find a block of available ports from the top down
                    while spt_high >= total_span:
                        port_range_to_check = range(spt_high - total_span + 1, spt_high + 1)
                        if not any(p in existing_ports for p in port_range_to_check):
                            break  # Found a free block
                        spt_high -= 1
                    else:  # This else belongs to the while loop
                        if not silent:
                            QMessageBox.critical(self, 'Port Assignment Error', f"Not enough available ports for uplink type '{ut}'.")
                        return

                    # Get CN and EB counts for NB port labeling
                    cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                    eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                    port_labels = self.planner.generate_grouped_ports(ut, groups, ppg, split, fac, spt_high, rsv, locked, cn_count=cn_count, eb_count=eb_count)

            if port_labels:
                self.port_map.extend(port_labels)
                existing_ports.update(p for p, _ in port_labels)
                ports_generated_this_run += len(port_labels)

        # Clear dirty state and update indicators
        self.uplink_ports_dirty = False
        
        if not silent:
            # Only show message and navigate when explicitly called (not during auto-assignment)
            self._show_timed_messagebox('Success', f'✓ {ports_generated_this_run} uplink ports assigned successfully', timeout=1000)
            self.notebook.setCurrentIndex(self.notebook.indexOf(self.output_tab))
        
        self._update_start_ports_realtime()
        self._do_live_preview()

    def _sched_both_node_updates(self):
        self.preview_timer.start(250)
        self.recalc_timer.start(100)

    def _sched_both_uplink_updates(self):
        self.preview_timer.start(250)
        self.recalc_timer.start(100)

    def _sched_multi_rack_preview(self):
        """Schedules a redraw of the multi-rack preview."""
        self.preview_timer.start(250)

    def _draw_multi_rack_preview(self):
        """Draws the preview images for the currently selected rack."""
        if not self.current_rack_name or self.current_rack_name not in self.multi_rack_config:
            self.multi_rack_canvas_a.clear()
            self.multi_rack_canvas_b.clear()
            return

        rack_data = self.multi_rack_config[self.current_rack_name]
        port_map = rack_data.get('port_map', [])
        rack_switch_id = rack_data.get('switch_id', self.switch_id)
        rack_layout_config = SWITCH_LAYOUTS[rack_switch_id]
        
        try:
            rack_base_image = Image.open(resource_path(rack_layout_config['IMAGE'])).convert('RGBA')
        except (FileNotFoundError, KeyError):
            rack_base_image = None

        if not rack_base_image or not port_map:
            self.multi_rack_canvas_a.clear()
            self.multi_rack_canvas_b.clear()
            return
        
        # Remove duplicate port IDs, keeping the last occurrence
        seen_ports = {}
        for port_id, port_name in reversed(port_map):
            if port_id not in seen_ports:
                seen_ports[port_id] = port_name
        port_map_deduplicated = [(port_id, seen_ports[port_id]) for port_id in sorted(seen_ports.keys())]
        
        df = pd.DataFrame(port_map_deduplicated, columns=['Port ID', 'Port Name'])
        
        # For the UI canvases, calculate their specific scale and redraw the overlay
        # with adjusted border thickness so it looks correct when scaled down.
        scale = self.multi_rack_canvas_a.width() / rack_base_image.width if rack_base_image and rack_base_image.width > 0 and self.multi_rack_canvas_a.width() > 0 else 1.0
        img_a = self._draw_overlay(df.assign(**{'Fabric ID': 'A'}), rack_base_image, rack_layout_config, display_scale=scale)
        img_b = self._draw_overlay(df.assign(**{'Fabric ID': 'B'}), rack_base_image, rack_layout_config, display_scale=scale)
        self.multi_rack_canvas_a.setPixmap(pil_to_qpixmap(img_a))
        self.multi_rack_canvas_b.setPixmap(pil_to_qpixmap(img_b))

    def _do_live_preview(self):
        current_tab_index = self.notebook.currentIndex()
        if current_tab_index == self.notebook.indexOf(self.node_tab):
            self._draw_preview(self.node_canvas_a, 'A', include_uplinks=True)
            self._draw_preview(self.node_canvas_b, 'B', include_uplinks=True)
        elif current_tab_index == self.notebook.indexOf(self.output_tab):
            self._update_output_tab_view() # This already handles both single and multi-rack
        elif current_tab_index == self.notebook.indexOf(self.multi_rack_tab):
            self._draw_multi_rack_preview()

    def _calculate_full_preview_port_map(self) -> list[tuple[int, str]]:
        """
        Calculates a complete port map based on the current UI inputs from both
        the Node Types and Uplinks tabs. This is for generating live previews
        and does not commit to self.port_map. It respects locked ports and performs
        a full, combined auto-assignment for unlocked ports.
        
        If the total ports needed exceeds switch capacity, returns the currently
        committed self.port_map instead of calculating a speculative preview.
        """
        # Check if we're in spine mode - if so, only process uplink ports
        is_spine_mode = self.leaf_spine_combo.currentText() == 'spine'
        
        # First check if the current configuration would exceed capacity
        # If it does, return the actual committed port_map instead of a speculative preview
        if not self._validate_total_port_count():
            # Validation failed - return only the committed assignments
            # Filter out node ports if in spine mode
            if is_spine_mode:
                return [(port_id, port_name) for port_id, port_name in (self.port_map.copy() if self.port_map else []) 
                       if get_port_base_type(port_name) not in self.node_types]
            return self.port_map.copy() if self.port_map else []
        
        preview_port_map = []
        assigned_ports = set()
        node_starts = {nt: 1 for nt in self.node_types}

        # --- 1. Handle locked ports first ---
        # Handle locked NODE ports (skip in spine mode)
        if not is_spine_mode:
            for nt, ent in self.node_entries.items():
                if ent['lock_cb'].isChecked():
                    manual_ports_str = ent['st'].text().strip()
                    parsed_ports = _parse_port_string(manual_ports_str)
                    cnt = safe_int(ent['cnt'].text())
                    split = ent['split_cb'].isChecked()
                    fac = safe_int(ent['fac'].currentText(), 1) if split else 1
                    rsv = safe_int(ent['rsv'].text())
                    
                    if parsed_ports:
                        # Check if it's a single start port or a full list
                        is_start_port_mode = '-' not in manual_ports_str and ',' not in manual_ports_str and manual_ports_str.isdigit()
                        
                        if is_start_port_mode:
                            # User entered a single number, treat it as the starting port
                            start_port = int(manual_ports_str)
                            port_labels, _ = self.planner.generate_node_ports(nt, cnt, split, fac, start_port, rsv, node_starts[nt])
                            preview_port_map.extend(port_labels)
                            assigned_ports.update(p for p, _ in port_labels)
                        else:
                            # User entered a full list/range - generate labels for each port
                            phys_needed_for_nodes = math.ceil(cnt / fac) if split else cnt
                            for i in range(phys_needed_for_nodes):
                                if i >= len(parsed_ports): break
                                port_num = parsed_ports[i]
                                if split:
                                    first_node = node_starts[nt] + i * fac
                                    last_node = min(first_node + fac - 1, node_starts[nt] + cnt - 1)
                                    label = f'{nt}-{first_node}' if first_node == last_node else f'{nt}-{first_node}/{last_node}'
                                else:
                                    label = f'{nt}-{node_starts[nt] + i}'
                                preview_port_map.append((port_num, label))
                            
                            # Add reserved ports
                            reserved_start_index = phys_needed_for_nodes
                            for i in range(rsv):
                                if reserved_start_index + i >= len(parsed_ports): break
                                preview_port_map.append((parsed_ports[reserved_start_index + i], f'RSVD-{nt}'))
                            
                            assigned_ports.update(parsed_ports)
                        
                        node_starts[nt] += cnt

        # --- 0. Auto-assign unlocked Uplinks FIRST (from high ports down) ---
        next_balanced_uplink_slice = self.layout_config['PORT_COUNT'] // 8 - 1
        # Use priority order to ensure correct assignment: IPL, ISL, EXT, NB from highest port down
        for ut in ['IPL', 'ISL', 'MLAG/BGP', 'NB']:
            ent = self.uplink_entries[ut]
            if ent['lock_cb'].isChecked(): 
                continue

            # For IPL and NB, groups is always 1 (widget is disabled)
            if ut in ['IPL', 'NB']:
                groups = 1
            else:
                gcnt_widget = ent.get('gcnt')
                if gcnt_widget and hasattr(gcnt_widget, 'text'):
                    groups = safe_int(gcnt_widget.text())
                else:
                    groups = 1  # Default if widget doesn't exist
            
            ppg = safe_int(ent['ppg'].text())
            split = ent['split_cb'].isChecked()
            fac = safe_int(ent['fac'].currentText(), 1) if split else 1
            rsv = safe_int(ent['rsv'].text())

            ports = []
            if self.layout_config.get('BALANCED_UPLINK_ASSIGNMENT'):
                ports, _, next_balanced_uplink_slice = self._generate_cisco_balanced_uplink_ports(
                    ut, groups, ppg, split, fac, rsv, assigned_ports, start_slice=next_balanced_uplink_slice)
            else:
                phys_per_group = math.ceil(ppg / fac) if split and fac > 1 else ppg
                total_span = (phys_per_group + rsv) * groups
                if total_span > 0:
                    spt_high = self.layout_config['PORT_COUNT']
                    # Check if the range [spt_high - total_span + 1, spt_high] conflicts with assigned_ports
                    while spt_high >= total_span:
                        start_port = spt_high - total_span + 1
                        end_port = spt_high + 1
                        # Check if ANY port in our desired range is already assigned
                        if any(p in assigned_ports for p in range(start_port, end_port)):
                            spt_high -= 1
                        else:
                            break
                    if spt_high >= total_span:
                        # Get CN and EB counts for NB port labeling
                        cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                        eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                        ports = self.planner.generate_grouped_ports(ut, groups, ppg, split, fac, spt_high, rsv, locked=False, cn_count=cn_count, eb_count=eb_count)

            if ports:
                preview_port_map.extend(ports)
                assigned_ports.update(p for p, _ in ports)

        # --- 1. Handle locked UPLINK ports SECOND (use priority order to ensure correct assignment) ---
        for ut in ['IPL', 'ISL', 'MLAG/BGP', 'NB']:
            ent = self.uplink_entries[ut]
            if ent['lock_cb'].isChecked():
                manual_ports_str = ent['st'].text().strip()
                parsed_ports = _parse_port_string(manual_ports_str)
                
                # Get groups for locked uplinks
                if ut in ['IPL', 'NB']:
                    groups = 1
                else:
                    gcnt_widget = ent.get('gcnt')
                    if gcnt_widget and hasattr(gcnt_widget, 'text'):
                        groups = safe_int(gcnt_widget.text())
                    else:
                        groups = 1  # Default if widget doesn't exist
                ppg = safe_int(ent['ppg'].text())
                split = ent['split_cb'].isChecked()
                fac = safe_int(ent['fac'].currentText(), 1) if split else 1
                rsv = safe_int(ent['rsv'].text())
                
                
                
                if parsed_ports:
                    # For uplinks, we need to generate the full labels now so they draw correctly.
                    # We can use the planner by treating the first parsed port as the "start".
                    # Get CN and EB counts for NB port labeling
                    cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                    eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                    ports = self.planner.generate_grouped_ports(ut, groups, ppg, split, fac, parsed_ports[0], rsv, locked=True, cn_count=cn_count, eb_count=eb_count)
                    preview_port_map.extend(ports)
                    assigned_ports.update(parsed_ports)
                elif ppg > 0:
                    # Handle locked ports without manual assignment (like auto-locked NB ports)
                    # Use auto-assignment logic for these ports
                    ports = []  # Initialize ports list
                    if self.layout_config.get('BALANCED_UPLINK_ASSIGNMENT'):
                        ports, _, _ = self._generate_cisco_balanced_uplink_ports(
                            ut, groups, ppg, split, fac, rsv, assigned_ports, start_slice=0)
                    else:
                        phys_per_group = math.ceil(ppg / fac) if split and fac > 1 else ppg
                        total_span = (phys_per_group + rsv) * groups
                        if total_span > 0:
                            spt_high = self.layout_config['PORT_COUNT']
                            # Check if the range [spt_high - total_span + 1, spt_high] conflicts with assigned_ports
                            while spt_high >= total_span:
                                start_port = spt_high - total_span + 1
                                end_port = spt_high + 1
                                # Check if ANY port in our desired range is already assigned
                                if any(p in assigned_ports for p in range(start_port, end_port)):
                                    spt_high -= 1
                                else:
                                    break
                            if spt_high >= total_span:
                                # Get CN and EB counts for NB port labeling
                                cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                                eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if ut == 'NB' and hasattr(self, 'node_entries') else 0
                                ports = self.planner.generate_grouped_ports(ut, groups, ppg, split, fac, spt_high, rsv, locked=True, cn_count=cn_count, eb_count=eb_count)
                    
                    if ports:
                        preview_port_map.extend(ports)
                        assigned_ports.update(p for p, _ in ports)

        # --- 3. Auto-assign unlocked Nodes (from low ports up) ---
        # Skip node auto-assignment in spine mode
        if not is_spine_mode:
            next_balanced_node_slice = 0
            for nt in self.node_types:
                ent = self.node_entries[nt]
                if ent['lock_cb'].isChecked(): continue

                count = safe_int(ent['cnt'].text())
                split = ent['split_cb'].isChecked()
                fac = safe_int(ent['fac'].currentText(), 1) if split else 1
                rsv = safe_int(ent['rsv'].text())

                ports = []
                if self.layout_config.get('BALANCED_NODE_ASSIGNMENT'):
                    ports, _, next_balanced_node_slice = self._generate_cisco9364_node_ports(
                        nt, count, split, fac, rsv, node_starts[nt], assigned_ports, start_slice=next_balanced_node_slice)
                else:
                    phys_needed = (math.ceil(count / fac) if split else count) + rsv
                    if phys_needed > 0:
                        spt = 1
                        while any(p in assigned_ports for p in range(spt, spt + phys_needed)):
                            spt += 1
                        ports, _ = self.planner.generate_node_ports(nt, count, split, fac, spt, rsv, node_starts[nt])

                if ports:
                    preview_port_map.extend(ports)
                    assigned_ports.update(p for p, _ in ports)
                node_starts[nt] += count

        return preview_port_map

    def _draw_preview(self, canvas: QLabel, fabric_id: str, *, include_uplinks: bool):
        if not self.base_image:
            canvas.setText('⬅ Click "Assign Switch" on Setup tab to begin')
            return

        if canvas.width() <= 1 or canvas.height() <= 1:
            return

        # Use the new centralized method to get a complete, accurate port map
        rows = self._calculate_full_preview_port_map()

        if not rows:
            if include_uplinks:
                canvas.setText('⬅ Configure and assign uplink ports above')
            else:
                canvas.setText('⬅ Configure and assign node ports above')
            return

        df_raw = pd.DataFrame(rows, columns=['Port ID', 'Port Name'])
        # Use .copy() to create a new DataFrame and avoid SettingWithCopyWarning.
        # This ensures that we are modifying a copy, not a view, of the original data.
        df = df_raw.drop_duplicates(subset=['Port ID'], keep='first').copy()
        df['Fabric ID'] = fabric_id
        df['Hostname'] = self.ha_entry.text().strip() or 'FabricA' if fabric_id == 'A' else self.hb_entry.text().strip() or 'FabricB'

        # Calculate the display scale factor to adjust border thickness for the preview.
        # We only care about width scaling, as the canvases are width-constrained.
        display_scale = 1.0
        if self.base_image and self.base_image.width > 0 and canvas.width() > 0:
            display_scale = canvas.width() / self.base_image.width

        img = self._draw_overlay(df, self.base_image, self.layout_config, display_scale=display_scale)
        canvas.setPixmap(pil_to_qpixmap(img))

    def _draw_overlay(self, df: pd.DataFrame, base: Image.Image, cfg: dict, *, display_scale: float = 1.0) -> Image.Image:
        """
        Draws the port layout overlay on a copy of the base switch image.
        This method now delegates the drawing of each port to the PortDrawer helper class.
        """
        img_with_overlay = base.copy()
        overlay = Image.new('RGBA', img_with_overlay.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Remove duplicate Port IDs before converting to dict
        df_unique = df.drop_duplicates(subset='Port ID', keep='first')
        info = df_unique.set_index('Port ID').to_dict('index')

        # Get CN and EB counts for NB port coloring
        cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if hasattr(self, 'node_entries') else 0
        eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if hasattr(self, 'node_entries') else 0

        drawer = PortDrawer(draw, cfg, display_scale, cn_count, eb_count)

        for pid in range(1, cfg['PORT_COUNT'] + 1):
            if pid not in info:
                x, y = drawer._get_port_coordinates(pid)
                w, h = cfg['PORT_WIDTH'] + 2, cfg['PORT_HEIGHT'] + 2
                draw.rectangle([x, y, x + w, y + h], fill='black', outline='black', width=1)
                continue

            port_info = info[pid]
            label, fabric = port_info['Port Name'], port_info['Fabric ID']
            drawer.draw_port(pid, label, fabric)

        return Image.alpha_composite(img_with_overlay, overlay)

    def generate_overlays_and_export(self, *, export_files: bool=True):
        if not self.base_image:
            if export_files:
                QMessageBox.critical(self, 'Error', 'Ports or image missing')
            else:
                self.canvas_a.setText('⬅ Load switch on Setup tab first')
                self.canvas_b.setText('⬅ Load switch on Setup tab first')
            return

        is_multi_rack = self.multi_rack_checkbox.isChecked()
        has_multi_rack_data = bool(self.multi_rack_config and len(self.multi_rack_config) > 0)
        
        if is_multi_rack and has_multi_rack_data:
            # In multi-rack mode, if we are just viewing (not exporting),
            # we should display the currently selected rack from the dropdown.
            # The _update_output_tab_view function already handles this logic perfectly.
            if not export_files:
                self._update_output_tab_view()
                return

            # If exporting, generate all images.
            if export_files:
                self._generate_multi_rack_outputs(generate_images=True, generate_configs=False)
            elif self.multi_rack_config:
                first_rack_name = list(self.multi_rack_config.keys())[0]
                self._update_output_canvas_for_rack(first_rack_name)
            return # End multi-rack logic here
        
        if not has_multi_rack_data:
            # No racks cloned - use current Cell Planning tab configuration
            # Determine which mode is active (Default or Advanced)
            if hasattr(self, 'cell_planning_mode_advanced_radio') and self.cell_planning_mode_advanced_radio.isChecked():
                # Advanced mode is active
                port_data = self.cell_planning_advanced_port_map if self.cell_planning_advanced_port_map else []
                if not port_data:
                    port_data = self._calculate_cell_planning_advanced_ports() or []
            else:
                # Default mode is active
                port_data = self._calculate_full_preview_port_map() or self.port_map
            
            if not port_data:
                if export_files:
                    QMessageBox.critical(self, 'Error', 'No port data to export.')
                else:
                    self.canvas_a.setText('⬅ Configure Cell Planning tab first')
                    self.canvas_b.setText('⬅ Configure Cell Planning tab first')
                return
            
            # Use the Cell Planning port map for display/export
            df_raw = pd.DataFrame(port_data, columns=['Port ID', 'Port Name'])
            df_agg = df_raw.groupby('Port ID')['Port Name'].apply(lambda s: s.iloc[0]).reset_index()

            dfA = df_agg.copy()
            dfA['Fabric ID'] = 'A'
            dfA['Hostname'] = self.ha_entry.text().strip() or 'FabricA'

            dfB = df_agg.copy()
            dfB['Fabric ID'] = 'B'
            dfB['Hostname'] = self.hb_entry.text().strip() or 'FabricB'

            # For the UI canvases, calculate their specific scale and redraw the overlay
            scale_a = self.canvas_a.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.canvas_a.width() > 0 else 1.0
            imgA_display = self._draw_overlay(dfA, self.base_image, self.layout_config, display_scale=scale_a)
            self.canvas_a.setPixmap(pil_to_qpixmap(imgA_display))

            scale_b = self.canvas_b.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.canvas_b.width() > 0 else 1.0
            imgB_display = self._draw_overlay(dfB, self.base_image, self.layout_config, display_scale=scale_b)
            self.canvas_b.setPixmap(pil_to_qpixmap(imgB_display))

            if export_files:
                # For file export, re-render at full resolution
                imgA_export = self._draw_overlay(dfA, self.base_image, self.layout_config, display_scale=1.0)
                imgB_export = self._draw_overlay(dfB, self.base_image, self.layout_config, display_scale=1.0)

                # Use the new cluster-specific output directory
                os.makedirs(self._cluster_output_dir, exist_ok=True)
                ls_type = self.leaf_spine_combo.currentText()
                cluster_name = self.cluster_name_entry.text().strip() or 'UnnamedCluster'
                hostname_a = dfA['Hostname'].iloc[0]
                hostname_b = dfB['Hostname'].iloc[0]
                
                # Create descriptive filenames with cluster, switch, leaf/spine names
                outA = get_unique_filename(os.path.join(self._cluster_output_dir, f"{cluster_name}_{hostname_a}_{ls_type}_A.png"))
                outB = get_unique_filename(os.path.join(self._cluster_output_dir, f"{cluster_name}_{hostname_b}_{ls_type}_B.png"))
                imgA_export.save(outA)
                imgB_export.save(outB)
                self._show_timed_messagebox('Success', f'PNGs exported to:\n{os.path.relpath(outA)}\n{os.path.relpath(outB)}', timeout=2000)

            self._calculate_and_display_bandwidth()
            return

        # --- Original Single-Rack Logic (when multi-rack checkbox is unchecked) ---
        try:
            # Use live preview data for output tab, committed data for export
            if export_files:
                port_data = self.port_map
            else:
                port_data = self._calculate_full_preview_port_map()
            
            df_raw = pd.DataFrame(port_data, columns=['Port ID', 'Port Name'])
            # The rest of the original logic for single-rack mode
            df_agg = df_raw.groupby('Port ID')['Port Name'].apply(lambda s: s.iloc[0]).reset_index()

            dfA = df_agg.copy()
            dfA['Fabric ID'] = 'A'
            dfA['Hostname'] = self.ha_entry.text().strip() or 'FabricA'

            dfB = df_agg.copy()
            dfB['Fabric ID'] = 'B'
            dfB['Hostname'] = self.hb_entry.text().strip() or 'FabricB'

            # For the UI canvases, calculate their specific scale and redraw the overlay
            # with adjusted border thickness so it looks correct when scaled down.
            scale_a = self.canvas_a.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.canvas_a.width() > 0 else 1.0
            imgA_display = self._draw_overlay(dfA, self.base_image, self.layout_config, display_scale=scale_a)
            self.canvas_a.setPixmap(pil_to_qpixmap(imgA_display))

            scale_b = self.canvas_b.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.canvas_b.width() > 0 else 1.0
            imgB_display = self._draw_overlay(dfB, self.base_image, self.layout_config, display_scale=scale_b)
            self.canvas_b.setPixmap(pil_to_qpixmap(imgB_display))

            if export_files:
                # For file export, we can just save the already-generated display images if we want,
                # or re-render at full resolution. Re-rendering is better for quality.
                imgA_export = self._draw_overlay(dfA, self.base_image, self.layout_config, display_scale=1.0)
                imgB_export = self._draw_overlay(dfB, self.base_image, self.layout_config, display_scale=1.0)

                # Use the new cluster-specific output directory
                os.makedirs(self._cluster_output_dir, exist_ok=True)
                ls_type = self.leaf_spine_combo.currentText()
                cluster_name = self.cluster_name_entry.text().strip() or 'UnnamedCluster'
                hostname_a = dfA['Hostname'].iloc[0]
                hostname_b = dfB['Hostname'].iloc[0]
                
                # Create descriptive filenames with cluster, switch, leaf/spine names
                outA = get_unique_filename(os.path.join(self._cluster_output_dir, f"{cluster_name}_{hostname_a}_{ls_type}_A.png"))
                outB = get_unique_filename(os.path.join(self._cluster_output_dir, f"{cluster_name}_{hostname_b}_{ls_type}_B.png"))
                imgA_export.save(outA)
                imgB_export.save(outB)
                self._show_timed_messagebox('Success', f'PNGs exported to:\n{os.path.relpath(outA)}\n{os.path.relpath(outB)}', timeout=2000)

            self._calculate_and_display_bandwidth()

        except Exception as e:
            if export_files: QMessageBox.critical(self, 'Error', f'Failed to generate overlays: {e}')

    def _construct_switch_conf_command_parts(self, env_vars: dict, use_shell_vars: bool = False, script_filename: str = 'switch_conf.py') -> list[str]:
        """Helper to build the command list for switch_conf.py."""
        # This is a new helper function extracted from the original _generate_switch_config
        # No changes to the logic, just relocation.
        return self._build_command_parts(env_vars, use_shell_vars, script_filename)

    def _build_command_parts(self, env_vars: dict, use_shell_vars: bool = False, script_filename: str = 'switch_conf.py') -> list[str]:
        """Helper to build the command list for switch_conf.py."""
        def get_val(key):
            """Gets the command-line representation of a value (literal or shell variable)."""
            if use_shell_vars:
                if key == 'autonomous_systems':
                    return '$ASNS'
                return f'${key.upper()}'
            return env_vars.get(key, '')

        cmd_parts = ['python3', script_filename]
        # Always check the actual value from env_vars before adding an argument.
        if env_vars.get('swtype'):
            cmd_parts.append(get_val('swtype'))

        param_map = {'clustername': '--cluster-name', 'hostnames': '--hostname', 'mgmt_ips': '--mgmt-ips', 'mcidr': '--mgmt-subnet', 'mgw': '--mgmt-gateway', 'ntp1': '--ntp', 'lors': '--switch-type', 'external_vlans': '--external-vlans', 'autonomous_systems': '--autonomous-systems', 'extports': '--external-ports', 'iplports': '--ipl-ports', 'islports': '--isl-ports'}
        for key, switch in param_map.items():
            if env_vars.get(key):
                cmd_parts.extend([switch, get_val(key)])

        # Add --vxlan flag if requested
        if env_vars.get('vxlan'):
            cmd_parts.append('--vxlan')

        # Conditionally add --external-speed only for non-Cisco switches
        if env_vars.get('swtype') != 'cisco' and env_vars.get('uplinkspeed'):
            cmd_parts.extend(['--external-speed', get_val('uplinkspeed')])

        # Conditionally add --data-vlan only if it's not the default value.
        if (data_vlan_val := env_vars.get('datavlan')) and data_vlan_val != '69':
            cmd_parts.extend(['--data-vlan', get_val('datavlan')])

        node_port_keys = ['cports', 'dports', 'eports', 'ieports', 'gports', 'nic2_nbports']
        # Filter keys based on whether they have a non-empty value in env_vars.
        active_node_port_keys = [k for k in node_port_keys if env_vars.get(k)]
        if active_node_port_keys:
            if use_shell_vars:
                # Get the shell variable names for the active keys.
                shell_vars = [f'${k.upper()}' for k in active_node_port_keys]
                cmd_parts.extend(['--node-ports', ','.join(shell_vars)])
            else:
                # Get the actual values for the active keys.
                node_port_values = [env_vars[k] for k in active_node_port_keys]
                cmd_parts.extend(['--node-ports', ','.join(node_port_values)])

        return [part for part in cmd_parts if part] if not use_shell_vars else cmd_parts
    
    def _get_switch_config_env_vars(self) -> dict[str, str]:
        """Collects UI data and assembles the environment variables for switch_conf.py."""
        ha = self.ha_entry.text().strip() or 'FabricA'
        hb = self.hb_entry.text().strip() or 'FabricB'
        hostnames = f'{ha},{hb}' if ha and hb else ha or hb
        mgmt_ips = f"{self.switch_a_mgmt_ip_entry.text().strip()},{self.switch_b_mgmt_ip_entry.text().strip()}" if self.switch_a_mgmt_ip_entry.text().strip() and self.switch_b_mgmt_ip_entry.text().strip() else self.switch_a_mgmt_ip_entry.text().strip() or self.switch_b_mgmt_ip_entry.text().strip()

        cluster_name = self.cluster_name_entry.text().strip() or 'VastData-0001'        
        vendor_map = {'Cisco-NXOS': 'cisco', 'MNLX-Onyx': 'mellanox', 'MNLX-Cumulus': 'cumulus', 'Arista-EOS': 'arista'}
        swtype = vendor_map.get(self.vendor_combo.currentText(), '')

        uplink_speed = self.uplink_speed_combo.currentText() or self.layout_config.get('NATIVE_SPEED', '')
        
        # For single-rack mode, use a default rack name
        rack_name = 'Rack1'

        # Get port split settings from UI widgets
        port_splits = {
            nt: (safe_int(ent['fac'].currentText(), 1) if ent['split_cb'].isChecked() else 1)
            for nt, ent in self.node_entries.items()
        }
        uplink_splits = {
            ut: (safe_int(ent['fac'].currentText(), 1) if ent.get('split_cb') and ent['split_cb'].isChecked() else 1)
            for ut, ent in self.uplink_entries.items()
        }

        # Group ports by type and group
        port_plan = {}
        current_group_key = None
        for port, label in self.port_map:
            base_type = get_port_base_type(label)
            key = None
            if base_type in ['IPL', 'NB'] or base_type in self.node_types:
                key = base_type
                current_group_key = None
            elif base_type in ['ISL', 'MLAG/BGP', 'EXT']:
                # EXT is the display name for MLAG/BGP, map it back
                internal_type = 'MLAG/BGP' if base_type == 'EXT' else base_type
                match = re.match(rf'{base_type}(\d+)', label)
                if match:
                    group_num = int(match.group(1))
                    key = f'{internal_type}-GROUP-{group_num}'
                    current_group_key = key
                elif label.startswith('RSVD-') and current_group_key and (current_group_key.startswith(base_type) or (base_type == 'EXT' and current_group_key.startswith('MLAG/BGP'))):
                    key = current_group_key
                elif not label.startswith('RSVD-'):
                    # No group number in label (e.g., "EXT-1" or "ISL-1") - default to group 1
                    key = f'{internal_type}-GROUP-1'
                    current_group_key = key

            if key:
                port_plan.setdefault(key, []).append(port)
            else:
                current_group_key = None

        # Format port ranges
        isl_ranges = [_format_port_ranges(ports, uplink_splits.get('ISL', 1)) for key, ports in port_plan.items() if key.startswith('ISL-GROUP')]
        ext_ranges = [_format_port_ranges(ports, uplink_splits.get('MLAG/BGP', 1)) for key, ports in port_plan.items() if key.startswith('MLAG/BGP-GROUP')]

        customer_vlans_raw = self.customer_vlans_entry.text().strip()
        cleaned_vlans = re.sub(r',+', ',', customer_vlans_raw.replace(' ', ',')).strip(',')
        
        bgp_asn_raw = self.bgp_asn_entry.text().strip()
        cleaned_asns = re.sub(r',+', ',', bgp_asn_raw.replace(' ', ',')).strip(',')
        
        # VXLAN is only enabled if BGP ASNs are defined and the overlay option is selected
        has_bgp_asns = bool(cleaned_asns)
        should_use_vxlan = self.use_vxlan_overlay and has_bgp_asns
        vxlan_value = 'True' if should_use_vxlan else ''

        env_vars = {
            'mgmt_ips': mgmt_ips, 'mcidr': self.net_cidr_combo.currentText(), 'mgw': self.net_def_route_entry.text().strip(),
            'clustername': cluster_name, 'uplinkspeed': uplink_speed, 'rack_name': rack_name,
            'ntp1': self.ntp_server_entry.text().strip() or '0.0.0.123', 'hostnames': hostnames, 'swtype': swtype,
            'lors': self.leaf_spine_combo.currentText(), 'vxlan': vxlan_value,
            'external_vlans': cleaned_vlans, 'autonomous_systems': cleaned_asns, 'datavlan': self.data_vlan_entry.text().strip() or '69',
            'cports': _format_port_ranges(port_plan.get('CN', []), port_splits.get('CN', 1)),
            'dports': _format_port_ranges(port_plan.get('DN', []), port_splits.get('DN', 1)),
            'eports': _format_port_ranges(port_plan.get('EB', []), port_splits.get('EB', 1)),
            'ieports': _format_port_ranges(port_plan.get('IE', []), port_splits.get('IE', 1)),
            'gports': _format_port_ranges(port_plan.get('GN', []), port_splits.get('GN', 1)),
            'extports': ','.join(sorted(ext_ranges)),
            'iplports': _format_port_ranges(port_plan.get('IPL', []), uplink_splits.get('IPL', 1)),
            'islports': ','.join(sorted(isl_ranges)),
            'nic2_nbports': _format_port_ranges(port_plan.get('NB', []), uplink_splits.get('NB', 1)),
        }

        if self.use_2nd_nic_checkbox.isChecked():
            env_vars['2ND_NIC'] = 'Yes'
        if self.pfc_checkbox.isChecked():
            env_vars['pfc'] = 'True'

        # Filter out any keys with empty values before returning
        return {k: v for k, v in env_vars.items() if v}

    def _validate_required_fields_for_config(self) -> tuple[bool, list[str]]:
        """
        Validates that all required fields for switch config generation are filled.
        Returns (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        
        # Check Switch A Hostname
        if not self.ha_entry.text().strip():
            missing_fields.append("Switch A Hostname")
        
        # Check Switch B Hostname
        if not self.hb_entry.text().strip():
            missing_fields.append("Switch B Hostname")
        
        # Check Mgmt Default Route
        if not self.net_def_route_entry.text().strip():
            missing_fields.append("Mgmt Default Route")
        
        # Check Network CIDR (always has a value from combo, but verify)
        if not self.net_cidr_combo.currentText().strip():
            missing_fields.append("Network CIDR")
        
        # Check FabricA Mgmt IP
        if not self.switch_a_mgmt_ip_entry.text().strip():
            missing_fields.append("FabricA Mgmt IP")
        
        # Check FabricB Mgmt IP
        if not self.switch_b_mgmt_ip_entry.text().strip():
            missing_fields.append("FabricB Mgmt IP")
        
        # Check NTP Server IP
        if not self.ntp_server_entry.text().strip():
            missing_fields.append("NTP Server IP")
        
        # Check Cluster Name
        if not self.cluster_name_entry.text().strip():
            missing_fields.append("Cluster Name")
        
        # Check Leaf or Spine (always has a value from combo, but verify)
        if not self.leaf_spine_combo.currentText().strip():
            missing_fields.append("Leafs Or Spines")

        # Ensure VXLAN overlay requirements are satisfied
        if self.use_vxlan_overlay and not self._has_bgp_asns():
            missing_fields.append("BGP ASNs (required for VXLAN overlay)")
        
        return (len(missing_fields) == 0, missing_fields)
    
    def _generate_switch_config(self):
        # Validate required fields before proceeding
        is_valid, missing_fields = self._validate_required_fields_for_config()
        if not is_valid:
            missing_list = "\n".join([f"  • {field}" for field in missing_fields])
            QMessageBox.critical(
                self,
                "⚠️ Required Fields Missing",
                f"Please fill in the following required fields before creating switch configs:\n\n{missing_list}\n\n"
                "These fields are critical for switch configuration generation."
            )
            return
        
        self.create_config_button.setEnabled(False)
        self._ensure_status_dialog("Generating Switch Configs")
        self._status_append("Starting switch configuration generation...")

        if self.multi_rack_checkbox.isChecked() and self.multi_rack_config:
            self._generate_multi_rack_outputs(generate_images=False, generate_configs=True)
        else:
            # --- Original Single-Rack Logic ---
            script_filename = os.path.basename(get_unique_filename(os.path.join(self._switch_config_dir, 'switch_conf.py')))
            env_vars = self._get_switch_config_env_vars()
            # Use the new cluster-specific switch config directory
            params = {
                'config_dir': self._switch_config_dir,
                'env_vars': env_vars,
                'cmd_parts_for_file': self._build_command_parts(env_vars, use_shell_vars=True, script_filename=script_filename),
                'cmd_parts_exec': self._build_command_parts(env_vars, use_shell_vars=False, script_filename=script_filename),
                'script_filename': script_filename
            }
            self._run_config_worker(params)

    def _generate_multi_rack_outputs(self, generate_images: bool, generate_configs: bool):
        """
        Iterates through all racks in multi_rack_config and generates the requested outputs.
        For config generation, downloads switch_conf.py once and processes all racks in parallel.
        """
        total_racks = len(self.multi_rack_config)
        all_results = []

        # Initialize status dialog title
        status_title = (
            "Generating Overlays and Switch Configs" if (generate_images and generate_configs)
            else "Generating Overlays" if generate_images
            else "Generating Switch Configs"
        )
        self._ensure_status_dialog(status_title)

        # For config generation, download switch_conf.py once before processing racks
        if generate_configs:
            self._status_append("Downloading switch_conf.py ...")
            os.makedirs(self._switch_config_dir, exist_ok=True)
            script_filename = os.path.basename(get_unique_filename(os.path.join(self._switch_config_dir, 'switch_conf.py')))
            # Download once using a dummy worker
            dummy_params = {'config_dir': self._switch_config_dir, 'env_vars': {}, 
                           'cmd_parts_for_file': [], 'cmd_parts_exec': [], 'script_filename': script_filename}
            dummy_worker = SwitchConfigWorker(dummy_params, skip_download=False)
            dummy_worker.run_sync()  # This will download the script once
            script_filename = dummy_worker.params.get('script_filename', script_filename)
        else:
            script_filename = 'switch_conf.py'

        # Store all tasks for parallel processing
        image_tasks = []

        for i, (rack_name, rack_data) in enumerate(self.multi_rack_config.items(), 1):
            if generate_configs:
                self._status_append(f"Preparing configs... ({i}/{total_racks})")

            port_map, _ = self._calculate_rack_port_map(rack_data)
            if not port_map:
                all_results.append(f"Skipped {rack_name}: No ports assigned.")
                continue

            if generate_images:
                # Store task for parallel processing
                image_tasks.append((rack_name, rack_data, port_map))
            
            if generate_configs:
                env_vars = self._get_rack_config_env_vars(rack_data, port_map, rack_name)
                # Use the new cluster-specific switch config directory
                params = {
                    'config_dir': self._switch_config_dir,
                    'env_vars': env_vars,
                    'cmd_parts_for_file': self._build_command_parts(env_vars, use_shell_vars=True, script_filename=script_filename),
                    'cmd_parts_exec': self._build_command_parts(env_vars, use_shell_vars=False, script_filename=script_filename),
                    'script_filename': script_filename
                }
                # Store params for parallel processing later
                all_results.append(('config_params', params, rack_name))

        # Process images in parallel if requested
        if generate_images and image_tasks:
            
            def process_rack_images(task):
                """Process a single rack's images."""
                rack_name, rack_data, port_map = task
                try:
                    df_raw = pd.DataFrame(port_map, columns=['Port ID', 'Port Name'])
                    df_agg = df_raw.groupby('Port ID')['Port Name'].apply(lambda s: s.iloc[0]).reset_index()
                    rack_switch_id = rack_data.get('switch_id', self.switch_id)
                    rack_layout_config = SWITCH_LAYOUTS[rack_switch_id]
                    try:
                        rack_base_image = Image.open(resource_path(rack_layout_config['IMAGE'])).convert('RGBA')
                    except (FileNotFoundError, KeyError):
                        return f"Skipped images for {rack_name}: Base image not found."

                    dfA = df_agg.copy(); dfA['Fabric ID'] = 'A'; dfA['Hostname'] = rack_data.get('hostname_a', f'{rack_name}-A')
                    dfB = df_agg.copy(); dfB['Fabric ID'] = 'B'; dfB['Hostname'] = rack_data.get('hostname_b', f'{rack_name}-B')

                    imgA = self._draw_overlay(dfA, rack_base_image, rack_layout_config, display_scale=1.0)
                    imgB = self._draw_overlay(dfB, rack_base_image, rack_layout_config, display_scale=1.0)

                    # Use the new cluster-specific output directory
                    os.makedirs(self._cluster_output_dir, exist_ok=True)
                    ls_type = rack_data.get('lors', 'leaf')
                    cluster_name = self.cluster_name_entry.text().strip() or 'UnnamedCluster'
                    hostname_a = dfA['Hostname'].iloc[0]
                    hostname_b = dfB['Hostname'].iloc[0]
                    
                    outA = get_unique_filename(os.path.join(self._cluster_output_dir, f"{cluster_name}_{rack_name}_{hostname_a}_{ls_type}_A.png"))
                    outB = get_unique_filename(os.path.join(self._cluster_output_dir, f"{cluster_name}_{rack_name}_{hostname_b}_{ls_type}_B.png"))
                    imgA.save(outA)
                    imgB.save(outB)
                    return f"Generated images for {rack_name}: {os.path.relpath(outA)}, {os.path.relpath(outB)}"
                except Exception as e:
                    return f"Failed to generate images for {rack_name}: {e}"
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                completed = 0
                for future in concurrent.futures.as_completed(executor.submit(process_rack_images, task) for task in image_tasks):
                    completed += 1
                    self._status_append(f"Images: {completed}/{len(image_tasks)} completed")
                    result = future.result()
                    all_results.append(result)

        # If generating configs, process all racks in parallel now
        if generate_configs:
            # Separate config tasks from other results
            config_tasks = [r for r in all_results if isinstance(r, tuple) and r[0] == 'config_params']
            other_results = [r for r in all_results if not (isinstance(r, tuple) and r[0] == 'config_params')]
            all_results = other_results
            
            if config_tasks:
                self._status_append("Generating switch configs in parallel ...")
                
                def process_rack_config(config_item):
                    """Process a single rack config."""
                    _, params, rack_name = config_item
                    # Skip download for all racks (already downloaded)
                    worker = SwitchConfigWorker(params, skip_download=True)
                    return worker.run_sync()
                
                # Process all racks in parallel using ThreadPoolExecutor
                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                    future_to_rack = {executor.submit(process_rack_config, task): task[2] for task in config_tasks}
                    
                    completed = 0
                    for future in concurrent.futures.as_completed(future_to_rack):
                        completed += 1
                        self._status_append(f"Configs: {completed}/{len(config_tasks)} completed")
                        result = future.result()
                        all_results.append(result)

        # Display summary within the unified status dialog
        summary_title = "Image Generation Complete" if generate_images and not generate_configs else "Switch Config Generation Complete" if generate_configs and not generate_images else "Overlay and Config Generation Complete"
        self._ensure_status_dialog(summary_title)
        
        if all_results:
            for result in all_results:
                self._status_append(result)
        else:
            self._status_append("No results to display.")

        if generate_configs:
            self.create_config_button.setEnabled(True)
        self._status_append("Done.")

    def _run_config_worker(self, params: dict):
        """
        Helper function to create and run the SwitchConfigWorker in a thread.
        This encapsulates the original single-rack worker logic.
        """
        self.thread = QThread()
        self.worker = SwitchConfigWorker(params)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_switch_config_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_switch_config_finished(self, result_message):
        # Route results to the unified status dialog instead of spawning a separate message box
        self._ensure_status_dialog('Switch Config Results')
        self._status_append(result_message)
        self.create_config_button.setEnabled(True)

    def _get_rack_config_env_vars(self, rack_data: dict, port_map: list, rack_name: str) -> dict:
        """Gathers data for a specific rack and assembles environment variables."""
        ha = rack_data.get('hostname_a', 'FabricA')
        hb = rack_data.get('hostname_b', 'FabricB')
        hostnames = f'{ha},{hb}' if ha and hb else ha or hb
        mgmt_ips = f"{rack_data.get('mgmt_ip_a', '')},{rack_data.get('mgmt_ip_b', '')}"
        
        # Inherit global settings from the main Setup tab
        # Use the rack's specific switch model for config generation
        rack_switch_id = rack_data.get('switch_id', self.switch_id)
        rack_layout_config = SWITCH_LAYOUTS[rack_switch_id]
        cluster_name = self.cluster_name_entry.text().strip() or 'VastData-0001'        
        vendor_map = {'Cisco-NXOS': 'cisco', 'MNLX-Onyx': 'mellanox', 'MNLX-Cumulus': 'cumulus', 'Arista-EOS': 'arista'}
        swtype = vendor_map.get(self.vendor_combo.currentText(), '')
        uplink_speed = self.uplink_speed_combo.currentText() or rack_layout_config.get('NATIVE_SPEED', '')

        # Get port split settings from the rack's data
        port_splits = {
            nt: (d.get('factor', 1) if d.get('split') else 1)
            for nt, d in rack_data.get('nodes', {}).items()
        }
        uplink_splits = {
            ut: (d.get('factor', 1) if d.get('split') else 1)
            for ut, d in rack_data.get('uplinks', {}).items()
        }

        # Group ports by type and group from the calculated port_map
        port_plan = {}
        for port, label in port_map:
            base_type = get_port_base_type(label)
            key = base_type
            if base_type in ['ISL', 'MLAG/BGP', 'EXT']:
                # EXT is the display name for MLAG/BGP, map it back
                internal_type = 'MLAG/BGP' if base_type == 'EXT' else base_type
                match = re.match(rf'{base_type}(\d+)', label)
                if match:
                    group_num = int(match.group(1))
                    key = f'{internal_type}-GROUP-{group_num}'
                elif not label.startswith('RSVD-'):
                    # No group number in label (e.g., "EXT-1" or "ISL-1") - default to group 1
                    key = f'{internal_type}-GROUP-1'
            port_plan.setdefault(key, []).append(port)

        # Format port ranges
        isl_ranges = [_format_port_ranges(ports, uplink_splits.get('ISL', 1)) for key, ports in sorted(port_plan.items()) if key.startswith('ISL-GROUP')]
        ext_ranges = [_format_port_ranges(ports, uplink_splits.get('MLAG/BGP', 1)) for key, ports in sorted(port_plan.items()) if key.startswith('MLAG/BGP-GROUP')]

        customer_vlans_raw = self.customer_vlans_entry.text().strip()
        cleaned_vlans = re.sub(r',+', ',', customer_vlans_raw.replace(' ', ',')).strip(',')
        
        bgp_asn_raw = self.bgp_asn_entry.text().strip()
        cleaned_asns = re.sub(r',+', ',', bgp_asn_raw.replace(' ', ',')).strip(',')
        
        # VXLAN is only enabled if BGP ASNs are defined and the overlay option is selected for this rack
        has_bgp_asns = bool(cleaned_asns)
        rack_use_vxlan = rack_data.get('use_vxlan_overlay', self.use_vxlan_overlay)
        should_use_vxlan = rack_use_vxlan and has_bgp_asns
        vxlan_value = 'True' if should_use_vxlan else ''

        env_vars = {
            'mgmt_ips': mgmt_ips, 'mcidr': self.net_cidr_combo.currentText(), 'mgw': self.net_def_route_entry.text().strip(),
            'clustername': cluster_name, 'uplinkspeed': uplink_speed, 'rack_name': rack_name,
            'ntp1': self.ntp_server_entry.text().strip() or '0.0.0.123', 'hostnames': hostnames, 'swtype': swtype,
            'lors': rack_data.get('lors', 'leaf'), 'vxlan': vxlan_value,
            'external_vlans': cleaned_vlans, 'datavlan': self.data_vlan_entry.text().strip() or '69',
            'autonomous_systems': cleaned_asns,
            'cports': _format_port_ranges(port_plan.get('CN', []), port_splits.get('CN', 1)),
            'dports': _format_port_ranges(port_plan.get('DN', []), port_splits.get('DN', 1)),
            'eports': _format_port_ranges(port_plan.get('EB', []), port_splits.get('EB', 1)),
            'ieports': _format_port_ranges(port_plan.get('IE', []), port_splits.get('IE', 1)),
            'gports': _format_port_ranges(port_plan.get('GN', []), port_splits.get('GN', 1)),
            'extports': ','.join(sorted(ext_ranges)),
            'iplports': _format_port_ranges(port_plan.get('IPL', []), uplink_splits.get('IPL', 1)),
            'islports': ','.join(sorted(isl_ranges)),
            'nic2_nbports': _format_port_ranges(port_plan.get('NB', []), uplink_splits.get('NB', 1)),
        }

        # Removed debug print of multi-rack env_vars extports

        if self.use_2nd_nic_checkbox.isChecked():
            env_vars['2ND_NIC'] = 'Yes'
        if self.pfc_checkbox.isChecked():
            env_vars['pfc'] = 'True'

        filtered = {k: v for k, v in env_vars.items() if v}
        return filtered

    def _calculate_advanced_rack_port_map(self, rack_data: dict) -> tuple[list, set]:
        """Calculates port map for advanced mode racks using stored advanced config."""
        port_map = []
        assigned = set()
        
        rack_switch_id = rack_data.get('switch_id', self.switch_id)
        rack_layout_config = SWITCH_LAYOUTS[rack_switch_id]
        port_count = rack_layout_config.get('PORT_COUNT', 64)
        left_ports, right_ports = self._get_left_right_ports_mellanox(port_count)
        
        advanced_config = rack_data.get('advanced_config', {})
        node_routing = advanced_config.get('node_routing', {})
        nodes_data = rack_data.get('nodes', {})
        uplinks_data = rack_data.get('uplinks', {})
        dbox_type = advanced_config.get('dbox_type', 'CeresV2')  # Default to CeresV2 for backward compatibility
        
        # Track current indices for left and right sides
        left_current_index = 0
        right_current_index = 0
        
        # DN assignment: Based on DBox type
        if 'DN' in nodes_data:
            dn_info = nodes_data['DN']
            dn_count = dn_info.get('count', 0)
            if dn_count > 0:
                dn_split = dn_info.get('split', False)
                dn_factor = dn_info.get('factor', 2)
                
                # Get DNode groups based on DBox type
                left_dns, right_dns = self._get_dnode_groups_by_dbox_type(dn_count, dbox_type)
                
                # Assign DNs to LEFT side
                if dn_split and dn_factor > 1:
                    # Port splitting: take first N DNs from left_dns list for each port
                    left_idx = 0
                    while left_idx < len(left_dns) and left_current_index < len(left_ports):
                        # Take next dn_factor DNs from the left_dns list
                        dns_for_port = left_dns[left_idx:left_idx + dn_factor]
                        if len(dns_for_port) == 1:
                            label = f'DN-{dns_for_port[0]}'
                        else:
                            label = f'DN-{dns_for_port[0]}/{dns_for_port[-1]}'
                        
                        port = left_ports[left_current_index]
                        port_map.append((port, label))
                        assigned.add(port)
                        left_current_index += 1
                        left_idx += len(dns_for_port)
                else:
                    # No splitting: one DN per port
                    for dn_num in left_dns:
                        if left_current_index < len(left_ports):
                            port = left_ports[left_current_index]
                            port_map.append((port, f'DN-{dn_num}'))
                            assigned.add(port)
                            left_current_index += 1
                
                # Assign DNs to RIGHT side
                if dn_split and dn_factor > 1:
                    # Port splitting: take first N DNs from right_dns list for each port
                    right_idx = 0
                    while right_idx < len(right_dns) and right_current_index < len(right_ports):
                        # Take next dn_factor DNs from the right_dns list
                        dns_for_port = right_dns[right_idx:right_idx + dn_factor]
                        if len(dns_for_port) == 1:
                            label = f'DN-{dns_for_port[0]}'
                        else:
                            label = f'DN-{dns_for_port[0]}/{dns_for_port[-1]}'
                        
                        port = right_ports[right_current_index]
                        port_map.append((port, label))
                        assigned.add(port)
                        right_current_index += 1
                        right_idx += len(dns_for_port)
                else:
                    # No splitting: one DN per port
                    for dn_num in right_dns:
                        if right_current_index < len(right_ports):
                            port = right_ports[right_current_index]
                            port_map.append((port, f'DN-{dn_num}'))
                            assigned.add(port)
                            right_current_index += 1
        
        # Assign other node types based on routing preferences
        for nt in ['CN', 'EB', 'IE', 'GN']:
            if nt not in nodes_data:
                continue
            
            node_info = nodes_data[nt]
            count = node_info.get('count', 0)
            if count == 0:
                continue
            
            # Get routing preference from advanced_config
            routing_pref = node_routing.get(nt, 'RIGHT')
            
            # Get split settings
            split = node_info.get('split', False)
            factor = node_info.get('factor', 2)
            
            # Choose port list based on routing preference
            if routing_pref == 'LEFT':
                current_index = left_current_index
                port_list = left_ports
            else:
                current_index = right_current_index
                port_list = right_ports
            
            # Assign ports
            for i in range(count):
                if split:
                    if i % factor == 0:
                        end_idx = min(i + factor - 1, count - 1)
                        label = f'{nt}-{i+1}/{end_idx+1}'
                    else:
                        continue
                else:
                    label = f'{nt}-{i+1}'
                
                if current_index < len(port_list):
                    port = port_list[current_index]
                    port_map.append((port, label))
                    assigned.add(port)
                    current_index += 1
            
            # Update the appropriate index
            if routing_pref == 'LEFT':
                left_current_index = current_index
            else:
                right_current_index = current_index
        
        # Assign uplinks (from right side, remaining ports)
        uplink_labels = []
        for ut in ['IPL', 'ISL', 'MLAG/BGP']:
            # Map MLAG/BGP to EXT for lookup in advanced config
            lookup_key = 'EXT' if ut == 'MLAG/BGP' else ut
            if lookup_key not in uplinks_data:
                continue
            
            uplink_info = uplinks_data[lookup_key]
            groups = uplink_info.get('groups', 0)
            ppg = uplink_info.get('ports_per_group', 0)
            
            if groups == 0 or ppg == 0:
                continue
            
            # IPL is always 1 group
            if ut == 'IPL':
                groups = 1
            
            for group_num in range(1, groups + 1):
                for port_num in range(1, ppg + 1):
                    # Find next available port from right side
                    while right_current_index < len(right_ports) and right_ports[right_current_index] in assigned:
                        right_current_index += 1
                    
                    if right_current_index < len(right_ports):
                        port = right_ports[right_current_index]
                        label = f'{ut}{group_num}-{port_num}'
                        uplink_labels.append((port, label))
                        assigned.add(port)
                        right_current_index += 1
        
        port_map.extend(uplink_labels)
        
        return sorted(port_map, key=lambda x: x[0]), assigned

    def _calculate_rack_port_map(self, rack_data: dict) -> tuple[list, set]:
        """Calculates the full port map for a single rack's configuration data."""
        # Check if this rack uses advanced mapping mode
        mapping_mode = rack_data.get('mapping_mode', 'default')
        if mapping_mode == 'advanced':
            return self._calculate_advanced_rack_port_map(rack_data)
        
        # Default mode: continue with existing logic
        port_map = []
        assigned_ports = set()
        
        rack_switch_id = rack_data.get('switch_id', self.switch_id)
        rack_layout_config = SWITCH_LAYOUTS[rack_switch_id]

        # --- 1. Process Uplinks (High ports first) ---
        next_balanced_uplink_slice = rack_layout_config['PORT_COUNT'] // 8 - 1
        # Use priority order to ensure correct assignment: IPL, ISL, EXT, NB from highest port down
        for uplink_type in ['IPL', 'ISL', 'MLAG/BGP', 'NB']:
            uplink_info = rack_data.get('uplinks', {}).get(uplink_type, self._get_default_uplink_data(uplink_type))
            # IPL and NB are always single groups
            groups = 1 if uplink_type in ['IPL', 'NB'] else uplink_info.get('groups', 0)
            ppg = uplink_info.get('ports_per_group', 0)
            split = uplink_info.get('split', False)
            fac = uplink_info.get('factor', 2)
            reserved = uplink_info.get('reserved', 0)
            start_port_str = str(uplink_info.get('start', '')).strip()

            ports = []
            # Check if a manual start port is provided
            if start_port_str:
                spt_high = safe_int(start_port_str)
                # Get CN and EB counts for NB port labeling
                cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if uplink_type == 'NB' and hasattr(self, 'node_entries') else 0
                eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if uplink_type == 'NB' and hasattr(self, 'node_entries') else 0
                ports = self.planner.generate_grouped_ports(uplink_type, groups, ppg, split, fac, spt_high, reserved, locked=True, cn_count=cn_count, eb_count=eb_count)
            elif rack_layout_config.get('BALANCED_UPLINK_ASSIGNMENT'):
                ports, _, next_balanced_uplink_slice = self._generate_cisco_balanced_uplink_ports(
                    uplink_type, groups, ppg, split, fac, reserved, assigned_ports, start_slice=next_balanced_uplink_slice)
            else:
                phys_per_group = math.ceil(ppg / fac) if split and fac > 1 else ppg
                total_span = (phys_per_group + reserved) * groups
                if total_span > 0:
                    spt_high = rack_layout_config.get('PORT_COUNT', 64)
                    while spt_high >= total_span and any(p in assigned_ports for p in range(spt_high - total_span + 1, spt_high + 1)):
                        spt_high -= 1
                    if spt_high >= total_span:
                        # Get CN and EB counts for NB port labeling
                        cn_count = safe_int(self.node_entries.get('CN', {}).get('cnt', QLineEdit()).text(), 0) if uplink_type == 'NB' and hasattr(self, 'node_entries') else 0
                        eb_count = safe_int(self.node_entries.get('EB', {}).get('cnt', QLineEdit()).text(), 0) if uplink_type == 'NB' and hasattr(self, 'node_entries') else 0
                        ports = self.planner.generate_grouped_ports(uplink_type, groups, ppg, split, fac, spt_high, reserved, locked=False, cn_count=cn_count, eb_count=eb_count)

            if ports:
                port_map.extend(ports)
                assigned_ports.update(p for p, _ in ports)

        # --- 2. Process Nodes (Low ports first) ---
        next_balanced_node_slice = 0
        for node_type in self.node_types:
            node_info = rack_data.get('nodes', {}).get(node_type, self._get_default_node_data())
            count = node_info.get('count', 0)
            split = node_info.get('split', False)
            fac = node_info.get('factor', 2)
            reserved = node_info.get('reserved', 0)
            node_start = node_info.get('start', 1)
            start_port_str = str(node_info.get('start_port', '')).strip()

            ports = []
            # Check if a manual start port is provided
            if start_port_str:
                spt = safe_int(start_port_str)
                ports, _ = self.planner.generate_node_ports(node_type, count, split, fac, spt, reserved, node_start)
            elif rack_layout_config.get('BALANCED_NODE_ASSIGNMENT'):
                ports, _, next_balanced_node_slice = self._generate_cisco9364_node_ports(
                    node_type, count, split, fac, reserved, node_start, assigned_ports, start_slice=next_balanced_node_slice)
            else:
                phys_needed = (math.ceil(count / fac) if split else count) + reserved
                if phys_needed > 0:
                    spt = 1
                    while any(p in assigned_ports for p in range(spt, spt + phys_needed)):
                        spt += 1
                    if spt + phys_needed - 1 <= rack_layout_config.get('PORT_COUNT', 64):
                        ports, _ = self.planner.generate_node_ports(node_type, count, split, fac, spt, reserved, node_start)

            if ports:
                port_map.extend(ports)
                assigned_ports.update(p for p, _ in ports)

        return port_map, assigned_ports

    def select_output_directory(self):
        # This function is now informational, as the path is set by cluster name.
        # We can keep it to allow the user to see the full path.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_dir = os.path.join(script_dir, 'DesignOutput')
        d = QFileDialog.getExistingDirectory(self, 'Select Base Output Directory', default_dir)
        if d:
            # This doesn't change the actual output dir, just shows the user where it is.
            QMessageBox.information(self, "Output Directory", f"Output is organized by cluster name inside:\n\n{os.path.abspath(d)}")

    def load_switch_and_prepare(self):
        path = resource_path(self.layout_config['IMAGE'])
        try:
            self.base_image = Image.open(path).convert('RGBA')
            self.config_started = True
            self.setup_ready_to_load = False  # Reset indicator after loading
            self.reset_button.setEnabled(True)
            self.load_button.setVisible(False)
            self._update_button_indicator(self.load_button, False, 'Assign Switch')
            
            # Update status indicator
            if hasattr(self, 'setup_status_label'):
                self.setup_status_label.setText("✓ Status: Switch assigned - Ready to configure switches!")
                self.setup_status_label.setStyleSheet("font-weight: bold; color: #00FF00; padding: 5px;")
            
            
            # Update Cell Planning Advanced mode switch label
            if hasattr(self, 'cell_planning_advanced_switch_label'):
                self.cell_planning_advanced_switch_label.setText(f"Switch Model: {self.layout_config['NAME']}")
            
            self._on_multi_rack_toggled(self.multi_rack_checkbox.isChecked()) # Ensure rack 1 is created if needed
            # Trigger initial path setup
            self._update_output_paths(self.cluster_name_entry.text())
            self._reset_all_inputs()
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', f'Base image "{path}" not found')

    def _on_tab_changed(self, index):
        # --- IP Conflict Validation on Setup Tab ---
        # Check if we are trying to navigate *away* from the Setup tab to a different tab.
        allowed_destinations = ['Setup', 'Help', 'Legacy Installs']
        previous_tab_text = self.notebook.tabText(self.current_tab_index)
        if previous_tab_text == 'Setup' and self.notebook.tabText(index) not in allowed_destinations:
            if not self._validate_setup_ips():
                # If validation fails, block the tab change by switching back.
                # Use a QTimer to ensure the UI has time to process the initial tab change
                # tab change before we force it back.
                QTimer.singleShot(0, lambda: self.notebook.setCurrentIndex(self.current_tab_index))
                return # Stop further processing

        # Update the current tab index *after* the check.
        self.current_tab_index = index

        tab_text = self.notebook.tabText(index)
        is_multi_rack = self.multi_rack_checkbox.isChecked()

        if tab_text == 'Setup':
            if self.config_started:
                self.reset_button.setEnabled(True)
                self.load_button.setVisible(False)
            elif not is_multi_rack: # Prevent reset button from being disabled in multi-rack mode
                self.reset_button.setEnabled(False)
                self.load_button.setVisible(True)
            self._update_excuse_label()

        # --- Pre-Config Tab Access Validation ---
        # This check prevents navigating to most tabs before "Assign Switch" is clicked.
        # It's specifically designed to allow the 'Legacy Installs' tab to become visible
        # without being blocked, as setTabVisible() can trigger this signal.
        allowed_pre_config_tabs = ['Setup', 'Help', 'Legacy Installs']
        if not self.config_started and tab_text not in allowed_pre_config_tabs:
            QMessageBox.information(self, "Setup Required", "Please click 'Assign Switch' on the Setup tab before proceeding.\n\nReturning to Setup tab...")
            # Return to Setup tab instead of previous tab
            QTimer.singleShot(0, lambda: self.notebook.setCurrentIndex(self.notebook.indexOf(self.setup_tab)))
            self.current_tab_index = self.notebook.indexOf(self.setup_tab)
            return
        
        if tab_text == 'Multi-Rack' and is_multi_rack:
            self._draw_multi_rack_preview()

        # Trigger a redraw/recalc when switching to a preview tab.
        if tab_text in ['Cell Planning']:  # Uplinks tab is now hidden
            self._do_live_preview()
            # Also trigger advanced mode recalculation if in advanced mode
            if hasattr(self, 'cell_planning_mode') and self.cell_planning_mode == 'advanced':
                self._on_cell_planning_advanced_recalculate()
            # Update switch label for advanced mode
            if hasattr(self, 'cell_planning_advanced_switch_label'):
                switch_text = self.layout_config['NAME'] if self.config_started else 'Not loaded - configure on Setup tab'
                self.cell_planning_advanced_switch_label.setText(f"Switch Model: {switch_text}")
        elif tab_text == 'Output':
            self.output_rack_selector_widget.setVisible(is_multi_rack)
            if is_multi_rack:
                # Block signals while populating to avoid premature updates
                self.output_rack_selector_combo.blockSignals(True)
                self.output_rack_selector_combo.clear()
                if self.multi_rack_config:
                    rack_names = list(self.multi_rack_config.keys())
                    self.output_rack_selector_combo.addItems(rack_names)
                self.output_rack_selector_combo.blockSignals(False)
                # Manually trigger the update for the currently selected item
                if self.output_rack_selector_combo.count() > 0:
                    self._on_output_rack_selected(self.output_rack_selector_combo.currentText())
            else:
                # For single-rack mode, just update the view
                self._update_output_tab_view()
        
        # Automatically populate legacy fields when switching to that tab
        if tab_text == 'Legacy Installs':
            self._populate_legacy_from_setup()

    def _calculate_and_store_rack_port_map(self, rack_name: str):
        """Calculates the port map for a given rack and stores it in the data model."""
        if rack_name not in self.multi_rack_config:
            return

        rack_data = self.multi_rack_config[rack_name]
        port_map, _ = self._calculate_rack_port_map(rack_data)
        self.multi_rack_config[rack_name]['port_map'] = port_map

    def _validate_setup_ips(self) -> bool:
        """Validates IPs and VLANs on the Setup tab. Returns True if valid, False otherwise."""
        # --- VLAN Validation ---
        data_vlan = self.data_vlan_entry.text().strip()
        customer_vlans_str = self.customer_vlans_entry.text().strip()
        # Normalize customer VLANs into a set of strings
        customer_vlans = {v.strip() for v in customer_vlans_str.replace(',', ' ').split()}

        # 1. Critical: Data VLAN cannot be in Customer VLANs
        if data_vlan in customer_vlans:
            QMessageBox.critical(self, "VLAN Conflict Detected",
                                 f"The Data VLAN ({data_vlan}) cannot also be present in the 'Customer Vlans' list.\n\n"
                                 "Please remove it from one of the fields to continue.")
            return False

        # 2. Warning: VLAN 10 in Customer VLANs
        if '10' in customer_vlans:
            reply = QMessageBox.warning(self, "Potential Security Risk",
                                        "VLAN 10 was found in the 'Customer Vlans' list.\n\n"
                                        "Exposing VLAN 10 may expose the cluster backend network. "
                                        "This is only allowed in very specific configuration scenarios.\n\n"
                                        "Do you want to proceed?",
                                        QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
                                        QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Cancel:
                return False

        # --- IP Validation ---
        ip_fields_to_validate = {
            "Mgmt Default Route": self.net_def_route_entry,
            "FabricA Mgmt IP": self.switch_a_mgmt_ip_entry,
            "FabricB Mgmt IP": self.switch_b_mgmt_ip_entry,
            "NTP Server IP": self.ntp_server_entry,
        }

        # Get network CIDR for validation
        cidr_str = self.net_cidr_combo.currentText().strip()
        gateway_ip_str = self.net_def_route_entry.text().strip()
        
        # Create network object for validation if we have both gateway and CIDR
        network = None
        if gateway_ip_str and cidr_str:
            try:
                network = ipaddress.ip_network(f"{gateway_ip_str}/{cidr_str}", strict=False)
            except ValueError:
                # If we can't create the network, we'll still validate individual IPs
                pass

        # Validate each IP field for correct format and network boundaries
        for name, field in ip_fields_to_validate.items():
            ip_str = field.text().strip()
            if ip_str:  # Only validate non-empty fields
                try:
                    ip_obj = ipaddress.ip_address(ip_str)
                    
                    # Check if IP is valid for the network (if network is defined)
                    if network and name != "NTP Server IP":  # NTP server might be outside the management network
                        if ip_obj == network.network_address:
                            QMessageBox.critical(self, "Invalid IP Address",
                                                 f"The '{name}' field contains the network address ({ip_str}) which is not valid for host assignment in a /{network.prefixlen} network.\n\n"
                                                 f"Valid host IPs in this network range from {network.network_address + 1} to {network.broadcast_address - 1}.")
                            return False
                        
                        if ip_obj == network.broadcast_address:
                            QMessageBox.critical(self, "Invalid IP Address",
                                                 f"The '{name}' field contains the broadcast address ({ip_str}) which is not valid for host assignment in a /{network.prefixlen} network.\n\n"
                                                 f"Valid host IPs in this network range from {network.network_address + 1} to {network.broadcast_address - 1}.")
                            return False
                        
                        if ip_obj not in network:
                            QMessageBox.critical(self, "IP Address Out of Range",
                                                 f"The '{name}' field contains an IP address ({ip_str}) that is outside the management network ({network}).\n\n"
                                                 f"Please enter an IP address within the network range.")
                            return False
                            
                except ValueError:
                    QMessageBox.critical(self, "Invalid IP Address",
                                         f"The '{name}' field contains an invalid IP address: {ip_str}\n\n"
                                         "Please enter a valid IPv4 address (e.g., 192.168.1.1).")
                    return False

        # --- IP Conflict Validation ---
        gateway_ip_str = self.net_def_route_entry.text().strip()
        if not gateway_ip_str:
            return True  # No gateway to conflict with, and all checks passed

        try:
            gateway_ip = ipaddress.ip_address(gateway_ip_str)
        except ValueError:
            # This should not happen since we validated above, but just in case
            QMessageBox.critical(self, "Invalid Gateway IP",
                                 f"The 'Mgmt Default Route' contains an invalid IP address: {gateway_ip_str}\n\n"
                                 "Please enter a valid IPv4 address.")
            return False

        ip_fields_to_check = {
            "FabricA Mgmt IP": self.switch_a_mgmt_ip_entry,
            "FabricB Mgmt IP": self.switch_b_mgmt_ip_entry,
            "NTP Server IP": self.ntp_server_entry,
        }

        for name, field in ip_fields_to_check.items():
            field_ip_str = field.text().strip()
            if field_ip_str and field_ip_str == gateway_ip_str:
                QMessageBox.critical(self, "IP Conflict Detected", f"The 'Mgmt Default Route' ({gateway_ip_str}) cannot be the same as the '{name}'.\n\nPlease resolve the conflict before proceeding.")
                return False
        return True

    def _on_output_rack_selected(self, rack_name: str):
        """Handles rack selection on the Output tab."""
        if not rack_name:
            return
        self._update_output_tab_view()

    def _update_output_tab_view(self):
        """Updates the diagrams and bandwidth summary on the Output tab."""
        is_multi_rack = self.multi_rack_checkbox.isChecked()
        
        # Check if multi-rack config is empty (no racks cloned)
        has_multi_rack_data = bool(self.multi_rack_config and len(self.multi_rack_config) > 0)
        
        if is_multi_rack and has_multi_rack_data:
            # Multi-rack mode with actual racks
            rack_name = self.output_rack_selector_combo.currentText()
            self._update_output_canvas_for_rack(rack_name)
            self._calculate_and_display_bandwidth()
        elif not has_multi_rack_data:
            # No racks cloned - use current Cell Planning tab configuration
            # Determine which mode is active (Default or Advanced)
            if hasattr(self, 'cell_planning_mode_default_radio') and hasattr(self, 'cell_planning_mode_advanced_radio'):
                if self.cell_planning_mode_advanced_radio.isChecked():
                    # Advanced mode is active - use advanced port map
                    port_map = self.cell_planning_advanced_port_map if self.cell_planning_advanced_port_map else []
                    if not port_map:
                        # Recalculate if not available
                        port_map = self._calculate_cell_planning_advanced_ports()
                        self.cell_planning_advanced_port_map = port_map
                else:
                    # Default mode is active - use default port map
                    port_map = self._calculate_full_preview_port_map() or self.port_map
            else:
                # Fallback if mode radio buttons don't exist yet
                port_map = self._calculate_full_preview_port_map() or self.port_map
            
            # Display the port map on the Output tab canvases
            if port_map and self.base_image:
                df_raw = pd.DataFrame(port_map, columns=['Port ID', 'Port Name'])
                df_agg = df_raw.groupby('Port ID')['Port Name'].apply(lambda s: s.iloc[0]).reset_index()
                
                dfA = df_agg.copy()
                dfA['Fabric ID'] = 'A'
                dfA['Hostname'] = self.ha_entry.text().strip() or 'FabricA'
                
                dfB = df_agg.copy()
                dfB['Fabric ID'] = 'B'
                dfB['Hostname'] = self.hb_entry.text().strip() or 'FabricB'
                
                # Calculate scales and draw overlays
                scale_a = self.canvas_a.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.canvas_a.width() > 0 else 1.0
                imgA_display = self._draw_overlay(dfA, self.base_image, self.layout_config, display_scale=scale_a)
                self.canvas_a.setPixmap(pil_to_qpixmap(imgA_display))
                
                scale_b = self.canvas_b.width() / self.base_image.width if self.base_image and self.base_image.width > 0 and self.canvas_b.width() > 0 else 1.0
                imgB_display = self._draw_overlay(dfB, self.base_image, self.layout_config, display_scale=scale_b)
                self.canvas_b.setPixmap(pil_to_qpixmap(imgB_display))
            else:
                self.canvas_a.setText('⬅ Configure Cell Planning tab first')
                self.canvas_b.setText('⬅ Configure Cell Planning tab first')
            
            # Calculate bandwidth
            self._calculate_and_display_bandwidth()
        else:
            # Single-rack mode (not multi-rack checkbox)
            self.generate_overlays_and_export(export_files=False)

    def _update_output_canvas_for_rack(self, rack_name: str):
        """Updates the main Output tab canvases to show the specified rack's layout."""
        if not self.base_image or rack_name not in self.multi_rack_config:
            self.canvas_a.clear()
            self.canvas_b.clear()
            return

        port_map = self.multi_rack_config[rack_name].get('port_map', [])
        rack_switch_id = self.multi_rack_config[rack_name].get('switch_id', self.switch_id)
        rack_layout_config = SWITCH_LAYOUTS[rack_switch_id]
        rack_base_image = Image.open(resource_path(rack_layout_config['IMAGE'])).convert('RGBA')
        if not port_map:
            self.canvas_a.clear()
            self.canvas_b.clear()
            return

        df = pd.DataFrame(port_map, columns=['Port ID', 'Port Name'])
        scale = self.canvas_a.width() / rack_base_image.width if rack_base_image.width > 0 and self.canvas_a.width() > 0 else 1.0
        self.canvas_a.setPixmap(pil_to_qpixmap(self._draw_overlay(df.assign(**{'Fabric ID': 'A'}), rack_base_image, rack_layout_config, display_scale=scale)))
        self.canvas_b.setPixmap(pil_to_qpixmap(self._draw_overlay(df.assign(**{'Fabric ID': 'B'}), rack_base_image, rack_layout_config, display_scale=scale)))

    def _calculate_and_display_bandwidth(self):
        """Calculates and displays the bandwidth summary and audit on the Output tab."""
        is_multi_rack = self.multi_rack_checkbox.isChecked()
        
        # Check if multi-rack config has actual data
        has_multi_rack_data = bool(self.multi_rack_config and len(self.multi_rack_config) > 0)
        
        if is_multi_rack and has_multi_rack_data:
            rack_name = self.output_rack_selector_combo.currentText()
            if not rack_name or rack_name not in self.multi_rack_config:
                return # No rack selected or available
            port_map_to_use = self.multi_rack_config[rack_name].get('port_map', [])
            rack_switch_id = self.multi_rack_config[rack_name].get('switch_id', self.switch_id)
            rack_layout_config = SWITCH_LAYOUTS[rack_switch_id]
            # In multi-rack mode, get the goal from the specific rack's config
            goal_val = safe_int(self.multi_rack_config[rack_name].get('peak_bw_goal', ''), 0)
            goal_units = self.multi_rack_config[rack_name].get('peak_bw_units', 'GB/s')
        elif not has_multi_rack_data:
            # No racks cloned - use current Cell Planning tab configuration
            if hasattr(self, 'cell_planning_mode_advanced_radio') and self.cell_planning_mode_advanced_radio.isChecked():
                # Advanced mode is active
                port_map_to_use = self.cell_planning_advanced_port_map if self.cell_planning_advanced_port_map else []
                if not port_map_to_use:
                    port_map_to_use = self._calculate_cell_planning_advanced_ports() or []
            else:
                # Default mode is active
                port_map_to_use = self._calculate_full_preview_port_map() or self.port_map
            rack_layout_config = self.layout_config
            goal_val = safe_int(self.peak_bw_goal_entry.text(), 0)
            goal_units = self.peak_bw_units_combo.currentText()
        else:
            # In single-rack mode, use live preview data for accurate bandwidth calculation
            port_map_to_use = self._calculate_full_preview_port_map() or self.port_map
            # In single-rack mode, the layout config is the global one
            rack_layout_config = self.layout_config
            # In single-rack mode, get the goal from the main Setup tab
            goal_val = safe_int(self.peak_bw_goal_entry.text(), 0)
            goal_units = self.peak_bw_units_combo.currentText()

        if not port_map_to_use:
            # Clear the labels if there's no data
            self.bw_target_label.setText("Not Set")
            # (You might want to clear other labels here too if needed)
            return

        # Define conversion factors for clarity and to avoid magic numbers.
        BITS_IN_BYTE = 8
        GIB_TO_GB_FACTOR = (2**30) / (10**9) # Gibibytes to Gigabytes

        def parse_speed(speed_str):
            if not speed_str: return 0
            return safe_int(speed_str.upper().replace('G', ''), 0)

        native_speed_val = parse_speed(rack_layout_config.get('NATIVE_SPEED', ''))
        uplink_speed_str = self.uplink_speed_combo.currentText()
        uplink_speed_val = parse_speed(uplink_speed_str) or native_speed_val
        
        # Calculate bandwidths directly in Gb/s.
        bw = {'cn': 0, 'eb': 0, 'nb': 0, 'isl': 0, 'ext': 0}

        df = pd.DataFrame(port_map_to_use, columns=['Port ID', 'Port Name']).drop_duplicates(subset=['Port ID'])
        df['Base Type'] = df['Port Name'].apply(get_port_base_type)

        for _, row in df.iterrows():
            base_type = row['Base Type']

            if base_type == 'CN':
                bw['cn'] += native_speed_val
            elif base_type == 'EB':
                bw['eb'] += native_speed_val
            elif base_type == 'NB':
                bw['nb'] += native_speed_val
            elif base_type == 'ISL':
                bw['isl'] += native_speed_val
            elif base_type in ('MLAG/BGP', 'EXT'):
                bw['ext'] += uplink_speed_val

        # Convert the goal to Gb/s for comparison. Port speeds are in Gb/s.
        # The UI shows GB/s (Gigabytes) or GiB/s (Gibibytes), so we multiply by 8 to get bits.
        if goal_units == 'GiB/s':
            # 1 GiB/s = (2^30 * 8) / 10^9 Gb/s ~= 8.59 Gb/s
            goal_gbps = goal_val * GIB_TO_GB_FACTOR * BITS_IN_BYTE
        else: # Default to GB/s
            # 1 GB/s = 8 Gb/s
            goal_gbps = goal_val * BITS_IN_BYTE

        def format_bw(value):
            """Formats the value (in Gb/s) to the user-selected units."""
            if goal_units == 'GiB/s':
                # Convert Gb/s to GiB/s
                converted_val = (value / BITS_IN_BYTE) / GIB_TO_GB_FACTOR
                unit = "GiB/s"
            else: # Default to GB/s
                # Convert Gb/s to GB/s
                converted_val = value / BITS_IN_BYTE
                unit = "GB/s"
            return f"{converted_val:.1f} {unit}"

        def get_audit_label(value, goal, is_ext=False, isl_bw=0):
            if goal == 0: return ""
            if is_ext and value == 0:
                return "<font color='red'>X</font>"
            # Use a small tolerance for floating point comparisons
            if value >= goal or abs(value - goal) < 1e-9:
                if is_ext and value < isl_bw:
                    return "<font color='yellow'>✓</font>"
                return "<font color='green'>✓</font>"
            else:
                return "<font color='red'>X</font>"

        # Display the goal as entered by the user, without conversion.
        self.bw_target_label.setText(f"{goal_val} {goal_units.replace('/s', '')}" if goal_val > 0 else "Not Set")
        self.bw_target_audit.setText("🎯" if goal_gbps > 0 else "")

        # Northbound ports take precedence over CN/EB ports for customer bandwidth
        nb_bw_per_switch = bw['nb'] if bw['nb'] > 0 else (bw['cn'] + bw['eb'])
        nb_bw_aggregate_pair = nb_bw_per_switch * 2

        # Display per-switch and aggregate values
        self.bw_nb_a_label.setText(format_bw(nb_bw_per_switch))
        self.bw_nb_b_label.setText(format_bw(nb_bw_aggregate_pair))

        # Audit against the goal. The per-switch audit is for information,
        # while the aggregate audit determines if the cluster meets the total goal.
        self.bw_nb_a_audit.setText(get_audit_label(nb_bw_per_switch, goal_gbps))
        self.bw_nb_b_audit.setText(get_audit_label(nb_bw_aggregate_pair, goal_gbps))

        self.bw_isl_a_label.setText(format_bw(bw['isl']))
        # To show the total capacity of the link between the switch pair, the aggregate
        # value is calculated by doubling the per-switch bandwidth.
        isl_bw_per_switch = bw['isl']
        isl_bw_aggregate_pair = isl_bw_per_switch * 2
        self.bw_isl_b_label.setText(format_bw(isl_bw_aggregate_pair))

        self.bw_ext_a_label.setText(format_bw(bw['ext']))
        self.bw_ext_b_label.setText(format_bw(bw['ext']))

        # HA check assumes 50% of bandwidth is lost in a single switch failure
        # For ISLs, a single switch failure means the link capacity is halved.
        ha_isl_bw = isl_bw_aggregate_pair / 2
        ha_ext_bw = bw['ext'] / 2

        self.bw_isl_per_switch_audit.setText(get_audit_label(isl_bw_per_switch, goal_gbps))
        self.bw_isl_aggregate_audit.setText(get_audit_label(isl_bw_aggregate_pair, goal_gbps))
        self.bw_isl_a_ha_audit.setText(get_audit_label(ha_isl_bw, goal_gbps))
        self.bw_isl_b_ha_audit.setText(get_audit_label(ha_isl_bw, goal_gbps))
        self.bw_ext_a_audit.setText(get_audit_label(bw['ext'], goal_gbps, is_ext=True, isl_bw=bw['isl']))
        self.bw_ext_b_audit.setText(get_audit_label(bw['ext'], goal_gbps, is_ext=True, isl_bw=bw['isl']))
        self.bw_ext_a_ha_audit.setText(get_audit_label(ha_ext_bw, goal_gbps, is_ext=True, isl_bw=ha_isl_bw))
        self.bw_ext_b_ha_audit.setText(get_audit_label(ha_ext_bw, goal_gbps, is_ext=True, isl_bw=ha_isl_bw))

        # Align audit icons to the center
        for audit_label in [self.bw_nb_a_audit, self.bw_nb_b_audit, self.bw_isl_per_switch_audit, self.bw_isl_aggregate_audit,
                              self.bw_ext_a_audit, self.bw_ext_b_audit, self.bw_isl_a_ha_audit, self.bw_isl_b_ha_audit,
                              self.bw_ext_a_ha_audit, self.bw_ext_b_ha_audit]:
            audit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # --- Legacy Install Generation Logic ---

    def _confirm_legacy_action(self) -> bool:
        """Shows a confirmation dialog for legacy actions and returns True if the user clicks OK."""
        msg = "These configurations should be reviewed for completeness, and may require non-standard options."
        reply = QMessageBox.question(self, "Legacy Configuration Notice", msg,
                                     QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        return reply == QMessageBox.StandardButton.Ok

    def _save_legacy_output(self):
        """Saves the content of the legacy output text area to a file."""
        if not self._confirm_legacy_action():
            return

        cluster_name = self.legacy_cluster_name.text().strip() or "UnnamedCluster"
        ls_type = self.leaf_spine_combo.currentText()
        
        # Create descriptive filename with cluster, leaf/spine names
        default_filename = f"{cluster_name}_{ls_type}_install_commands.txt"

        filepath, _ = QFileDialog.getSaveFileName(self, "Save Legacy Commands", os.path.join(self.out_dir, default_filename), "Text Files (*.txt);;All Files (*)")
        if not filepath:
            return

        try:
            with open(filepath, 'w') as f:
                f.write(self.legacy_output_text.toPlainText())
            self._show_timed_messagebox("Save Successful", f"Output saved to:\n{os.path.basename(filepath)}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save file: {e}")

    def _generate_legacy_commands(self):
        """Gathers inputs from the UI and generates the legacy install command script."""
        if not self._confirm_legacy_action():
            return

        generator = LegacyCommandGenerator(self)
        script_content, errors = generator.generate()

        if errors:
            error_message = "\n".join(errors)
            QMessageBox.critical(self, "Validation Error", error_message)
            self.legacy_output_text.clear()
            return

        if script_content:
            self.legacy_output_text.setText(script_content)
            self._show_timed_messagebox("Success", "Legacy install commands generated successfully.")

    def _populate_legacy_from_setup(self):
        """Automatically populates the Legacy Installs tab with values from the Setup tab."""
        if not self.config_started:
            QMessageBox.warning(self, "Setup Not Started", "Please load a switch on the 'Setup' tab before importing.")
            return
 
        # Customer Name
        if customer_name := self.customer_name_entry.text():
            self.legacy_customer.setText(customer_name)
 
        # Cluster Name
        if cluster_name := self.cluster_name_entry.text():
            self.legacy_cluster_name.setText(cluster_name)
 
        # NTP Servers
        if ntp_server := self.ntp_server_entry.text():
            self.legacy_ntp.setText(ntp_server)
 
        # Mgmt Netmask (from CIDR)
        try:
            cidr = self.net_cidr_combo.currentText()
            netmask = ipaddress.IPv4Network(f'0.0.0.0/{cidr}').netmask
            self.legacy_mgmt_netmask.setText(str(netmask))
        except (ValueError, ipaddress.AddressValueError):
            pass # Ignore if CIDR is invalid
 
        # Mgmt Default Route
        if mgmt_route := self.net_def_route_entry.text():
            self.legacy_ext_gateway.setText(mgmt_route)
 
        # Switch IPs (Fabric A/B Mgmt IP from Setup -> Backend Switch 1/2 IP in Legacy)
        if fabric_a_ip := self.switch_a_mgmt_ip_entry.text():
            self.legacy_switch1.setText(fabric_a_ip)
        if fabric_b_ip := self.switch_b_mgmt_ip_entry.text():
            self.legacy_switch2.setText(fabric_b_ip)
 
        # Checkboxes
        self.legacy_mellanox_switches.setChecked('MNLX' in self.vendor_combo.currentText())

        # Switch OS mapping
        setup_os = self.vendor_combo.currentText()
        if setup_os == 'MNLX-Onyx':
            self.legacy_switch_os.setCurrentText('Onyx')
        elif setup_os == 'MNLX-Cumulus':
            self.legacy_switch_os.setCurrentText('Cumulus')

        self.legacy_rdma_pfc.setChecked(self.pfc_checkbox.isChecked())
        self.legacy_vxlan.setChecked(self.vxlan_checkbox.isChecked())
        # The logic for "Skip Secondary NIC" is inverted between the two pages.
        # Setup: "Use 2nd Nic?" (Yes/No) -> Legacy: "Skip Secondary NIC?" (Checked/Unchecked)
        self.legacy_skip_nic.setChecked(not self.use_2nd_nic_checkbox.isChecked())

        # Data VLAN mapping
        data_vlan = self.data_vlan_entry.text().strip()
        if data_vlan and data_vlan != '69':
            self.legacy_change_vlan.setChecked(True)
            self.legacy_vlan_id.setText(data_vlan)

    def _update_legacy_hostname_example(self):
        """Updates the example hostname label in real-time as the user types."""
        template = self.legacy_hostname_template.text().strip()

        if template:
            # Use sample data to generate the example
            base_placeholders = {
                'customer': self.legacy_customer.text().strip() or 'cust',
                'cluster': self.legacy_cluster_name.text().strip() or 'cl1',
                'rack': self.legacy_rack_identifier.text().strip() or 'r1',
            }

            try:
                # Try Python string formatting first (supports {num:03d} etc.)
                cnode_example = template.format(**base_placeholders, type='cn', num=1)
                dnode_example = template.format(**base_placeholders, type='dn', num=100)
                ebox_example = template.format(**base_placeholders, type='eb', num=1)
            except (KeyError, ValueError):
                # Fallback to simple string replacement for basic placeholders
                cnode_example = template
                dnode_example = template
                ebox_example = template
                
                # Replace basic placeholders
                for key, value in base_placeholders.items():
                    cnode_example = cnode_example.replace(f'{{{key}}}', str(value))
                    dnode_example = dnode_example.replace(f'{{{key}}}', str(value))
                    ebox_example = ebox_example.replace(f'{{{key}}}', str(value))
                
                # Replace type and number placeholders
                cnode_example = cnode_example.replace('{type}', 'cn').replace('{num}', '1')
                dnode_example = dnode_example.replace('{type}', 'dn').replace('{num}', '100')
                ebox_example = ebox_example.replace('{type}', 'eb').replace('{num}', '1')

            self.legacy_hostname_example_label.setText(f"Example: {cnode_example}, {dnode_example}, {ebox_example}")
        else:
            # Show default example based on architecture
            self.legacy_hostname_example_label.setText("Example: (default is cnode1, dnode100, eb1)")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Port-Mapper GUI Application (PyQt6)')
    parser.add_argument('--legacy', action='store_true', help='Enable legacy installation variables')
    args = parser.parse_args()

    # Directories will be created dynamically based on Customer/Site/Cluster names
    
    app = QApplication(sys.argv)

    # Dynamically add the background image to the main stylesheet. This avoids
    # using `widget.setStyleSheet()`, which would override all other app-wide styles
    # for that widget and its children.
    final_stylesheet = STYLESHEET
    try:
        image_path = resource_path('vast-man.jpeg')
        image_path_str = image_path.replace('\\', '/')
        background_style = f"""
            QWidget#SetupTab {{
                background-image: url({image_path_str});
            }}
        """
        final_stylesheet += background_style
    except Exception as e:
        print(f"INFO: Could not load setup background image for stylesheet: {e}")
    app.setStyleSheet(final_stylesheet)

    main_window = PortMapperPyQt(legacy_mode=args.legacy)
    main_window.show()

    sys.exit(app.exec())
