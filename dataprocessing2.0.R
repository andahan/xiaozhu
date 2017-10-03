
##################################第一波数据处理####################################
library(openxlsx)
library(reshape2)
library(stringr)
library(magrittr)
library(dplyr)
###input宽数据###
GDP_wide <- read.xlsx("GDP.xlsx", sheet = 1)
College_wide <- read.xlsx("学校数高等.xlsx", sheet = 1)
Population_wide <- read.xlsx("人口.xlsx", sheet = 1)
Income_wide <- read.xlsx("工资.xlsx", sheet = 1)
TourismIncome_wide <- read.xlsx("旅游收入国内.xlsx", sheet = 1)
TourismPop_wide <- read.xlsx("旅游人数国内.xlsx", sheet = 1)

###变成长数据###
GDP_long <- melt(GDP_wide,id.vars = "year")
College_long <- melt(College_wide,id.vars = "year")
Population_long <- melt(Population_wide,id.vars = "year")
Income_long <- melt(Income_wide,id.vars = "year")
TourismIncome_long <- melt(TourismIncome_wide,id.vars = "year")
TourismPop_long <- melt(TourismPop_wide,id.vars = "year")
#修改列名
colnames(GDP_long)=c('year','city','GDP')
colnames(College_long)=c('year','city','College')
colnames(Population_long)=c('year','city','Population')
colnames(Income_long)=c('year','city','Income')
colnames(TourismIncome_long)=c('year','city','TourismIncome')
colnames(TourismPop_long)=c('year','city','TourismPop')

###合并数据集###
m1 <- merge(GDP_long,College_long,all.x=TRUE)
m2 <- merge(m1,Population_long,all.x=TRUE)
m3 <- merge(m2,Income_long,all.x=TRUE)
m4 <- merge(m3,TourismIncome_long,all.x=TRUE)
CluData <- merge(m4,TourismPop_long,all.x=TRUE)

#timetype
#CluData$year <- as.Date(CluData$year,origin="1900-01-01")
#CluData$year <- substr(CluData$year,1,4)

###输出结果###
write.table(CluData,file="CluData.csv",sep=",",row.name=FALSE,col.names =TRUE)

###########################第二波数据处理：未处理空值########################
#input header###
xiaozhunctrip1.0<- read.csv("xiaozhunctrip1.0.csv")
CluData1.0<- read.csv("CluData1.0.csv")
CluData2.0 <- merge(xiaozhunctrip1.0,CluData1.0,all.y=TRUE)
#空值转化为0
CluData2.0$xiaozhu_year[is.na(CluData2.0$xiaozhu_year)] <- 0
CluData2.0$ctrip_year[is.na(CluData2.0$ctrip_year)] <- 0
#2017转化为0
CluData2.0$xiaozhu_year <- str_replace_all(CluData2.0$xiaozhu_year,"2017","0")
#xiaozhu_year，ctrip_year onehot
f=function(x,y){
  if(x<=y){
    x=1
  }else if
  (x>y){
    x=0
  }
}
f0=function(x,y){
  if(x==y){
    x=1
  }else if
  (x!=y){
    x=0
  }
}
f1=function(x,y){
  if(y-x==1){
    x=1
  }else if
  (y-x!=1){
    x=0
  }
}
f2=function(x,y){
  if(y-x==2){
    x=1
  }else if
  (y-x!=2){
    x=0
  }
}
f3=function(x,y){
  if(y-x==3){
    x=1
  }else if
  (y-x!=3){
    x=0
  }
}
f4=function(x,y){
  if(y-x==4){
    x=1
  }else if
  (y-x!=4){
    x=0
  }
}
f5=function(x,y){
  if(y-x==5){
    x=1
  }else if
  (y-x!=5){
    x=0
  }
}
f6=function(x,y){
  if(y-x==6){
    x=1
  }else if
  (y-x!=6){
    x=0
  }
}
f7=function(x,y){
  if(y-x==7){
    x=1
  }else if
  (y-x!=7){
    x=0
  }
}
f8=function(x,y){
  if(y-x==8){
    x=1
  }else if
  (y-x!=8){
    x=0
  }
}
f9=function(x,y){
  if(y-x==9){
    x=1
  }else if
  (y-x!=9){
    x=0
  }
}
f10=function(x,y){
  if(y-x==10){
    x=1
  }else if
  (y-x!=10){
    x=0
  }
}
f11=function(x,y){
  if(y-x==10){
    x=1
  }else if
  (y-x!=10){
    x=0
  }
}
f12=function(x,y){
  if(y-x==10){
    x=1
  }else if
  (y-x!=10){
    x=0
  }
}
f13=function(x,y){
  if(y-x==10){
    x=1
  }else if
  (y-x!=10){
    x=0
  }
}
f14=function(x,y){
  if(y-x==10){
    x=1
  }else if
  (y-x!=10){
    x=0
  }
}

CluData2.0$xiaozhu_year_full <- mapply(f,CluData2.0$xiaozhu_year,CluData2.0$year)
CluData2.0$ctrip_year_full <- mapply(f,CluData2.0$ctrip_year,CluData2.0$year)

CluData2.0$xiaozhu_year0 <- mapply(f0,CluData2.0$xiaozhu_year,CluData2.0$year)
CluData2.0$ctrip_year0 <- mapply(f0,CluData2.0$ctrip_year,CluData2.0$year)

CluData2.0$xiaozhu_year1 <- mapply(f1,CluData2.0$xiaozhu_year,CluData2.0$year)
CluData2.0$ctrip_year1 <- mapply(f1,CluData2.0$ctrip_year,CluData2.0$year)

CluData2.0$xiaozhu_year2 <- mapply(f2,CluData2.0$xiaozhu_year,CluData2.0$year)
CluData2.0$ctrip_year2 <- mapply(f2,CluData2.0$ctrip_year,CluData2.0$year)

CluData2.0$xiaozhu_year3 <- mapply(f3,CluData2.0$xiaozhu_year,CluData2.0$year)
CluData2.0$ctrip_year3 <- mapply(f3,CluData2.0$ctrip_year,CluData2.0$year)

CluData2.0$xiaozhu_year4 <- mapply(f4,CluData2.0$xiaozhu_year,CluData2.0$year)
CluData2.0$ctrip_year4 <- mapply(f4,CluData2.0$ctrip_year,CluData2.0$year)

CluData2.0$ctrip_year5 <- mapply(f5,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year6 <- mapply(f6,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year7 <- mapply(f7,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year8 <- mapply(f8,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year9 <- mapply(f9,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year10 <- mapply(f10,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year11 <- mapply(f11,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year12 <- mapply(f12,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year13 <- mapply(f13,CluData2.0$ctrip_year,CluData2.0$year)
CluData2.0$ctrip_year14 <- mapply(f14,CluData2.0$ctrip_year,CluData2.0$year)
###输出结果###
write.table(CluData2.0,file="CluData2.0.csv",sep=",",row.name=FALSE,col.names =TRUE)

