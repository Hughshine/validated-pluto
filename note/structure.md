# Project Structure

pluto工作方式：一次优化一个scop，截取，运算，output；多次截取操作由polycc.sh完成，单次优化逻辑由pluto/main完成；pluto优化时不关心类型信息，用户负责。

<!-- autoconf: 
1. `configure.ac` -> `configure`
2. ./configure -->

本项目：`lib/`, `tool/`

其他项目：
1. math_support.h
2. osl_pluto.h, 这个应该是openscop和pluto表示转换的库
   1. osl/irregular.h，要支持的拓展
   2. osl/scop.h
3. pet_to_pluto.h，这个应该是用pet做extractor的库
   1. pet.h
      1. 具体用的是哪一种表示？
4. pluto.h, pluto/pluto.h, pluto核心算法
5. post_transform.h, 后续分块/并行化等算法
6. program.h，不知道
7. transforms.h，不知道
8. clan.h -- include 

pluto options 含义：
1. todo，整理，归类，和算法的对应

main.cpp 逻辑：
1. help message
2. 计时器
3. options, 整理，归类
4. extractor，pet或clan
   1. pet
      1. pet to pluto prog
      2. isl context
   2. clan
      1. read openscop
      2. extract openscop
      3. 对最终的scop做些检查
      4. backup irregular program portion

此时得到`prog`，类型是pluto prog。
1. statement number
2. loop dimension: 每一个指令的dim做和（似乎没有关心重复的dim，TODO）
3. deps number：dep怎么表示的？
4. 最大stmt维度
5. 参数数量（context）

后续操作（根据option选择）：
1. index set splitting
2. auto transform
3. compute dep directions/satisfaction
4. ... pprint, 前期transformation结果
5. tile/intratile
6. parallel (和tile不同时进行)
   1. skewing... obtain wavefront parallelization: todo
   2. 似乎同时会进行tile? ... 
7. 施加transformation引入的影响，变换回输入的representation
8. .cloog? 

最后，计时，内存释放

extractor

用的表示：支持isl吗，还是指支持openscop，还是...？