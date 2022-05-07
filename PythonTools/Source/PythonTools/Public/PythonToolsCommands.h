// Copyright Epic Games, Inc. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Framework/Commands/Commands.h"
#include "PythonToolsStyle.h"

class FPythonToolsCommands : public TCommands<FPythonToolsCommands>
{
public:

	FPythonToolsCommands()
		: TCommands<FPythonToolsCommands>(TEXT("PythonTools"), NSLOCTEXT("Contexts", "PythonTools", "PythonTools Plugin"), NAME_None, FPythonToolsStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
