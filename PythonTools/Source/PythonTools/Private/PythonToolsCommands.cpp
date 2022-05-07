// Copyright Epic Games, Inc. All Rights Reserved.

#include "PythonToolsCommands.h"

#define LOCTEXT_NAMESPACE "FPythonToolsModule"

void FPythonToolsCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "PythonTools", "Execute PythonTools action", EUserInterfaceActionType::Button, FInputChord());
}

#undef LOCTEXT_NAMESPACE
