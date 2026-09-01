; Harem booru-viewer Windows Installer

[Setup]
AppName=harem-booru-viewer
AppVersion=0.3.2-harem
AppPublisher=SlaviqueBots
AppPublisherURL=https://github.com/SlaviqueBots/harem-booru-viewer
DefaultDirName={localappdata}\harem-booru-viewer
DefaultGroupName=harem-booru-viewer
OutputBaseFilename=harem-booru-viewer-setup
OutputDir=dist
Compression=lzma2
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\harem-booru-viewer.exe
PrivilegesRequired=lowest

[Files]
Source: "dist\harem-booru-viewer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "licenses\*"; DestDir: "{app}\licenses"; Flags: ignoreversion

[Icons]
Name: "{group}\harem-booru-viewer"; Filename: "{app}\harem-booru-viewer.exe"
Name: "{autodesktop}\harem-booru-viewer"; Filename: "{app}\harem-booru-viewer.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Run]
Filename: "{app}\harem-booru-viewer.exe"; Description: "Launch harem-booru-viewer"; Flags: nowait postinstall skipifsilent

[Code]
var
  RemoveDataCheckbox: TNewCheckBox;

procedure InitializeUninstallProgressForm();
begin
  RemoveDataCheckbox := TNewCheckBox.Create(UninstallProgressForm);
  RemoveDataCheckbox.Parent := UninstallProgressForm;
  RemoveDataCheckbox.Left := 10;
  RemoveDataCheckbox.Top := UninstallProgressForm.ClientHeight - 50;
  RemoveDataCheckbox.Width := UninstallProgressForm.ClientWidth - 20;
  RemoveDataCheckbox.Height := 20;
  RemoveDataCheckbox.Caption := 'REMOVE ALL USER DATA (BOOKMARKS, CACHE, LIBRARY — DATA LOSS)';
  RemoveDataCheckbox.Font.Color := clRed;
  RemoveDataCheckbox.Font.Style := [fsBold];
  RemoveDataCheckbox.Checked := False;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  AppDataDir: String;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if RemoveDataCheckbox.Checked then
    begin
      AppDataDir := ExpandConstant('{userappdata}\harem-booru-viewer');
      if DirExists(AppDataDir) then
        DelTree(AppDataDir, True, True, True);
    end;
  end;
end;
