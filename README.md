# jar打开方式自动添加java版本
jar打开方式自动添加java版本

1.jar包运行不了：多半是jar文件打开方式没关联到java
2.jar运行多版本选择：打开方式只会显示“Java(TM) Platform SE binary”


给他一个java路径，剩下交给代码
代码先着java.exe文件，然后执行java -version来获取对应的版本，然后写入jar文件打开方式，在修改打开方式里面java的描述
