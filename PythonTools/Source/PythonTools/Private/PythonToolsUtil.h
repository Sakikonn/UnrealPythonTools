// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"

/**
 * 
 */
class PythonToolsUtil
{
public:
	PythonToolsUtil();
	~PythonToolsUtil();

	static void PluginButtonClickedEvent();

	static void PythonToolsInitialize();

	static void RunFile(FString FilePath);
};
