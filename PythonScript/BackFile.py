import argparse
import unreal

# 创建媒体轨道
def AddSequenceTrackMedia(Sequence):
    # 添加轨道
    MediaTrack = unreal.LevelSequence.add_master_track(Sequence,unreal.MovieSceneMediaTrack) # 添加媒体轨道 如果添加成功 返回媒体轨道实例
    unreal.MovieSceneMediaTrack.set_display_name(MediaTrack,"DDD") # 修改媒体轨道的显示名字
    # 加载资产
    MediaVideo = '/Game/ASD/Video.Video'
    MediaVideoIns = unreal.load_asset(MediaVideo)
    # 给轨道里面添加东西
    MediaTrackContent = unreal.MovieSceneTrack.add_section(MediaTrack)
    # 设置内容属性 右键轨道中的内容的时候 的属性列表 名字有空格用_代替
    unreal.MovieSceneSection.set_range_seconds(MediaTrackContent,0,30)
    unreal.MovieSceneSection.set_editor_property(MediaTrackContent,'Media_Source',MediaVideoIns)
    print("--------------------" , MediaVideoIns , "----------------")


    MediaTrack = unreal.LevelSequence.add_master_track(Sequence,unreal.MovieSceneMediaTrack) # 添加媒体轨道 如果添加成功 返回媒体轨道实例
    unreal.MovieSceneMediaTrack.set_display_name(MediaTrack,"AAA") # 修改媒体轨道的显示名字
    pass

# 添加Actor绑定代理轨道
def AddSequenceTrackActor(Sequence):
    # unreal.LevelSequence.add_master_track(Sequence,unreal.MovieSceneSpawnTrack) 添加已生成轨道

    # 从类生成actor
    actorclass = unreal.EditorAssetLibrary.load_blueprint_class('/Game/ASD/MyActor.MyActor')
    # actor = unreal.EditorLevelLibrary.spawn_actor_from_object(actorclass,location=[0,0,100])
    # 创建轨道绑定至object
    # MasterTrack = unreal.LevelSequence.add_possessable(Sequence,actor)
    
    # 绑定代理object 需要object类
    SequencerBindingProxy = unreal.LevelSequence.add_spawnable_from_class(Sequence,actorclass)
    unreal.SequencerBindingProxy.set_display_name(SequencerBindingProxy,"これわ Object")
    # 添加轨道
    ObjectMovieSceneTrack = unreal.SequencerBindingProxy.add_track(SequencerBindingProxy,unreal.MovieScene3DTransformTrack)
    # 添加Transform轨道中部分
    ObjectMovieSceneSection = unreal.MovieScene3DTransformTrack.add_section(ObjectMovieSceneTrack)
    unreal.MovieSceneSection.set_range_seconds(ObjectMovieSceneSection,0,30)

    

    # 获取当前绑定中的所有轨道
    for track in unreal.SequencerBindingProxy.get_tracks(SequencerBindingProxy):
        print(unreal.MovieSceneTrack.get_class(track))
        pass
    

    pass

# Import Asset
def importTask(filename,destination_path):

    task = unreal.AssetImportTask()

    # task.set_editor_property('automated', True)

    task.set_editor_property('destination_name', '')

    task.set_editor_property('destination_path', destination_path)

    task.set_editor_property('filename',filename)

    task.set_editor_property('replace_existing', True)

    task.set_editor_property('save', True)

    return task

def ImportVideo():
    MyTask = importTask('C:/Users/Admin/Desktop/Video.mp4','/Game')
    unreal.AssetTools.import_asset_tasks(unreal.AssetToolsHelpers.get_asset_tools(),[MyTask])
    pass

# SpawnActorformClass
def SpawnActor():
    unreal.EditorActorSubsystem().spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(0,0,100))
    pass

# 创建序列资产
def CreateSequenceAsset(AssetName,AssetPath,StartTime,EndTime):
    AssetTool = unreal.AssetToolsHelpers.get_asset_tools()
    assert isinstance(AssetTool,unreal.AssetTools)
    Sequence = unreal.AssetTools.create_asset(AssetTool,AssetName,AssetPath,unreal.LevelSequence,unreal.LevelSequenceFactoryNew()) # or # AssetTool.create_asset("A","/Game",unreal.LevelSequence,unreal.LevelSequenceFactoryNew())
    assert isinstance(Sequence,unreal.LevelSequence)
    # unreal.LevelSequence.set_display_rate(Sequence,unreal.FrameRate(numerator=0,denominator=1))
    unreal.LevelSequence.set_playback_start_seconds(Sequence,StartTime)
    unreal.LevelSequence.set_playback_end_seconds(Sequence,EndTime)
    unreal.LevelSequence.set_work_range_start(Sequence,StartTime)
    unreal.LevelSequence.set_work_range_end(Sequence,EndTime)
    unreal.LevelSequence.set_view_range_start(Sequence,StartTime)
    unreal.LevelSequence.set_view_range_end(Sequence,EndTime)
    
    # AddSequenceTrackActor(Sequence=Sequence)
    return Sequence

