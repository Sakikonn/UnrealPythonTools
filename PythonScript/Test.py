import unreal
import sys
import argparse

def GetLevelActors(x=0,y=0,z=0):
    Actors = unreal.EditorActorSubsystem().get_selected_level_actors()
    for Actor in Actors:
        assert isinstance(Actor,unreal.Actor)
        Actor.add_actor_local_offset(unreal.Vector(x,y,z),sweep=False,teleport=False)
    pass

# 创建序列
def CreateSequence(AssetName,AssetPath,StartTime,EndTime):
    AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
    Sequence = unreal.AssetTools.create_asset(AssetTools,AssetName,AssetPath,unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
    unreal.LevelSequence.set_playback_start_seconds(Sequence,StartTime)
    unreal.LevelSequence.set_playback_end_seconds(Sequence,EndTime)
    unreal.LevelSequence.set_work_range_start(Sequence,StartTime)
    unreal.LevelSequence.set_work_range_end(Sequence,EndTime)
    unreal.LevelSequence.set_view_range_start(Sequence,StartTime)
    unreal.LevelSequence.set_view_range_end(Sequence,EndTime)
    # unreal.EditorTutorial().open_asset(Sequence)
    unreal.LevelSequenceEditorBlueprintLibrary().open_level_sequence(Sequence)
    pass

# 将场景中选择的Actor添加到当前打开的序列中
def BindSelectActorsToSequence():
    LevelSequenceEditorBlueprintLibrary = unreal.LevelSequenceEditorBlueprintLibrary()
    CurLevelSequence = LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()
    assert isinstance(CurLevelSequence,unreal.LevelSequence)
    startf = unreal.LevelSequence.get_playback_start(CurLevelSequence)
    endf = unreal.LevelSequence.get_playback_end(CurLevelSequence)
    print('--------------------------------------------')
    print(startf,endf)
    print('--------------------------------------------')
    Actors = unreal.EditorActorSubsystem().get_selected_level_actors()
    
    for Actor in Actors:
        # 给序列中Transform 用的字典
        ActorTransform = {}
        FTransform = unreal.Actor.get_actor_transform(Actor)
        ActorTransform['Location.X'] = FTransform.translation.x
        ActorTransform['Location.Y'] = FTransform.translation.y
        ActorTransform['Location.Z'] = FTransform.translation.z
        ActorTransform['Rotation.X'] = FTransform.rotation.x
        ActorTransform['Rotation.Y'] = FTransform.rotation.y
        ActorTransform['Rotation.Z'] = FTransform.rotation.z
        ActorTransform['Scale.X'] = FTransform.scale3d.x
        ActorTransform['Scale.Y'] = FTransform.scale3d.y
        ActorTransform['Scale.Z'] = FTransform.scale3d.z

        # unreal.LevelSequence.add_spawnable_from_instance(CurLevelSequence,Actor)
        # unreal.Actor.destroy_actor(Actor)
        BindingProxy = unreal.LevelSequence.add_possessable(CurLevelSequence,Actor)

        TransformTrack = BindingProxy.add_track(unreal.MovieScene3DTransformTrack)
        TransformSection = TransformTrack.add_section()
        unreal.MovieScene3DTransformSection.set_range(TransformSection,startf,endf) # 设置范围
        # 给每个通道设置对应的值
        all_channels = unreal.MovieScene3DTransformSection.get_channels(TransformSection)
        for channel in all_channels:
            temp = unreal.MovieSceneScriptingDoubleChannel.get_name(channel)
            unreal.MovieSceneScriptingFloatChannel.add_key(channel,unreal.FrameNumber(0),ActorTransform[str(temp).split('_')[0]])
            pass

    LevelSequenceEditorBlueprintLibrary.refresh_current_level_sequence()

# 删除内容浏览器中选中的序列
def DeleteSelectSequence():
    
    messageboxresult = unreal.EditorDialog().show_message("DeleteSequence","确认删除的序列是正确的吗",unreal.AppMsgType.OK_CANCEL,unreal.AppReturnType.CANCEL)
    if messageboxresult is unreal.AppReturnType.OK:
        Assets = unreal.EditorUtilityLibrary().get_selected_assets()

        def TestFunction(Asset):
            if isinstance(Asset,unreal.LevelSequence):
                unreal.EditorAssetLibrary.delete_loaded_asset(Asset)
            pass
        SlowTaskManager(Assets,TestFunction,"TestSlowTask").SlowTaskStart()

        # 旧
        # for Asset in Assets:
        #     # LevelSequence = unreal.LevelSequence.cast(Asset)
        #     if isinstance(Asset,unreal.LevelSequence):
        #         unreal.EditorAssetLibrary.delete_loaded_asset(Asset)
        #     pass
    pass

# 选择世界中标签为 (str)TargetLabel 的Actor
def SelectWorldActorFormLabel(TargetLabel='Cube'):
    Actors = unreal.EditorActorSubsystem().get_all_level_actors()
    TargetActors = [] #unreal.Array(unreal.Actor)
    for Actor in Actors:
        if unreal.Actor.get_actor_label(Actor) == TargetLabel:
            TargetActors.append(Actor)
    unreal.EditorActorSubsystem().set_selected_level_actors(TargetActors)
    pass

# 更方便的创建Slow Task (大概)
class SlowTaskManager(object):
    # inTaskObjects:是Slow Task中需要处理的对象数组
    # inTaskFunction:是处理单个TaskObject的方法(有一个固定参数用于传入TaskObject)
    # inTaskName:是Slow Task的名称
    # 例子:
        # Actors = unreal.EditorActorSubsystem().get_selected_level_actors()
        # def TestFunction(Actor):
        #     unreal.log_warning(Actor.get_actor_label())
        #     time.sleep(0.5) # 这个是测试用的 怕太快还没看见就完了
        #     pass
        # SlowTaskManager(Actors,TestFunction,"TestSlowTask").SlowTaskStart()
    # pass
    def __init__(self,inTaskObjects:unreal.Array,inTaskFunction,inTaskName:str) -> None:
        self.__TaskObjects = inTaskObjects
        self.__TaskFunction = inTaskFunction
        self.__Slow_Task_Len = len(self.__TaskObjects)
        self.__TaskName = inTaskName
        pass

    def __SlowTaskStart__(self, *args, **kwargs):
        unreal.log_warning("Tasks Start>>>")

    def __SlowTaskEnd__(self, *args, **kwargs):
        unreal.log_warning("Task End>>>>")

    def SlowTaskStart(self):
        self.__SlowTaskStart__()
        Slow_Task_Len = self.__Slow_Task_Len

        with unreal.ScopedSlowTask(Slow_Task_Len,self.__TaskName + "...") as slow_task:
            # slow_task.make_dialog(True)
            slow_task.make_dialog_delayed(1,True)
            schedule = 0
            for TaskObject in self.__TaskObjects:
                if slow_task.should_cancel():
                    break
                else:
                    self.__TaskFunction(TaskObject)
                    schedule+=1
                    slow_task.enter_progress_frame(1,self.__TaskName + '...' + str(schedule) +'/' +str(Slow_Task_Len))
        self.__SlowTaskEnd__()
    pass
#'zh-Hans'
#'en'
def SetEditorLanguage(language:str):
    unreal.InternationalizationLibrary().set_current_language(language,True)
    pass

def GetCurEditorLanguage():
    return unreal.InternationalizationLibrary().get_current_language()
    
def CreateMovieRenderPipelineSettings(): # 这是一个示例  如何创建一个MoviePipelineMasterConfig
    Asset_Tools = unreal.AssetToolsHelpers.get_asset_tools()
    # unreal.AssetTools.create_asset_with_dialog
    TupleName = unreal.AssetTools.create_unique_asset_name(Asset_Tools,'/Game/ASD/abc',"")
    UniquePackageName ,UniqueAssetName = TupleName # 存入唯一包名 和 唯一资产名
    Config = unreal.MoviePipelineMasterConfig.get_default_object()
    unreal.MoviePipelineMasterConfig.initialize_transient_settings(Config)
    print(unreal.MoviePipelineEditorLibrary.export_config_to_asset(Config,UniquePackageName,UniqueAssetName,False))
    unreal.log_error(TupleName)
    pass

def EditorMode():
    # unreal.log_error("Test...\n..\n.")
    # Actors = unreal.EditorActorSubsystem().get_selected_level_actors()
    # def TestFunction(Actor):
    #     unreal.log_warning(Actor.get_actor_label())
    #     pass
    # SlowTaskManager(Actors,TestFunction,"TestSlowTask").SlowTaskStart()
    # unreal.InternationalizationLibrary().set_current_language("zh-Hans",True)
   
    # unreal.LevelEditorSubsystem().editor_set_game_view(True)
    # unreal.log_warning(unreal.GameUserSettings().get_default_window_mode())

    # //////
    # CreateMovieRenderPipelineSettings()
    # //////

    # CreateAssetTest()
    Test()
    pass


def Test(): # ?
    # NewPackage = unreal.new_object(unreal.Package,None,'/Game/nametest')
    # print(NewPackage)
    # NewConfig = unreal.new_object(unreal.MoviePipelineShotConfig,NewPackage,"nametest")
    # print(NewConfig)
    
    # # NewConfig = unreal.MoviePipelineShotConfig()
    # unreal.EditorAssetLibrary.save_loaded_asset(NewConfig,False)
    # print("AAA")
    pass

def MovieRenderPipeline():
    LevelSequenceEditorBlueprintLibrary = unreal.LevelSequenceEditorBlueprintLibrary()
    CurLevelSequence = LevelSequenceEditorBlueprintLibrary.get_current_level_sequence()

    # unreal.MovieRenderPipelineProjectSettings()

    # unreal.SequencerTools().render_movie()
    MoviePipelineQueue = unreal.MoviePipelineQueueSubsystem().get_queue()
    print(MoviePipelineQueue)
    jobs = unreal.MoviePipelineQueue.get_jobs(MoviePipelineQueue)
    print(len(jobs))
    
    pass

if __name__ == "__main__":
    # 第一种传递参数的方式
    # for arg in sys.argv:
    #     print(arg)
    #     pass

    # 第二种传递参数的方式
    # parser = argparse.ArgumentParser(description='Manual to this script')
    # parser.add_argument('--gpus',type=str,default='0')
    # parser.add_argument('--Batch-size',type=int,default=233)
    # args = parser.parse_args()
    # print(args.gpus)
    # print(args.Batch_size)

    # parser = argparse.ArgumentParser(description='Manual to this script')
    # parser.add_argument('--Name',type=str,default='NullName')
    # parser.add_argument('--Path',type=str,default="/Game")
    # parser.add_argument('--StartTime',type=int,default=0)
    # parser.add_argument('--EndTime',type=int,default=5)
    # args = parser.parse_args()
    # CreateSequenceAsset(args.Name,args.Path,args.StartTime,args.EndTime)

    # ImportVideo()

    # SpawnActor()
    
    # Example()

    # GetLevelActors()
    pass

# 这个是C++自己新增的一个函数
def CreateAssetTest():
    Asset_Tools = unreal.AssetToolsHelpers.get_asset_tools()
    # unreal.AssetTools.create_asset_with_dialog
    TupleName = unreal.AssetTools.create_unique_asset_name(Asset_Tools,'/Game/ASD/abc',"")
    UniquePackageName ,UniqueAssetName = TupleName # 存入唯一包名 和 唯一资产名
    Config = unreal.MoviePipelineShotConfig.get_default_object()
    # unreal.MoviePipelineMasterConfig.initialize_transient_settings(Config)
    print(unreal.MoviePipelineUtilLibrary.export_shot_config_to_asset(Config,UniquePackageName,UniqueAssetName,False))
    unreal.log_error(TupleName)
    pass