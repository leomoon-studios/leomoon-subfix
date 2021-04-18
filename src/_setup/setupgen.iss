#define AppName "LeoMoon SubFix"
#define AppShortName "SubFix"
#define AppVersion "1.0.0"
#define AppExeName "LeoMoon SubFix.exe"
#define CompanyName "LeoMoon Studios"
#define AppWebsiteName "LeoMoon Studios Homepage"
#define AppWebsite "http://leomoon.com"
#define AppOutput "leomoon-subfix_win"

[Setup]
PrivilegesRequired=admin
DisableWelcomePage=no
AppId={#AppName}
AppName={#AppName}
AppVersion={#AppVersion}
VersionInfoVersion={#AppVersion}
AppPublisher={#CompanyName}
AppPublisherURL={#AppWebsite}
AppSupportURL={#AppWebsite}
AppUpdatesURL={#AppWebsite}
AppCopyright=Copyright (C) 2018 LeoMoon Studios
DefaultDirName={commonpf}\{#AppName}
DisableDirPage=yes
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
LicenseFile=EULA.txt
OutputDir=..\dist\build
OutputBaseFilename={#AppOutput}
SetupIconFile=setup.ico
Compression=lzma/ultra
InternalCompressLevel=ultra
SolidCompression=yes
DirExistsWarning=yes
UninstallDisplayIcon={app}\{#AppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "editordesktopicon"; Description: "{cm:CreateDesktopIcon} for {#AppName}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#AppName}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "istask.dll"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
;Program Files
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"
;Desktop Shortcuts
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: editordesktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall runascurrentuser skipifsilent

[Registry]
;fileassoc
;Root: HKCR; Subkey: ".aes"; ValueData: "{#AppShortName}"; Flags: uninsdeletevalue; ValueType: string; ValueName: ""
;Root: HKCR; Subkey: "{#AppShortName}"; ValueData: "Program {#AppName}";  Flags: uninsdeletekey;   ValueType: string;  ValueName: ""
;Root: HKCR; Subkey: "{#AppShortName}\DefaultIcon"; ValueData: "{app}\{#AppExeName},0"; ValueType: string; ValueName: ""
;Root: HKCR; Subkey: "{#AppShortName}\shell\open\command"; ValueData: """{app}\{#AppExeName}"" -d ""%1"""; ValueType: string; ValueName: ""
;right click entry
;Root: HKCR; Subkey: "*\shell\Encrypt with {#AppShortName}\command"; ValueData: """{app}\{#AppExeName}"" -e ""%1"""; ValueType: string; ValueName: ""
;Root: HKCR; Subkey: "*\shell\Decrypt with {#AppShortName}\command"; ValueData: """{app}\{#AppExeName}"" -d ""%1"""; ValueType: string; ValueName: ""

[Code]
function RunTask(FileName: ansistring; bFullpath: Boolean): Boolean;
	external 'RunTask@files:istask.dll stdcall delayload';
function KillTask(ExeFileName: ansistring): Integer;
	external 'KillTask@files:istask.dll stdcall delayload';

function InitializeSetup(): Boolean;
var
  uninstaller: String;
  ErrorCode: Integer;
begin
	Result:= true;
  if RunTask('{#AppExeName}', false) then
	begin
		KillTask('{#AppExeName}');
	end;
  if RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#AppName}_is1') then
  begin
	RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#AppName}_is1', 'UninstallString', uninstaller);
    ShellExec('runas', uninstaller, '/SILENT', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);
    Result := True;
  end;
end;

function RunTaskU(FileName: ansistring; bFullpath: Boolean): Boolean;
	external 'RunTask@{app}\istask.dll stdcall delayload uninstallonly';
function KillTaskU(ExeFileName: ansistring): Integer;
	external 'KillTask@{app}\istask.dll stdcall delayload uninstallonly';

function InitializeUninstall(): Boolean;
begin
	Result:= true;
  if RunTaskU('{#AppExeName}', false) then
	begin
		KillTaskU('{#AppExeName}');
	end;
  UnloadDll(ExpandConstant('{app}\istask.dll'));
end;