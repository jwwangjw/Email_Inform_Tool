# 一个简易的将新收到邮件进行微信通知的脚本

[toc]

## 一.使用python库

|   库    |               功能               |
| :-----: | :------------------------------: |
| poplib  |   登陆pop3服务器，获取邮件状态   |
|  email  | 将获取到的字符进行转码，便于显示 |
| request |      向server酱发送http请求      |

## 二.代码使用

1. 前去对应使用的邮箱进行pop3和smtp功能开启，获取授权码以代替密码（更加安全）

2. 去server酱按步骤注册企业微信，获取sendkey

3. 将sendkey以及邮箱名，授权码填入代码对应位置
4. 运行，若想不间断地运行，建议在服务器上通过nohup方式运行

## 三.借鉴代码说明

​	该脚本的获取部分来源于库自身api，获取转码部分来源于网络对email，server酱则是之前使用通知程序使用注册

## 四.版权说明

​	完全开源，可任意使用以及修改。