def Example():
    # 添加可视性轨道
    def AddSequenceVisivilityTrack(ActorSequencerBindingProxy):
        VisibilityTrack = ActorSequencerBindingProxy.add_track(unreal.MovieSceneVisibilityTrack) # 添加可视性轨道
        unreal.MovieSceneVisibilityTrack.set_property_name_and_path(VisibilityTrack,'bhidden','bhidden')

        Visibility_Section = unreal.MovieSceneVisibilityTrack.add_section(VisibilityTrack)
        unreal.MovieSceneVisibilitySection.set_range_seconds(Visibility_Section,0,20) # 设置可视性轨道范围
        
        MovieSceneScriptingChannel = unreal.MovieSceneVisibilitySection.get_channels(Visibility_Section)[0] #获取通道0
        VisibilityChannleBool = unreal.MovieSceneScriptingBoolChannel.cast(MovieSceneScriptingChannel)

        for x in range(6):
            new_time = unreal.FrameNumber(x*100)
            unreal.MovieSceneScriptingBoolChannel.add_key(VisibilityChannleBool,new_time,True)
        pass
    # 添加绑定actor 由序列控制 actor
    def AddBindTransformTrack(ActorSequencerBindingProxy):
        TransformTrack = ActorSequencerBindingProxy.add_track(unreal.MovieScene3DTransformTrack)
        TransformSection = unreal.MovieScene3DTransformTrack.add_section(TransformTrack)
        unreal.MovieScene3DTransformSection.set_range_seconds(TransformSection,0,20)

        # all_channels = unreal.MovieScene3DTransformSection.get_channels(TransformSection)
        # 获取通道测试
        unreal.Transform(location=[0,0,100],rotation=[0,0,0],scale=[1,1,1])

        n = 0
        for Channle in unreal.MovieScene3DTransformSection.get_channels_by_type(TransformSection,unreal.MovieSceneScriptingDoubleChannel):
            print(Channle.channel_name)
            n+=1
            pass
        print(n)
        
        pass
    
    parser = argparse.ArgumentParser(description='Manual to this script')
    parser.add_argument('--Name',type=str,default='NullName')
    parser.add_argument('--Path',type=str,default="/Game")
    parser.add_argument('--StartTime',type=int,default=0)
    parser.add_argument('--EndTime',type=int,default=5)
    args = parser.parse_args()
    Sequence = CreateSequenceAsset(args.Name,args.Path,args.StartTime,args.EndTime)
    
    # 两种实现方式
    # 1
    # unreal.LevelSequence.add_master_track(Sequence,unreal.MovieSceneFadeTrack).add_section().set_range_seconds(0,20)

    # 2
    # master_track = unreal.LevelSequence.add_master_track(Sequence,unreal.MovieSceneFadeTrack)
    # section = unreal.MovieSceneFadeTrack.add_section(master_track)
    # unreal.MovieSceneFadeSection.set_range_seconds(section,0,20)

    # 以下是新建一个 Sequence 控制 actor轨道
    ActorSequencerBindingProxy = unreal.LevelSequence.add_spawnable_from_class(Sequence,unreal.EditorAssetLibrary.load_blueprint_class('/Game/ASD/MyActor.MyActor'))
    AddSequenceVisivilityTrack(ActorSequencerBindingProxy) # 添加可视性轨道 并且设置值

    AddBindTransformTrack(ActorSequencerBindingProxy)
    
    

    # 获取这个代理的所有子Track
    # Tranks = unreal.SequencerBindingProxy.get_tracks(ActorSequencerBindingProxy)
    # Section = unreal.MovieSceneSection.cast(unreal.MovieSceneTrack.get_sections(Track)[0])
    # Section.set_range_seconds(0,20)
    # # 获取0号bool通道
    # BoolChannel = unreal.MovieSceneScriptingBoolChannel.cast(unreal.MovieSceneSection.get_channels(Section)[0])
    # print(BoolChannel)
    # new_time = unreal.FrameNumber(100)
    # unreal.MovieSceneScriptingBoolChannel.add_key(BoolChannel,new_time,True)
    pass