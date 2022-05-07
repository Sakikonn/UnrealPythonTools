// Copyright Epic Games, Inc. All Rights Reserved.

#include "PythonTools.h"
#include "PythonToolsStyle.h"
#include "PythonToolsCommands.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"
#include "IPythonScriptPlugin.h"
#include "PythonToolsUtil.h"

static const FName PythonToolsTabName("PythonTools");

#define LOCTEXT_NAMESPACE "FPythonToolsModule"

void FPythonToolsModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module

	PythonToolsUtil::PythonToolsInitialize();

	FPythonToolsStyle::Initialize();

	FPythonToolsStyle::ReloadTextures();

	FPythonToolsCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FPythonToolsCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FPythonToolsModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FPythonToolsModule::RegisterMenus));
}

void FPythonToolsModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FPythonToolsStyle::Shutdown();

	FPythonToolsCommands::Unregister();
}

// Button Click Event
void FPythonToolsModule::PluginButtonClicked()
{
	PythonToolsUtil::PluginButtonClickedEvent();
}

void FPythonToolsModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FPythonToolsCommands::Get().PluginAction, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar.PlayToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("PluginTools");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FPythonToolsCommands::Get().PluginAction));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}



#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FPythonToolsModule, PythonTools)