; FaceFusion Windows Installer Script
; Inno Setup Script for creating Windows installer

#define MyAppName "FaceFusion"
#define MyAppVersion "3.0.0"
#define MyAppPublisher "FaceFusion Team"
#define MyAppURL "https://facefusion.io"
#define MyAppExeName "FaceFusionLauncher.exe"

[Setup]
; Application information
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=no

; Output
OutputDir=output
OutputBaseFilename=FaceFusion-Setup-{#MyAppVersion}
Compression=lzma2
SolidCompression=yes

; Wizard appearance
WizardStyle=modern
WizardImageFile=installer_image.bmp
WizardSmallImageFile=installer_icon.bmp

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Uninstall
UninstallDisplayIcon={app}\facefusion.ico
UninstallDisplayName={#MyAppName}
CreateUninstallRegKey=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main application files
Source: "..\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: ".git,.github,tests,__pycache__,*.pyc,.gitignore"

; Launcher files
Source: "launcher.py"; DestDir: "{app}\windows_installer"; Flags: ignoreversion
Source: "install_wizard.py"; DestDir: "{app}\windows_installer"; Flags: ignoreversion

; Icons
Source: "..\facefusion.ico"; DestDir: "{app}"; Flags: ignoreversion

; Batch files for easy launching
Source: "launch_facefusion.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "setup_environment.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu icons
Name: "{group}\{#MyAppName}"; Filename: "pythonw.exe"; Parameters: """{app}\windows_installer\launcher.py"""; WorkingDir: "{app}"; IconFilename: "{app}\facefusion.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{group}\FaceFusion Documentation"; Filename: "https://docs.facefusion.io"

; Desktop icon
Name: "{autodesktop}\{#MyAppName}"; Filename: "pythonw.exe"; Parameters: """{app}\windows_installer\launcher.py"""; WorkingDir: "{app}"; IconFilename: "{app}\facefusion.ico"; Tasks: desktopicon

; Quick Launch icon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "pythonw.exe"; Parameters: """{app}\windows_installer\launcher.py"""; WorkingDir: "{app}"; IconFilename: "{app}\facefusion.ico"; Tasks: quicklaunchicon

[Registry]
; Add to Windows Registry
Root: HKLM; Subkey: "Software\{#MyAppName}"; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: "Software\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKLM; Subkey: "Software\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"

[Run]
; Run installation wizard after setup
Filename: "pythonw.exe"; Parameters: """{app}\windows_installer\install_wizard.py"""; Description: "Complete FaceFusion setup"; Flags: postinstall nowait skipifsilent

; Optional: Launch application
Filename: "pythonw.exe"; Parameters: """{app}\windows_installer\launcher.py"""; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

[Code]
var
  DependencyPage: TInputOptionWizardPage;
  AcceleratorPage: TInputOptionWizardPage;

procedure InitializeWizard;
begin
  { Create custom wizard page for dependencies }
  DependencyPage := CreateInputOptionPage(wpSelectDir,
    'Select Dependencies', 'Choose which dependencies to install',
    'The installer can automatically download and install required dependencies.',
    True, False);
  
  DependencyPage.Add('Install Git (if not already installed)');
  DependencyPage.Add('Install Miniconda (if not already installed)');
  DependencyPage.Add('Install FFmpeg (if not already installed)');
  
  { Set default values }
  DependencyPage.Values[0] := True;
  DependencyPage.Values[1] := True;
  DependencyPage.Values[2] := True;
  
  { Create custom wizard page for accelerator }
  AcceleratorPage := CreateInputOptionPage(DependencyPage.ID,
    'Choose Hardware Accelerator', 'Select your GPU type for optimal performance',
    'FaceFusion can use hardware acceleration for better performance.',
    True, False);
  
  AcceleratorPage.Add('Default (CPU only)');
  AcceleratorPage.Add('NVIDIA GPU (CUDA)');
  AcceleratorPage.Add('AMD GPU (DirectML)');
  AcceleratorPage.Add('Intel GPU (OpenVINO)');
  
  { Set default to CPU }
  AcceleratorPage.Values[0] := True;
end;

function GetAcceleratorType: String;
begin
  if AcceleratorPage.Values[1] then
    Result := 'cuda'
  else if AcceleratorPage.Values[2] then
    Result := 'directml'
  else if AcceleratorPage.Values[3] then
    Result := 'openvino'
  else
    Result := 'default';
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  PythonCmd: String;
  InstallCmd: String;
  Accelerator: String;
begin
  if CurStep = ssPostInstall then
  begin
    { Save installation preferences }
    Accelerator := GetAcceleratorType;
    
    { Create config file }
    SaveStringToFile(ExpandConstant('{app}\install_config.txt'), 
                     'accelerator=' + Accelerator + #13#10, False);
  end;
end;
