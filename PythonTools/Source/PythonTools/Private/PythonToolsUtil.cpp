// Fill out your copyright notice in the Description page of Project Settings.


#include "PythonToolsUtil.h"
#include <IPythonScriptPlugin.h>
#include <EngineSharedPCH.h>

PythonToolsUtil::PythonToolsUtil()
{
}

PythonToolsUtil::~PythonToolsUtil()
{
}

void PythonToolsUtil::PluginButtonClickedEvent()
{
	FString FilePath(FPaths::ProjectPluginsDir() / TEXT("PythonTools/PythonScript/Core/ButtonClick.py"));
	RunFile(FilePath);
}

void PythonToolsUtil::PythonToolsInitialize()
{
	IPythonScriptPlugin* PythonModule(IPythonScriptPlugin::Get());
	if (PythonModule)
	{
		PythonModule->OnPythonInitialized().AddLambda([PythonModule]()->void {
				FString FilePath(FPaths::ProjectPluginsDir() / TEXT("PythonTools/PythonScript/Core/initialization.py"));
				RunFile(FilePath);
			}
		);
	}
	// Test
	/*FString A = TEXT("E:/Unreal/UE5.0.0/UEPythonTest/Intermediate/Config/CoalescedSourceConfigs/PythonToolsSettings.ini");
	UPythonToolsSettings *Config =NewObject<UPythonToolsSettings>();
	Config->LoadConfig(UPythonToolsSettings::StaticClass(), *A);
	for (FString path : Config->Paths)
	{
		UE_LOG(LogTemp, Warning, TEXT("%s"), *path);
	}*/
}

void PythonToolsUtil::RunFile(FString FilePath)
{
	IPythonScriptPlugin* PythonModule(IPythonScriptPlugin::Get());
	if (PythonModule)
	{
		FPythonCommandEx PyCommand;
		PyCommand.Command = FilePath;
		PyCommand.ExecutionMode = EPythonCommandExecutionMode::ExecuteFile;
		PyCommand.FileExecutionScope = EPythonFileExecutionScope::Private;
		if (PythonModule->ExecPythonCommandEx(PyCommand))
		{
			// UE_LOG(LogTemp, Warning, TEXT("Success..."));
		}
		else
		{
			FString Result(PyCommand.CommandResult);
			// UE_LOG(LogTemp, Warning, TEXT("%s"), *Result);
		}
	}
}


