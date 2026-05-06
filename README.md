## Notes

### Project Airsim: 
- The official stable release (v0.1.1) is distributed as a prebuilt Unreal environment.
- There is no separate "stable source branch", but the prebuilt package is built from commit 9fe8d3a.
- This project uses the SAME source commit (v0.1.1 / 9fe8d3a), assuming it is stable since it was used to create the official prebuilt release.
- Instead of using the prebuilt binaries, we clone the source and build locally to allow customization.
- The only customized part is the Blocks folder: C:\ProjectAirSim\unreal\Blocks

### ProjectAirSim\unreal\Blocks:

- The ProjectAirSim repository is based on v0.1.1 / commit 9fe8d3a. However, the Unreal Blocks folder was originally taken from an untracked main-branch state and was customized before the repository was reset/checked out to v0.1.1.
- Because of this, the exact original commit for unreal/Blocks is unknown. The current Blocks folder should be treated as a custom local version, not a clean v0.1.1 copy.



# Setup: 

1) Install unreal engine 5.7 (put the location in local disk preferably) from EPIC Game Launcher: https://dev.epicgames.com/documentation/unreal-engine/install-unreal-engine

2) Download the Cesium Ion: https://www.unrealengine.com/en-US/download  
- Location of download (mandatory step to get plugins readable): C:\Program Files\Epic Games\UE_5.7\Engine\Plugins\Marketplace)

3) Use CfAR Cesium account for token

4) Git Clone Project Airsim (recommend using the ProjectAirsim_modified branch in this repo so all the neccesary configs/builds already done. Otherwise do the interfacing yourself):


5) Git clone main branch and place it in the same path as the Project Airsim cloned repo: 
git clone https://github.com/Tanya3333333/DigitalTwin-world.git

6) Install Python 3.12 and add to PATH

7) Create a virtual environment (.venv) in VSCode and activate it everytime: 
python -m venv .venv
.\.venv\Scripts\Activate.ps1

8) Install pip:
python -m pip install --upgrade pip 

9) Install ProjectAirSim Python client in venv - it would automatically look for the project airsim repo cloned:
pip install -e client/python/projectairsim

10) Install all other dependecies (libraries/packages) related to this repo: 
pip install -r requirements.txt

11) Open unreal by clicking on Block.sln file in folder: 
C:\Temp\ProjectAirSim\unreal\Blocks

12) once Visual Studio 2022 opend, then Ctrl+F5 --> this will build and launch Unreal  (this is how to launch the Unreal everytime)
Note: for the first time launch, go to Content Browser > Blocks > C++ Classes > Blocks > Public --> then drag and drop 'Actor_SetWorldOrigin' to the view port


# How to run the Pipeline:

1) Run PX4_SITL in Ubuntu OS (optional): 
px4_sitl none_iris 

2) Click Play (the green button) in Unreal in Windows OS

3) Run the interceptor_phys repo in VS Code in Ubuntu OS (optional): 
python -m sim.kernel.scheduler.scheduler_busy_Wait

4) Once home position received in Unreal Output Log, then in Windows VS Code, run this repo: 
py -m kernel.project_airsim_interface     

