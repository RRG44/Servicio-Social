# Create an Executable for your OS from this Repo!
1. Install python version different from Anaconda. We recommend 3.10. Also download UPX for your OS from [here](https://github.com/upx/upx/releases/tag/v4.2.4) and unzip it 
2. Using Python create a virtual environment as follows (**don't use Anaconda or any other environment!**):

    2.1. Create a folder in your preferred path. Example : `D:\> mkdir vEnv`
    
    2.2. Change to that folder and then execute: `D:\vEnv> python -m venv vEnv`
    
    2.3. Base on your OS search for the folder `Scripts` or `bin` and execute the command based on your OS. Example: `D:\vEnv\vEnv\Scripts> activate.bat`

    | Platform | Shell | Command to activate virtual environment |
    | -------- | ----- | --------------------------------------- |
    | POSIX | bash/zsh | $ source <venv>/bin/activate |
    | POSIX | fish | $ source <venv>/bin/activate.fish |
    | POSIX | csh/tcsh | $ source <venv>/bin/activate.csh |
    | POSIX | PowerShell | $ <venv>/bin/Activate.ps1 |
    | Windows | cmd.exe | C:\> <venv>\Scripts\activate.bat |
    | Windows | PowerShell | PS C:\> <venv>\Scripts\Activate.ps1 |

    Now your venv is active! **Don't close the CLI**

3. Clone this repo in another folder
4. On the same instance of the CLI open the folder repo and execute: 

    For CLI App: `D:\Servicio-Social> python -m pip install -r requirements.txt`
    
    For GUI App: `D:\Servicio-Social> python -m pip install -r requirementsGUI.txt`

5. Finally execute the command replacing \<this parameters\>:
    
    For CLI App: `pyinstaller --onefile --upx-dir <path to your unzipped upx.exe> --clean --name <name of the app> --icon assets\iconcd.ico main.py`
    
    For GUI App: `pyinstaller --onefile --windowed --upx-dir <path to your unzipped upx.exe> --clean --name <name of the app> --icon assets\iconcd.ico gui.py`

6. Your app will be in the `dist` folder of the repo!

For closing the venv execute `deactivate`.

You can delete all the folders creates by pyinstaller and those related to the venv.