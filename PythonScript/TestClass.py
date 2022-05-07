import unreal
# NOTE 生成一个 Unreal Class 对象
@unreal.ustruct()
class TestStruct(unreal.StructBase):
    Args1 = unreal.uproperty(str)
    Args2 = unreal.uproperty(float)
    Args3 = unreal.uproperty(unreal.Text)

@unreal.uclass()
class PyBPFunctionLibrary(unreal.BlueprintFunctionLibrary): # 这个括号里是继承的对象
    # 没有参数的函数
    @unreal.ufunction(static=True,meta=dict(Category="Python Blueprint"))
    def TestFunction1():
        unreal.SystemLibrary.print_string(None,'Python Test Function Run',text_color=[255,255,255,255])

    # 两个参数的函数
    @unreal.ufunction(params=[str,str],static=True,meta=dict(Category="Python Blueprint"))
    def TestFunction2(arg1,arg2):
        unreal.SystemLibrary.print_string(None,'Python Test Function Run',text_color=[255,255,255,255])

    # 两个参数并且有一个返回值的函数
    @unreal.ufunction(ret=str,params=[str,str],static=True,meta=dict(Category="Python Blueprint"))
    def TestFunction3(arg1,arg2):
        unreal.SystemLibrary.print_string(None,'Python Test Function Run',text_color=[255,255,255,255])
        return 'Python Test Function Run'


    @unreal.ufunction(params=[str,float],static=True,meta=dict(Category="Python Blueprint"))
    def MyFunction(string,float2):
        result = TestStruct()
        for x in range(int(float2)):
            result.Args1 = result.Args1+'-'+string
        result.Args2=float2
