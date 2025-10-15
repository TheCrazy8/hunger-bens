; Inno Setup script to build HungerBensInstaller.exe
; Requires: Inno Setup 6 (iscc)

#define MyAppName "Hunger Bens"
#define MyAppPublisher "Your Company or Name"
#define MyAppURL "https://github.com/TheCrazy8/hunger-bens"
#define MyAppExeName "HungerBens.exe" ; Built by PyInstaller --name=HungerBens
#define MyAppVersion GetEnv('APP_VERSION')
#ifndef MyAppVersion
  #define MyAppVersion "1.0.0"
#endif

[Setup]
AppId={{73A331F9-76C8-4D3E-832D-8F3B3B6D22D6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=HungerBensInstaller
OutputDir=out
WizardStyle=modern
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
DisableWelcomePage=no
LicenseFile=..\LICENSE
; Uncomment and set if you have an icon for the installer itself
; SetupIconFile=icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Dirs]
; Create a shared data folder for assets writable by all users
Name: "{commonappdata}\HungerBens"; Flags: uninsalwaysuninstall
; Ensure plugins folder exists for machine-wide plugins
Name: "{commonappdata}\HungerBens\plugins"; Flags: uninsalwaysuninstall

[Files]
; Install the application binaries built by PyInstaller (adjust Source if folder name differs)
Source: "..\\dist\\HungerBens\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Optionally include default assets/configs into ProgramData (shared)
; Source: "assets\*"; DestDir: "{commonappdata}\HungerBens"; Flags: ignoreversion recursesubdirs createallsubdirs onlyifdoesntexist

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Optionally remove shared data on uninstall; comment out if you want to keep user data
Type: filesandordirs; Name: "{commonappdata}\HungerBens"

; Notes:
; - Per-user data is best created by the application itself under {localappdata}\HungerBens
;   at first run. Installing to {userappdata} during an elevated install can target the admin
;   profile instead of the eventual end-user.
; - If your PyInstaller output folder is named differently, change Source and MyAppExeName above.
