#include <TFT_eSPI.h>
#include <WiFi.h>
#include "time.h"
#include <HTTPClient.h>
#include "./res/Connect.h"
#include "./res/As.h"
#include "./res/MyFont.h"  // 自制字体模板库
#include <ArduinoJson.h>  //Json库

const char* ssid       = "mrw";
const char* password   = "88888888";
uint32_t targetTime = 0;
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 8*1800;
const int   daylightOffset_sec = 8*1800;
int tm_Hour,tm_Minute,monthDay,tm_Month;


int led = 2;
String From,TodayEmail,UnseenEmail,Title;

TFT_eSPI tft = TFT_eSPI();  //设定屏幕
void setTime(){
   struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);//初始化时间
    return;
  }
   tm_Hour = timeinfo.tm_hour;
   tm_Minute = timeinfo.tm_min;
  
  }

void ConnectToWifi()
{
 while(WiFi.status() != WL_CONNECTED){//自动重连
    int i = 0;
    WiFi.begin(ssid, password);              // 连接网络
    while (WiFi.status() != WL_CONNECTED)    //等待wifi连接
    {
      tft.pushImage(120, 150, 100, 20, ConnectWifi[i]);//循环播放动画
      i++;
      if(i > 5){
        WiFi.mode(WIFI_OFF);
        Serial.print("WIFI OFF");
        break;
        }
      delay(400);
      Serial.print(".");
    }
    }

    Serial.println("WiFi connected");        //连接成功
    Serial.print("IP address: ");            //打印IP地址
    Serial.println(WiFi.localIP());
    tft.fillScreen(TFT_WHITE);
    tft.pushImage(120, 150, 100, 20, ConnectWifi[5]);//调用图片数据
    tft.setCursor(120, 140, 1);           //设置文字开始坐标(15,30)及1号字体
    tft.setTextSize(1);
    tft.println("WiFi Connected!");
    delay(200);
}

int httpcount = 0;
void sendData(){
    //http
  while(true){
  String httpString;
  HTTPClient httpClient;
  httpClient.begin("http://124.221.181.50:10010/mail/");
  //httpClient.begin("http://192.168.147.240:8888/mail/");
  int httpCode = httpClient.GET();
  if (httpCode > 0) {
    if (httpCode == HTTP_CODE_OK) {
      
        httpString = httpClient.getString();
        Serial.println(httpString);
        //////////////////

    StaticJsonBuffer<256> jsonBuffer;

    JsonObject& root = jsonBuffer.parseObject(httpString);
//    deserializeJson(doc, httpString);

    From = root["From"].as<String>(); // 59
    Serial.println("From:" +From);
    TodayEmail = root["TodayEmailCount"].as<String>();
    Serial.println("TodayEmailCount:" +TodayEmail);
    UnseenEmail = root["UnseenEmailCount"].as<String>(); // 59
    Serial.println("UnseenEmailCount:" +UnseenEmail);
    Title = root["Title"].as<String>();
    Serial.println("Title:" +From);
        /////////////////
    return;
  }
  }
  else{
    
    httpcount++;
    Serial.print(httpcount);
    }     
      httpClient.end();
      
      if(httpcount>3){
        httpcount = 0;
        targetTime -=28*60*1000; //两分钟后再次刷新
        return;
      }
    
    }
  }
  
void setup()
{
  targetTime = millis() + 30*60*1000; 
  tft.setRotation(3);
  Serial.begin(115200);
  tft.init();                         //初始化显示寄存器
  tft.fillScreen(TFT_WHITE);          //屏幕颜色
  tft.setTextColor(TFT_BLACK);        //设置字体颜色黑色
  tft.setCursor(120, 140, 1);           //设置文字开始坐标(15,30)及1号字体
  tft.println("WiFi Connecting...");
  tft.setSwapBytes(true);             //使图片颜色由RGB->BGR
  for (int j = 0; j < 5; j++)
    {
        tft.pushImage(120, 150, 100, 20, ConnectWifi[j]);   //调用图片数据
        delay(400);  
    }
  ConnectToWifi();                         // Wifi连接
  
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);//初始化时间

  sendData();

  tft.fillScreen(TFT_BLACK);
  showEmail();
  }

void showtext(int16_t x,int16_t y,uint8_t font,uint8_t s,uint16_t fg,uint16_t bg,const String str)
{
  //设置文本显示坐标，和文本的字体，默认以左上角为参考点，
    tft.setCursor(x, y, font);
  // 设置文本颜色为白色，文本背景黑色
    tft.setTextColor(fg,bg);
  //设置文本大小，文本大小的范围是1-7的整数
    tft.setTextSize(s);
  // 设置显示的文字，注意这里有个换行符 \n 产生的效果
    tft.println(str);
}
bool a = true;
void showEmail(){

    tft.drawFastHLine(70, 72, 168, tft.alphaBlend(0, TFT_BLACK,  TFT_WHITE));
    showtext(75,87,1,2,TFT_WHITE,TFT_BLACK,"Today Email:"+TodayEmail);
    showtext(70,120,1,2,TFT_WHITE,TFT_BLACK,"Unseen Email:"+UnseenEmail);
    tft.drawFastHLine(70, 155, 168, tft.alphaBlend(0, TFT_BLACK,  TFT_WHITE));
        if(a){
      tft.fillRect(0,175,320,65,TFT_BLACK);//局部刷新屏幕,自己瞎想的
      a = !a;
      }
      
      if(*const_cast<char *>(UnseenEmail.c_str()) == '0'){
        
        showtext(75,180,1,3,TFT_WHITE,TFT_BLACK,"Nice Day!");
        }
       else{

        showtext(5,166,1,1,TFT_WHITE,TFT_BLACK,"From:");
        Serial.println(From); 
        showtext(5,180,1,2,TFT_WHITE,TFT_BLACK,From);
        Serial.println(Title); 
        showtext(5,200,1,1,TFT_WHITE,TFT_BLACK,Title);
        }

    //int32_t x, int32_t y, int32_t w, int32_t h, uint32_t color
    
  }
int img_count = 0;
int time_count = 0;
void show(uint16_t fg,uint16_t bg,const uint16_t* image[])
{

    //tft.fillRect(10, 55,  64, 64, bg);
    
    tft.setSwapBytes(true);             //使图片颜色由RGB->BGR

    setTime();                          //更新本地时间
    String currentTime, hour, minute;
    if (tm_Hour < 10)
      hour = "0" + String(tm_Hour);
    else
      hour = String(tm_Hour);
    if (tm_Minute < 10)
      minute = "0" + String(tm_Minute);
    else
      minute = String(tm_Minute);
    currentTime = hour + ":" + minute;
    
    tft.pushImage(5, 5,  64, 64, image[img_count]);
    showtext(95,22,1,4,fg,bg,currentTime);
    //showEmail();
    
    delay(100);
    img_count++;
    time_count++;
    if(img_count>8){img_count=0;}


}

void loop()
{
  show(TFT_WHITE,TFT_BLACK,Astronaut);
  if (targetTime < millis()){
    targetTime += 30*60*1000;//半个小时请求一次邮件信息
    
    sendData();
    showEmail();   
    }
  
 // count++;
//  show_time(TFT_WHITE, TFT_BLACK, Astronaut, currentTime, currentDate, tm_Year, week); // 显示时间界面
  delay(50);
}
