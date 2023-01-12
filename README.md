# **Cosmic KSP**

## **Overview**
A project to command the video game **[Kerbal Space Program](https://www.kerbalspaceprogram.com/)** using real ground station software, **[OpenC3](https://openc3.com//)**.

### Project Goals
- Send commands to KSP spacecraft from OpenC3
- Receive Telemetry from KSP in OpenC3
<!-- - Initialize a *simulation* instance of KSP and screen commands before sending them to the *real* instance
- Create a mission planning app for verifying commands in simulation prior to execution -->

## Requirements
- KSP
- OpenC3
- Python3.11

## **Communication**
KPS does not support external commanding or telemetry out of the box. To address this I use two mods provided by the KSP fan community.

### **KOS**
The [Kerbal Operating System](https://ksp-kos.github.io/KOS/), KOS, mod enables running scripts "onboard" the spacecraft from either a built in terminal or remotely from a Telnet connection.
The ability to run scripts also enables more complicated automated behavior than what can be sent in a single command. Such as:
- automated abort conditions
- PID control loops
- precise maneuvers
- modular behaviors

### **Telemachus**
The [Telemachus](https://github.com/TeleIO/Telemachus-1) mod provides a easy to use telemetry stream from KSP to a standard computer socket.
The telemetry covers almost everything players would want to know about the state of the spacecraft. Including:
- Position, Rotation and Orbit parameters
- Resource levels
- environment status

## **Relays**
While the above mods add a lot of needed interfaces, they are not directly compatible with OpenC3 and need a translation layer.

On the Telemetry side, OpenC3 accepts fixed width strings to decode into data while Telemachus sends json formatted text.
So a relay, written in Python, subscribes to the Telemachus stream, reformats the data into the format OpenC3 needs, then sends it to a different socket for OpenC3 to receive.

On the commanding side, we have the same formatting problem but also KOS can only be commanded via telnet. So the commanding relay subscribes to the socket for OpenC3 commands, reformats the commands and sends them to KSP via telnet.

These two relays form the translation layer between OpenC3 and KSP. They also include several injection points for testing and screening data flow.

<!-- ## **Simulation**
This ground station supports screening and simulation functions, used for verification and planning. The simulation is just a second instance of KSP, set up to be initialized quickly from the states of the real KSP instance.

Initialization is done through save file manipulation. A quick-save file acts as a snapshot of the real KPS instance state and is copied onto the simulation KSP state and reloaded.

## **Simulation Manager App**
The Simulation Manager App, **SMA**, is the application that manages the simulation state and can send commands to it. It can initialize the sim from the real, and send commands to the sim using the OpenC3 format.

The SMA is used during the real missions to screen commands prior to commanding the real spacecraft. This serves as a final check to make sure the command will function as expected.

#### Features:
- Manage the initialization of the *sim* from the *real* instance data.
- Directly command the *sim* instance

## **Mission Planning App**
The Mission Planning App, **MPA**, is an app to construct sequences of commands and validate them using the simulation game instance. It creates a savable mission plan that can be

#### Features:
- Construct a list of commands in order of execution
- Export the commands as a procedure document with instructions for the operator
- All SMA functions -->

# Instalation

## Install the openc3 plugin
- Install OpenC3 on your machine. [Instructions](https://openc3.com/docs/v5/installation)
- Copy the plugin openc3-cosmos-cosmicksp to the root openc3 directory
- build the plugin
  - in a terminal change the working directory to the openc3-cosmos-cosmicksp folder
  - execute "../openc3.sh cle rake build VERSION=1.0.0"
- Install the plugin
  - navigate to your OpenC3 Admin panel
  - add the plugin

## modify ksp
- Install the mods KOS and Telemachus to KSP

## Install Cosmic KSP
- In a terminal, change the workign directory to this repository's root directory
- Install with "pip install ."
- Run the relay by executing "CosmicRelay" in a terminal