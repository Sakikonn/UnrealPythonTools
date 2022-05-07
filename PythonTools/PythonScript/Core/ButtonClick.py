import unreal
BlueprintClass = unreal.EditorAssetLibrary.load_asset("EditorUtilityWidgetBlueprint'/Game/EdUMG_MainMenu.EdUMG_MainMenu'")
if BlueprintClass:
    unreal.EditorUtilitySubsystem().spawn_and_register_tab_and_get_id(BlueprintClass)
else:
    unreal.log_warning("No Found Blueprint Asset...")